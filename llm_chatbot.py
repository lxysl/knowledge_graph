import json
import time
from py2neo import Graph
from openai import OpenAI


def request_llm(llm, prompt):
    response = llm.chat.completions.create(
        model="deepseek-coder",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": prompt}
        ],
        stream=False
    )
    content = response.choices[0].message.content
    cur_time = time.time()
    log_content = content.replace('\n', f'\n[LOG] {cur_time}: ')
    print(f"[LOG] {cur_time}: {log_content}")
    return content

class QuestionFilter:
    def filter(self, llm, question):
        prompt = f'你是一个依赖于知识库回答问题的严谨可靠的心血管疾病问诊助手，请根据以下问题判断是否需要从心血管疾病数据库中进行查询专业知识以回答用户提问：{question}。通过如下 json 格式返回结果：{{"result": "True"}} 或 {{"result": "False"}}'
        response = request_llm(llm, prompt)
        result = json.loads(response.replace("```json", '').replace("```", ''))
        return result

class EntityExtractor:
    def extract(self, llm, question):
        prompt = f'从以下问题中提取医疗实体和关系：{question}。通过如下 json 格式返回结果：{{"entities": ["entity1", "entity2", ...], "relations": ["relation1", "relation2", ...]}}'
        response = request_llm(llm, prompt)
        response = json.loads(response.replace("```json", '').replace("```", ''))
        entities, relations = response["entities"], response["relations"]
        return entities, relations

class QueryGenerator:
    def __init__(self):
        # 加载已知的疾病名称
        self.known_diseases = set()
        try:
            with open('./prepare_data/disease_name.txt', 'r', encoding='UTF-8') as f:
                for line in f:
                    self.known_diseases.add(line.strip())
        except Exception as e:
            print(f"[LOG] {time.time()}: 无法加载疾病名称文件：{str(e)}")

        # 添加属性名映射
        self.property_mapping = {
            'cause': 'causeName',
            'pathogenesis': 'pathogenesisName',
            'clinicalManifestations': 'clinicalManifestationsName',
            'differentialDiagnosis': 'differentialDiagnosisName',
            'diagnosis': 'diagnosisName',
            'treatment': 'treatmentName',
            'checks': 'checksName',
            'taboos': 'taboosName',
            'prevention': 'preventionName',
            'riskFactors': 'riskFactorsName',
            'diseaseSite': 'diseaseSiteName',
            'relatedDoctors': 'relatedDoctorsName',
            'relatedDiseases': 'relatedDiseasesName',
            'department': 'departmentName'
        }

        # 定义已知的关系类型
        self.known_relations = {f'r_{k}' for k in self.property_mapping.keys()}

    def check_in_database(self, entities, relations):
        """检查实体和关系是否在数据库中存在"""
        if not entities:
            return False, "未识别到任何实体"
            
        # 检查是否包含已知疾病
        has_known_entity = any(disease in entities for disease in self.known_diseases)
        return has_known_entity, "找到匹配的疾病实体" if has_known_entity else "未找到匹配的疾病实体"

    def generate(self, llm, entities, relations, question):
        # 检查实体是否在数据库中
        has_entities, message = self.check_in_database(entities, relations)
        
        if not has_entities:
            # 如果没有找到匹配的实体或关系无效，返回特殊标记
            return None, message
            
        # 生成查询
        prompt = f"""根据以下实体、关系和问题生成Cypher查询：
实体：{entities}
关系：{relations}
问题：{question}
已知关系类型：{self.known_relations}
节点属性名映射：{self.property_mapping}
要求：
1. 查询必须是只读操作
2. 疾病节点标签为'disease'，属性名为'diseaseName'
3. 使用正确的属性名进行查询（例如：cause节点的属性名应该是'causeName'）
4. 使用已知关系类型进行查询（例如：r_cause表示病因关系）
5. 通过如下 json 格式返回结果：{{"queries": ["cypher_query1", "cypher_query2", ...]}}
"""
        response = request_llm(llm, prompt)
        queries = json.loads(response.replace("```json", '').replace("```", ''))
        return queries, "OK"

class AnswerFormatter:
    def format(self, llm, query_results, question):
        prompt = f"根据查询结果回答以下问题。问题：{question}，查询结果：{query_results}"
        response = request_llm(llm, prompt)
        return response

class GraphRAGChatBot:
    def __init__(self):
        self.llm = OpenAI(api_key="sk-ba015551788a47438f4933c407d2c1fd", base_url="https://api.deepseek.com")
        self.g = Graph(
            "neo4j://localhost:7687",
            auth=("neo4j", "12345678")
        )
        # 检查数据库能否连接
        try:
            self.g.run("RETURN 1")
        except Exception as e:
            print(f"[LOG] {time.time()}: 数据库连接失败：{str(e)}")
            self.g = None
        self.question_filter = QuestionFilter()
        self.entity_extractor = EntityExtractor()
        self.query_generator = QueryGenerator()
        self.answer_formatter = AnswerFormatter()

    def free_answer(self, question):
        """当用户提问不需要查询数据库时，直接使用LLM生成答案"""
        prompt = f"""你是心卫士医药智能助理，一个可靠的心血管疾病问诊助手，请回答用户提问：{question}"""
        return request_llm(self.llm, prompt)

    def direct_answer(self, question):
        """当无法查询数据库时，直接使用LLM生成答案"""
        prompt = f"""请回答以下医疗相关问题，{question}。注意：由于数据库中没有相关信息，请基于你的知识谨慎回答，并在回答开头以醒目字体声明“**该回答为模型自动生成，仅供参考，请仔细甄别**”。"""
        return request_llm(self.llm, prompt)

    def chat(self, question):
        try:
            # 0. 问题过滤
            result = self.question_filter.filter(self.llm, question)
            
            if not eval(result["result"]):
                print(f"[LOG] {time.time()}: 问题过滤无需查询数据库")
                return self.free_answer(question)

            # 1. 实体抽取
            entities, relations = self.entity_extractor.extract(self.llm, question)
            
            # 2. 生成查询
            queries, status = self.query_generator.generate(self.llm, entities, relations, question)
            
            # 如果没有找到匹配的实体或关系无效，直接使用LLM回答
            if status != "OK":
                print(f"[LOG] {time.time()}: {status}")
                return self.direct_answer(question)
            
            # 3. 执行查询
            ans = []
            for query in queries["queries"]:
                try:
                    query_result = self.g.run(query).data()
                    print(f"[LOG] {time.time()}: 查询结果：{query_result}")

                    if not query_result:  # 如果查询结果为空
                        print(f"[LOG] {time.time()}: 查询结果为空")
                        ans.append(self.direct_answer(question))
                    else:
                        ans.append(query_result)

                except Exception as e:
                    print(f"[LOG] {time.time()}: 数据库查询错误：{str(e)}")
                    ans.append(self.direct_answer(question))

            ans = str(ans)
            print(f"[LOG] {time.time()}: 查询结果：{ans}")
            
            # 4. 格式化答案
            return self.answer_formatter.format(self.llm, ans, question)

        except Exception as e:
            return f"抱歉，处理您的问题时出现错误：{str(e)}"


if __name__ == '__main__':
    handler = GraphRAGChatBot()
    print('您好，我是心卫士医药智能助理，希望可以帮到您。本问答系统仅供参考，请谨遵医嘱。祝您身体棒棒！')
    while 1:
        question = input('用户:')
        answer = handler.chat(question)
        print('心卫士:', answer)

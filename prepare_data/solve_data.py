import pandas as pd
from py2neo import Graph, Node, Relationship

neo_graph = Graph(
    "http://localhost:7474",
    username="neo4j",
    password="neo4j"
)

labels = {'病因': 'cause',
          '发病机制': 'pathogenesis',
          '临床表现': 'clinicalManifestations',
          '鉴别诊断': 'differentialDiagnosis',
          '诊断': 'diagnosis',
          '治疗': 'treatment',
          '检查': 'checks',
          '禁忌': 'taboos',
          '预防': 'prevention',
          '危险因素': 'riskFactors',
          '发病部位': 'diseaseSite',
          '相关医生': 'relatedDoctors',
          '相关疾病': 'relatedDiseases',
          '科室': 'department'}


def solve_data(name, type):
    # read csv data
    csv_path = '../' + type + '/csv_data/' + name + '.csv'
    df = pd.read_csv(csv_path)
    data = df.values  # list
    # print(df.values)

    # 创建疾病节点
    disease_name = data[0][0]  # i[0] is the name of i
    disease_node = Node('disease', diseaseName=disease_name)
    try:
        neo_graph.create(disease_node)
    except:
        pass

    disease_node = neo_graph.nodes.match('disease', diseaseName=disease_name).first()
    for i in data:
        if i[2] == 2 or i[2] == 3:
            if i[2] == 2:  # i[2] is the category of i
                # 标签名   i[4] is the target of i
                label_name = data[i[4]][0]  # '病因' i.target.name
                label_value = labels[label_name]  # 'cause'

            if i[2] == 3:
                # 标签名
                label_name = data[data[i[4]][4]][0]  # '治疗' i.target.target.name
                r_property_name = data[i[4]][0]  # '预防血栓栓塞' i.target.name
                label_value = labels[label_name]  # 'treatment'

            if label_name == '病因':
                target_node = Node(label_value, causeName=i[0]) if (n := neo_graph.nodes.match(label_value, causeName=i[0]).first()) is None else n
            if label_name == '发病机制':
                target_node = Node(label_value, pathogenesisName=i[0]) if (n := neo_graph.nodes.match(label_value, pathogenesisName=i[0]).first()) is None else n
            if label_name == '临床表现':
                target_node = Node(label_value, clinicalManifestationsName=i[0]) if (n := neo_graph.nodes.match(label_value, clinicalManifestationsName=i[0]).first()) is None else n
            if label_name == '鉴别诊断':
                target_node = Node(label_value, differentialDiagnosisName=i[0]) if (n := neo_graph.nodes.match(label_value, differentialDiagnosisName=i[0]).first()) is None else n
            if label_name == '诊断':
                target_node = Node(label_value, diagnosisName=i[0]) if (n := neo_graph.nodes.match(label_value, diagnosisName=i[0]).first()) is None else n
            if label_name == '治疗':
                target_node = Node(label_value, treatmentName=i[0]) if (n := neo_graph.nodes.match(label_value, treatmentName=i[0]).first()) is None else n
            if label_name == '检查':
                target_node = Node(label_value, checksName=i[0]) if (n := neo_graph.nodes.match(label_value, checksName=i[0]).first()) is None else n
            if label_name == '禁忌':
                target_node = Node(label_value, taboosName=i[0]) if (n := neo_graph.nodes.match(label_value, taboosName=i[0]).first()) is None else n
            if label_name == '预防':
                target_node = Node(label_value, preventionName=i[0]) if (n := neo_graph.nodes.match(label_value, preventionName=i[0]).first()) is None else n
            if label_name == '危险因素':
                target_node = Node(label_value, riskFactiorsName=i[0]) if (n := neo_graph.nodes.match(label_value, riskFactiorsName=i[0]).first()) is None else n
            if label_name == '发病部位':
                target_node = Node(label_value, diseaseSiteName=i[0]) if (n := neo_graph.nodes.match(label_value, diseaseSiteName=i[0]).first()) is None else n
            if label_name == '相关医生':
                target_node = Node(label_value, relatedDoctorsName=i[0]) if (n := neo_graph.nodes.match(label_value, relatedDoctorsName=i[0]).first()) is None else n
            if label_name == '相关疾病':
                target_node = Node(label_value, relatedDiseasesName=i[0]) if (n := neo_graph.nodes.match(label_value, relatedDiseasesName=i[0]).first()) is None else n
            if label_name == '科室':
                target_node = Node(label_value, departmentName=i[0]) if (n := neo_graph.nodes.match(label_value, departmentName=i[0]).first()) is None else n
            try:
                neo_graph.create(target_node)
            except:
                pass  # 已存在

            # 关系名
            relation_value = 'r_' + label_value  # 'r_cause'
            try:
                relation = Relationship(disease_node, relation_value, target_node)
            except:
                print(label_name + '未列出')
                exit(1)
            if i[2] == 3:
                relation['relation_property'] = r_property_name
            neo_graph.create(relation)
    print('图数据库加载结束！')


def constraint_unique():
    nodes = neo_graph.nodes
    try:
        neo_graph.schema.create_uniqueness_constraint('disease', 'diseaseName')
    except:
        # 不能在已有限制的标签上添加限制
        pass
    for label in labels:
        try:
            neo_graph.schema.create_uniqueness_constraint(labels[label], labels[label] + 'Name')
        except:
            pass


if __name__ == '__main__':
    disease_list = []
    with open(r'./disease_name.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            disease_list.append(line.strip('\n').split(',')[0])
        # print(disease_list)
    num = len(disease_list)
    for index, value in enumerate(disease_list):
        print(str(index + 1) + '/' + str(num) + '正在处理"' + value + '"数据...')
        solve_data(value, 'disease')
        constraint_unique()

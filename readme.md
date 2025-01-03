## 基于知识图谱的心血管疾病问答系统

基于知识图谱的心血管疾病问答系统，使用Neo4j作为知识图谱数据库，通过关键词匹配构建问答系统，**新增LLM作为通用问答系统**。

#### 效果展示

![demo](pic/demo.gif)

#### 系统架构

![pic1](pic/1.png)

![pic2](pic/2.png)

![pic3](pic/3.png)

![pic4](pic/4.png)


#### 使用方法

1. 安装并启动Neo4j数据库

```
neo4j console
```

2. 导入知识图谱数据

```
cd prepare_data
python solve_data.py
```

3. 安装依赖

```
pip install -r requirements.txt
```

4. 启动 chatbot_graph.py 或 llm_chatbot.py

```
python chatbot_graph.py
python llm_chatbot.py  # 需要设置 api_key
```

5. Enjoy your chat!

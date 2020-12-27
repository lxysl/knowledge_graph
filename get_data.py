import requests
import json
import pandas as pd


def get_data(name, type):
    url = 'http://med.ckcest.cn/knowledgeGraphs.do'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3775.400 QQBrowser/10.6.4208.400'
    }
    data = {'name': name}
    response = requests.post(url=url, data=data, headers=header)

    json_obj = response.json()
    print(json_obj)
    print('json数据打印结束！')

    file_name = './' + type + '/json_data/' + name + '.json'
    fp = open(file_name, 'w', encoding='utf-8')
    json.dump(json_obj, fp=fp, ensure_ascii=False)
    print('json数据存储结束！')


def json_to_csv(name, type):
    json_path = './' + type + '/json_data/' + name + '.json'
    csv_path = './' + type + '/csv_data/' + name + '.csv'

    json_data = None
    row_list = []
    with open(json_path, "r", encoding='utf-8') as f:
        for json_data in f:
            json_data = json.loads(json_data)
            # print(json_data)

    column_name = json_data[0].keys()
    for i in json_data:
        row_list.append(list(i.values()))
    # print(row_list)

    df = pd.DataFrame(columns=column_name, data=row_list)
    df.to_csv(csv_path, encoding='utf-8', index=False)
    print('csv数据存储结束！')


if __name__ == '__main__':
    disease_list = ['心房颤动']
    num = len(disease_list)
    for index, value in enumerate(disease_list):
        print(str(index + 1) + '/' + str(num) + '正在获取"' + value + '"数据...')
        get_data(value, 'disease')
        json_to_csv(value, 'disease')

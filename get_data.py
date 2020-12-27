import requests
import json


def get_data(name):
    url = 'http://med.ckcest.cn/knowledgeGraphs.do'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3775.400 QQBrowser/10.6.4208.400'
    }
    data = {'name': name}

    response = requests.post(url=url, data=data, headers=header)
    json_obj = response.json()
    print(json_obj)
    print('数据打印结束！')

    file_name = name + '.json'
    fp = open(file_name, 'w', encoding='utf-8')
    json.dump(json_obj, fp=fp, ensure_ascii=False)
    print('数据存储结束！')


if __name__ == '__main__':
    name_list = ['心房颤动']
    for i in name_list:
        get_data(i)

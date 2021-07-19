#coding:utf-8
import requests,json

message={"path":'data/etf.xlsx', "clusterNum":120}
url = "http://127.0.0.1:8000/cluster/etf"
# url = "http://127.0.0.1:8000/cluster/mix"
# url = "http://127.0.0.1:8000/cluster/stock"
r = requests.post(url,data=json.dumps(message))
print(r.json)


#coding:utf-8
from flask import Flask, request, jsonify
from flask import Blueprint
import json
from etf import ETFCluster
from mix import MIXCluster
from stock import StockCluster
import sys

cluster=Blueprint("home",__name__,url_prefix="/cluster")
@cluster.route("/stock",methods=['post','get'])
def post_http1():
    '''
    股票
    '''
    result={
        "code":200,
        "msg":"成功"
    }
    if not request.data:
        result['code']=100
    try:
        params=request.data
        print(params)
        message = json.loads(params)

        path = message.get("path")
        k = message.get('clusterNum')
        clusters, sim_result = StockCluster(path=path, k=k, iter=100, interval=0.1).main(plot=False)
        result["cluster"]=clusters
        result["simmilarity"]=sim_result
    except Exception as e:
        result["msg"]=str(e)
        result['code']=100
    return jsonify(result)

@cluster.route("/etf",methods=['post','get'])
def post_http2():
    result={
        "code":200,
        "msg":"成功"
    }
    if not request.data:
        result['code']=100
    try:
        params=request.data
        print(params)
        message = json.loads(params)

        path = message.get("path")
        k = message.get('clusterNum')
        clusters, sim_result = ETFCluster(path=path, k=k, iter=100, interval=0.1).main(plot=False)
        result["cluster"] = clusters
        result["simmilarity"] = sim_result
    except Exception as e:
        result["msg"]=str(e)
        result['code']=100
    return jsonify(result)

@cluster.route("/mix",methods=['post','get'])
def post_http3():
    result={
        "code":200,
        "msg":"成功"
    }
    if not request.data:
        result['code']=100
    try:
        params=request.data
        print(params)
        message = json.loads(params)

        path = message.get("path")
        k = message.get('clusterNum')
        clusters, sim_result = MIXCluster(path=path, k=k, iter=100, interval=0.1).main(plot=False)
        result["cluster"] = clusters
        result["simmilarity"] = sim_result
    except Exception as e:
        result["msg"]=str(e)
        result['code']=100
    return jsonify(result)

if __name__=='__main__':
    host=sys.argv[1]
    port=sys.argv[2]
    app = Flask(__name__)
    app.register_blueprint(cluster)
    app.run(host=host, port=port)

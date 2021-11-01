from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from search import *

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route("/search", methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def searchModel():
    # try:
    opt, query = getData(request.json)
    print(opt, query)
    return search(opt,query)
    # # except:
    # #     return jsonify({'state': 'ko'})
@app.route("/s/doc", methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def getPage():
    # try:
    _ , query = getData(request.json)
    print(query)
    return getPageDoc(query)
    # # except:
    # #     return jsonify({'state': 'ko'})


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)

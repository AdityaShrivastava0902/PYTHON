from flask import Flask, jsonify, request
from flask_restful import Resource, Api

demo1 = Flask("__main__")
api = Api(demo1)

def checkData(data,fn_name):
    if(fn_name=="add" or fn_name=="substract" or fn_name=="multiply"):
        if 'x' not in data or 'y' not in data:
            return 301
        else:
            return 200
    elif(fn_name=="divide"):
        if 'x' not in data or 'y' not in data:
            return 301
        elif int(data["y"])==0:
            return 302
        else:
            return 200


class Add(Resource):
    def post(self):
        data = request.get_json()
        status_code = checkData(data,"add")
        if status_code==301:
            retMap = {
                'message':"an error has happened",
                'Status Code':301
            }

            return jsonify(retMap)

        x = data["x"]
        y = data["y"]
        x = int(x)
        y = int(y)
        ret = x+y
        retMap = {
            'message':ret,
            'Status Code':200
        }
        return jsonify(retMap)

class Substract(Resource):
    def post(self):
        data = request.get_json()
        status_code = checkData(data,"substract")
        if status_code==301:
            retMap = {
                'message':"an error has happened",
                'Status Code':301
            }

            return jsonify(retMap)

        x = data["x"]
        y = data["y"]
        x = int(x)
        y = int(y)
        ret = x-y
        retMap = {
            'message':ret,
            'Status Code':200
        }
        return jsonify(retMap)

class Multiply(Resource):
    def post(self):
        data = request.get_json()
        status_code = checkData(data,"multiply")
        if status_code==301:
            retMap = {
                'message':"an error has happened",
                'Status Code':301
            }

            return jsonify(retMap)

        x = data["x"]
        y = data["y"]
        x = int(x)
        y = int(y)
        ret = x*y
        retMap = {
            'message':ret,
            'Status Code':200
        }
        return jsonify(retMap)

class Divide(Resource):
    def post(self):
        data = request.get_json()
        status_code = checkData(data,"divide")
        if status_code==301:
            retMap = {
                'message':"an error has happened",
                'Status Code':301
            }
            return jsonify(retMap)
        elif status_code==302:
            retMap = {
                'message':"an error has happened",
                'Status Code':302
            }
            return jsonify(retMap)

        x = data["x"]
        y = data["y"]
        x = int(x)
        y = int(y)
        ret = (x*1.0)/y
        retMap = {
            'message':ret,
            'Status Code':200
        }
        return jsonify(retMap)



api.add_resource(Add,"/add")
api.add_resource(Substract,"/substract")
api.add_resource(Multiply,"/multiply")
api.add_resource(Divide,"/divide")








if __name__=="__main__":
    demo1.run(debug=True,host="127.0.0.1", port=80)
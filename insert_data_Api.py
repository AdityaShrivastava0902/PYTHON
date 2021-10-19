from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import pymongo


connection = pymongo.MongoClient("mongodb://localhost:27017/")
db = connection['demo_20211001']
collection = db['crud_demo_via_api']


insert_data_api = Flask("__main__")
api = Api(insert_data_api)



def checkData(data,fn_name):
    if fn_name=="insert":
        if "state" not in data  or "capital" not in data or "cm" not in data:
            return 400
        else:
            return 200
    elif fn_name=="update":
        if "where" not in data  or "newValue" not in data:
            return 400
        else:
            return 200
    elif fn_name=="find":
        if "state" not in data:
            return 400
        else:
            return 200
    
    pass


class Insert(Resource):
    def post(self):
        data = request.get_json()
        status_code = checkData(data,"insert")
        if status_code == 400:
            retMap = {
                        "status code":400,
                        "message": "Bad Request" 
                    }
            return jsonify(retMap)
        collection.insert_one(data)
        retMap = {
            "status code":status_code,
            "message": "successful" 
        }
        return jsonify(retMap)
    pass



class Update(Resource):
    def post(self):
        data = request.get_json()
        status_code = checkData(data,"update")
        if status_code ==400:
            retMap = {
                        "status code":400,
                        "message": "Bad Request" 
                    }
            return jsonify(retMap)
        where = data["where"]
        newVal= data["newValue"]
        collection.update_one(where,newVal)
        retMap = {
            "status code":status_code,
            "message": "successful" 
        }
        return jsonify(retMap)
    pass



class Delete(Resource):
    def post(self):
        data = request.get_json()
        id = data["state"]
        collection.delete_one({
        "state": id
        })
        retMap = {
        "status": 200,
        "msg": "successful"
        }
        return jsonify(retMap)
    pass



class Read(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        id = data["state"]
        print(id)
        status_code = checkData(data,"find")
        if status_code == 400:
            retMap = {
                        "status code":400,
                        "message": "Bad Request" 
                    }
            return jsonify(retMap)

        db_data = collection.find({"state":id},{"capital":1,"cm":1})
        print(db_data)
        retMap = {
            "message":db_data,
            "status code":200
        }
        return jsonify(retMap)
    pass




#insert_data_api.run(debug=True,host="127.0.0.1", port=80)


api.add_resource(Insert,"/insert")
api.add_resource(Update,"/update")
api.add_resource(Delete,"/delete")
api.add_resource(Read,"/read")

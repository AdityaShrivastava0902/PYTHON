from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import pymongo as mongo
import json


connection = mongo.MongoClient("mongodb://localhost:27017/")
db = connection['hr']
collection = db['hr']

aggregation = Flask("__main__")
api = Api(aggregation)

def checkCode(data,fn_name):
    if len(data)=="$Last % Hike":
        retMap = {
                    "message" : "invalid arguments",
                    "code" : 500,
                    "status": "failed"
                    }
        return retMap #empty json received
    if fn_name=="three_decades":


        if "first" not in data or "last" not in data or "salary" not in data:
            retMap = {
                    "message" : "invalid arguments",
                    "status" : "failed",
                    "code" : 500
                    }     
            return retMap   #not all parameters received  
        elif isinstance(data["first"], int) and isinstance(data["last"], int) and isinstance(data["salary"], int):
            retMap = {
                        "code" : 200,
                        "status": "failed"
                        }  
            return retMap
        else:
            retMap = {
                        "message" : "missing arguments",
                        "code" : 600,
                        "status": "failed"
                        } 
            return retMap


    elif fn_name=="different_count":
        if "name" not in data:
            retMap = {
                        "message" : "missing arguments",
                        "status" : "failed",
                        "code" : 600
                        }  
            return retMap
        elif isinstance(data["name"], (int,float)):
            retMap = {
                        "message" : "invalid arguments",
                        "code" : 500,
                        "status": "failed"
                        }  
            return retMap
        else:
            retMap = {
                "code": 200,
                "message":"incorrect data"
                }  
            return retMap
        
    elif fn_name == "count_ratio":
        if "type" not in data:
            retMap = {
                    "message" : "missing arguments",
                    "status" : "failed",
                    "code" : 600
                    }  
            return retMap
        elif isinstance(data["type"], (int,float)):
            retMap = {
                        "message" : "invalid arguments",
                        "code" : 500,
                        "status": "failed"
                        }  
            return retMap
        else:
            retMap = {
                "code": 200,
                "message":"incorrect data"
                }  
            return retMap

    elif fn_name == "hike":
        if "percentage" not in data:
            retMap = {
                        "message" : "missing arguments",
                        "status" : "failed",
                        "code" : 600
                        }  
            return retMap
        elif isinstance(data["percentage"], (int,float)):
            retMap =  {
                "code":200
            }
            return retMap
        else:
            retMap = {
                        "message" : "invalid arguments",
                        "code" : 500,
                        "status": "failed"
                        }  
            return retMap



class three_decades(Resource):
    def post(self):
        data = request.get_json()
        retMap = checkCode(data,"three_decades")
        if retMap["code"]!=200:
            return jsonify(retMap)

        first = data["first"]
        last = data["last"]
        sal = data["salary"]
        obj = collection.aggregate([
                                    {"$match":{ "Year of Joining" : {"$gte" : first,
                                                                    "$lte":last
                                                                    },
                                                "Salary" : {"$gte" : sal}
                                            }
                                    },
                                    {"$group": { "_id" : "$Last % Hike",
                                                "count" : {"$sum":1},
                                                "min salary":{"$min":"$Salary"},
                                                "max salary":{"$max":"$Salary"},
                                                "average salary":{"$avg":"$Salary"}
                                            }
                                    }
                                ])
        retMap={
                "status" : "success",
                "message": "success",
                "code" : 200,
                "data":{}
                }
        for i in obj:
            retMap["data"]["count"]=i["count"]
            retMap["data"]["min salary"]=i["min salary"]
            retMap["data"]["max salary"]=i["max salary"]
            retMap["data"]["average salary"]=i["average salary"]
        return(jsonify(retMap))
    pass

class count_ratio(Resource):
    def post(self):
        data = request.get_json()
        retMap = checkCode(data,"count_ratio")
        if retMap["code"]!=200:
            return jsonify(retMap)
        name = data["type"]
        arr = ["M","F"]
        if name not in arr:
            retMap = {
                        "message" : "invalid arguments",
                        "code" : 500,
                        "status": "failed"
                        }
            return jsonify(retMap)
        obj = db.hr.aggregate([
                    {"$match":{"Gender":name}},
                    {"$group":{"_id":"$Gender",
                        "count":{"$sum":1}
                        }
                    }
                ])
        ret = {}
        for i in obj:
            ret[i["_id"]]=i["count"]
        retMap={
                "status" : "success",
                "message": "success",
                "code" : 200,
                "data":ret
                }
        return(jsonify(retMap))


class different_counts(Resource):
    def post(self):
        data = request.get_json()
        retMap = checkCode(data,"different_count")
        if retMap["code"]!=200:
            return jsonify(retMap)
        arr = ["Mr.","Hon.","Dr.","Drs.","Mrs.","Prof.","Ms."]
        name = data["name"]
        if name not in arr:
            retMap = {
                        "message" : "invalid arguments",
                        "code" : 500,
                        "status": "failed"
                        }
            return jsonify(retMap)
        

        obj = collection.aggregate([
                    {"$match":{"Name Prefix": name }
                    },
                    {"$group":{"_id":"$Name Prefix",
                            "count":{"$sum":1}
                        }
                    }
                ])
        ret = {}
        for i in obj:
            ret[i["_id"]]=i["count"]
        retMap={
                "status" : "success",
                "message": "success",
                "code" : 200,
                "data":ret
                }

        

        return(jsonify(retMap))
    pass


class hike(Resource):
    def post(self):
        data = request.get_json()
        retMap = checkCode(data,"hike")
        if retMap["code"]!=200:
            return jsonify(retMap)
        percentage = data["percentage"]
        percentage = str(percentage)+"%"
        obj = collection.aggregate([
                                    {"$match":{ "Last % Hike" : percentage}
                                    },
                                    {"$group": { "_id" : "$Last % Hike",
                                    "count" : {"$sum":1}
                                    }
                                    }
                                    ])
        ret={}
        for i in obj:
            ret[i["_id"]]=i["count"]

        retMap={
                "status" : "success",
                "message": "success",
                "code" : 200,
                "data":ret
                }
        return jsonify(retMap)



    pass
api.add_resource(different_counts,"/different_counts")
api.add_resource(three_decades,"/three_decades")
api.add_resource(count_ratio,"/count_ratio")
api.add_resource(hike,"/hike")
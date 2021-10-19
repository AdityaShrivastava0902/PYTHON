import pymongo
from pymongo import collection

if __name__ == '__main__':
    conn = pymongo.MongoClient("mongodb://localhost:27017/")
    table = conn['users']
    collection = table['address']
    # connection = pymongo.MongoClient("mongodb://localhost:27017/")
    # db = connection['apidb']
    # collection = db['address']
    
    insertItem = [{"_id": 1, 'Name': 'komal', 'Destination': 'Italy'},
                  {"_id": 2, 'Name': 'Aditya', 'Destination': 'Switzerland'},
                  {"_id": 3, 'Name': 'Nandini', 'Destination': 'Germany'},
                  {"_id": 4, 'Name': 'Sonu', 'Destination': 'Canada'}
                  ]
    collection.insert_many(insertItem)
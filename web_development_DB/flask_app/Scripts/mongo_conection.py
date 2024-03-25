import pymongo as MongoDB
import os
def write_data(URL,data):
    state=check_db(URL=URL)
    if state:
        client = MongoDB.MongoClient(URL)
        db = client[os.environ['MONGO_DATA_BASE_NAME']]
        colletion = db[os.environ['MONGO_COLLECTION_NAME']]
        try:
            for DATA in data:
                DATA_MB ={
                    'Tipo': DATA.Tipo[0],
                    'Valor': DATA.Valor,
                    'Mb_Adress': DATA.address,
                    'Date_created': DATA.Date_created
                }
                result = colletion.insert_one(DATA_MB)
            return True
        except:
            return False
    else:
        return False
    


def check_db(URL):
    client = MongoDB.MongoClient(URL)
    db_list = client.list_database_names()
    
    if db_list.count(os.environ['MONGO_DATA_BASE_NAME']):
        db=client[os.environ['MONGO_DATA_BASE_NAME']]
        coll = db.list_collection_names()
        if coll.count(os.environ['MONGO_COLLECTION_NAME']):
            client.close()
            return True
        else:
            try:
                db.create_collection(os.environ['MONGO_COLLECTION_NAME'])
                client.close()
                return True
            except:
                client.close()
                return False    
            
    else:
        try:
           client[os.environ['MONGO_DATA_BASE_NAME']]
           db=client[os.environ['MONGO_DATA_BASE_NAME']]
           db.create_collection(os.environ['MONGO_COLLECTION_NAME'])
           client.close()
           return True
        except:
            client.close()
            return False
import pymongo

#configuration of the database 

url = 'mongodb://localhost:27017'
client = pymongo.MongoClient(url)

database = client['voting_database'] #name of the database 
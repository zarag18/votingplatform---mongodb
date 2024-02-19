import pymongo

#configuration of the database 

url = 'mongodb://localhost:27017' #url to connect to the database 
client = pymongo.MongoClient(url)

database = client['voting_database'] #name of the database 
import pymongo

url = 'mongodb://localhost:27017'
client = pymongo.MongoClient(url)

database = client['voting_database']
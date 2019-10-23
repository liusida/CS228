import pickle

database = {} 

with open('userData/database.p','wb') as f:
    pickle.dump(database,f)

import pickle
with open('userData/database.p','rb') as f:
    database = pickle.load(f)

userName = raw_input('Please enter your name: ') 
if userName in database: 
    print('welcome back ' + userName + '.')
    database[userName]['logins'] += 1
else:
    database[userName] = { 'logins': 1 }
    print('welcome ' + userName + '.')

print(database)

with open('userData/database.p','wb') as f:
    pickle.dump(database,f)

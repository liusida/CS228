import pickle

class Database:
    def __init__(self, load_from_file=True):
        if load_from_file:
            with open('userData/database.p','rb') as f:
                self.database = pickle.load(f)
        else:
            self.database = {}
        self.username = ""

    def save(self):
        with open('userData/database.p','wb') as f:
            pickle.dump(self.database,f)
            print(self.database)

    def reset(self):
        self.database = {}
        self.save()

    def login(self, username):
        self.username = username

    def set(self, key, value):
        if self.username not in self.database:
            self.database[self.username] = {}
        self.database[self.username][key] = value
        self.save()

    def inc(self, key):
        if self.username not in self.database:
            self.database[self.username] = {}
        if key not in self.database[self.username]:
            self.database[self.username][key] = 0
        self.database[self.username][key] += 1
        self.save()

    def get(self, key):
        if self.username not in self.database:
            return None
        if key not in self.database[self.username]:
            return None
        return self.database[self.username][key]

    
if __name__ == "__main__":
    db = Database(load_from_file=True)
    
    db.reset()
    #db.inc('sida', 'logins')


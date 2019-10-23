import pickle

class Database:
    def __init__(self, load_from_file=True):
        if load_from_file:
            with open('mainData/database.p','rb') as f:
                self.database = pickle.load(f)
        else:
            self.database = {}
        self.username = ""

    def save(self):
        with open('mainData/database.p','wb') as f:
            pickle.dump(self.database,f)
            print(self.database)

    def reset(self):
        self.database = {}
        self.save()

    def login(self, username):
        self.username = username

    # keys can be "level_1", "level_2", "key"
    def set(self, value, *keys):
        if self.username not in self.database:
            self.database[self.username] = {}
        entry = self.database[self.username]
        for index, key in enumerate(keys):
            if (index==len(keys)-1):
                entry[key] = value
            else:
                if key not in entry:
                    entry[key] = {}
                entry = entry[key]
        self.save()

    def set_bak(self, key, value):
        if self.username not in self.database:
            self.database[self.username] = {}
        self.database[self.username][key] = value
        self.save()

    def inc(self, *keys):
        if self.username not in self.database:
            self.database[self.username] = {}
        entry = self.database[self.username]
        for index, key in enumerate(keys):
            if (index==len(keys)-1):
                if key not in entry:
                    entry[key] = 0
                entry[key] += 1
            else:
                if key not in entry:
                    entry[key] = {}
                entry = entry[key]
        self.save()

    def get(self, *keys):
        if self.username not in self.database:
            return None
        entry = self.database[self.username]
        for index, key in enumerate(keys):
            if key not in entry:
                return None
            entry = entry[key]
        return entry
    
if __name__ == "__main__":
    db = Database(load_from_file=True)
    db.login("sida")
    #db.set(5, "scaffold_1", "digit")
    db.inc("scaffold_1","digit")
    d=db.get("scaffold_1","digit")
    print(d)

    db.reset()
    db.save()
    #db.inc('sida', 'logins')


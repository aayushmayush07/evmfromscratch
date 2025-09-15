# keyvaluestorage.py

class KeyValue:
    def __init__(self):
        self.storage={}

    def load(self,key):
        return self.storage[key]
    
    def store(self,key,value):
        self.storage[key]=value



class Storage(KeyValue):
    def __init__(self):
        super().__init__()
        self.cache=[]


    def load(self,key):
        warm=True if key in self.cache else False

        if not warm: self.cache.append(key)
        if key not in self.storage:return warm,0x00  #since sload it's asking for bot
        return warm,super.load(key)    


    # def store(self, key, value):
    #     warm = key in self.cache
    #     if not warm:
    #         self.cache.append(key)
    #     self.storage[key] = value
    #     return warm

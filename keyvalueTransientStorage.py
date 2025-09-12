class KeyValue:
    def __init__(self):
        self.storage={}

    def load(self,key):
        return self.storage[key]
    
    def store(self,key,value):
        self.storage[key]=value


class TStorage(KeyValue):
    def __init__(self):
        super().__init__()
        self.cache = []  # warm set 

    def load(self, key):
        warm = key in self.cache
        if not warm: self.cache.append(key)
        if key not in self.storage:return warm, 0x00
        return warm, super().load(key)

    def store(self, key, value):
        warm = key in self.cache
        if not warm:
            self.cache.append(key)
        self.storage[key] = value
        return warm

    def reset(self):
        # wipe I have done to clear at the end of transaction
        self.storage.clear()
        self.cache.clear()


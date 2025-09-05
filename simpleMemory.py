class SimpleMemory:
    def __init__(self):
        self.memory=[]


    def access(self,offset,size):
        return self.memory[offset:offset+size]


    def load(self,offset):
        return self.access(offset,32)

    def store(self,offset,value):
        self.memory[offset:offset+len(value)]=value




class Memory(SimpleMemory):
    def store(self,offset,value):

        memory_expansion_cost=0

        if len(self.memory)<=offset+len(value):

            expansion_size=0

            if(len(self.memory)==0):
                expansion_size=32
                self.memory=[0x00 for _ in range(32)]

            if(len(self.memory))<offset+len(value):
                expansion_size+=offset+len(value)-len(self.memory)
                self.memory.extend([0x00]*expansion_size)



            memory_expansion_cost=expansion_size**2 #simplified 
            super().store(offset,value)
            return memory_expansion_cost       



# m = Memory()

# print("Initial:", m.memory)

# # Store 4 bytes [0xaa, 0xbb, 0xcc, 0xdd] at offset 0
# cost1 = m.store(0, [0xaa,0xbb,0xcc,0xdd])
# print("After store1:", m.memory)
# print("Cost1:", cost1)

# # Store 4 bytes at offset 30 (forces expansion beyond 32)
# cost2 = m.store(30, [0x11,0x22,0x33,0x44])
# print("After store2:", m.memory)
# print("Cost2:", cost2)

# # Load 32 bytes from offset 0
# print("Load:", m.load(0))

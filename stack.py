MAXIMUM_STACK_SIZE=1024


class Stack:
    def __init__(self): self.items=[]

    def __str__(self):
        ws=[]
        for i,item in enumerate(self.items[::-1]):
            if i==0:
                ws.append(f"{item} <first>")
            elif i==len(self.items)-1:
                ws.append(f"{item} <last>")

            else:
                ws.append(str(item))

        return "\n".join(ws)

    def push(self, value): 
        if len(self.items) == MAXIMUM_STACK_SIZE-1: raise Exception("Stack overflow")
        self.items.append(value)    
    
    def pop(self):
        if len(self.items) == 0: raise Exception("Stack underflow")
        return self.items.pop()
    
    @property
    def stack(self):
        return self.items.copy()    


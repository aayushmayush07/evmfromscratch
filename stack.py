MAXIMUM_STACK_SIZE=1024


class Stack:
    def __init__(self): self.items=[]

    def __str__(self):
        def to_signed(x):
            if x >= 2**255:
                return x - 2**256
            return x

        ws = []
        for i, item in enumerate(self.items[::-1]):
            signed = to_signed(item)
            if i == 0:
                ws.append(f"{item} (signed: {signed}) <top>")
            elif i == len(self.items) - 1:
                ws.append(f"{item} (signed: {signed}) <bottom>")
            else:
                ws.append(f"{item} (signed: {signed})")
        return "\n".join(ws)

    def push(self, value): 
        if len(self.items) == MAXIMUM_STACK_SIZE-1: raise Exception("Stack overflow")
        self.items.append(value%2**256)    
    
    def pop(self):
        if len(self.items) == 0: raise Exception("Stack underflow")
        return self.items.pop()
    
    @property
    def stack(self):
        return self.items.copy()    


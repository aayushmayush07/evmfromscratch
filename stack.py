# stack.py

MAXIMUM_STACK_SIZE=1024
MOD=1<<256  # it's anoother  way of saying 2**256 chill

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
        if len(self.items) >= MAXIMUM_STACK_SIZE: raise Exception("Stack overflow")
        self.items.append(value%MOD)    
    
    def pop(self):
        if len(self.items) == 0: raise Exception("Stack underflow")
        return self.items.pop()
    
    @property
    def stack(self):
        return self.items.copy()    


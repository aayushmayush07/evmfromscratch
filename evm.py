from stack import Stack

stack=Stack()


stack.push(2)
stack.push(-4)
stack.push(3)


print(stack)


a=stack.pop()
b=stack.pop()
c=(a+b)

print(c)

stack.push(c)
print(stack)
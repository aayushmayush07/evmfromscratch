# log.py
class Log:
    def __init__(self,data,topic1=None,topic2=None,topic3=None,topic4=None):
        self.data=data
        self.topic1=topic1
        self.topic2=topic2
        self.topic3=topic3
        self.topic4=topic4



    def calc_gas(self,topic_count,size,memory_expansion_cost=0):
        return 375*topic_count+8*size+memory_expansion_cost



    def log0(self,evm):
        offset,size=evm.stack.pop(),evm.stack.pop()

        data=evm.memory.access(offset,size)
        log=Log(data)
        evm.append_log(log)

        evm.pc+=1
        evm.gas_dec(self.calc_gas(0,size))

    def log1(self,evm):
        offset, size = evm.stack.pop(), evm.stack.pop()
        topic = evm.stack.pop().value

        data = evm.memory.access(offset, size)
        log = Log(data, topic)
        evm.append_log(log)

        evm.pc += 1
        evm.gas_dec(self.calc_gas(1, size)) # TODO: memory expansion cost
    def log2(self,evm):
        offset, size = evm.stack.pop(), evm.stack.pop()
        topic1, topic2 = evm.stack.pop(), evm.stack.pop()

        data = evm.memory.access(offset, size)
        log = Log(data, topic1, topic2)
        evm.append_log(log)

        evm.pc += 1
        evm.gas_dec(self.calc_gas(2, size)) # TODO: memory expansion cost        
    def log3(self,evm):
        offset, size = evm.stack.pop(), evm.stack.pop()
        topic1 = evm.stack.pop()
        topic2 = evm.stack.pop()
        topic3 = evm.stack.pop()

        data = evm.memory.access(offset, size)
        log = Log(data, topic1, topic2, topic3)
        evm.append_log(log)

        evm.pc += 1
        evm.gas_dec(self.calc_gas(3, size)) # TODO: memory expansion cost
    def log4(self,evm):
        offset, size = evm.stack.pop(), evm.stack.pop()
        topic1 = evm.stack.pop()
        topic2 = evm.stack.pop()
        topic3 = evm.stack.pop()
        topic4 = evm.stack.pop()

        data = evm.memory.access(offset, size)
        log = Log(data, topic1, topic2, topic3, topic4)
        evm.append_log(log)

        evm.pc += 1
        evm.gas_dec(self.calc_gas(4, size)) # TODO: memory expansion cost        

    def revert(evm):
        offset, size = evm.stack.pop(), evm.stack.pop()
        evm.returndata = evm.memory.access(offset, size)

        evm.stop_flag = True
        evm.revert_flag = True
        evm.pc += 1
        evm.gas_dec(0)


# opcodes.py

UINT_256_MAX = 2**256 - 1
UINT_255_NEGATIVE_ONE = UINT_256_MAX   # alias for clarity

#Some constant for new idea of unsigned to signed
WORD_BITS = 256
MOD  = 2**256         # 2**256
SIGN = 2**255
JUMPDEST=0x5B
def to_unsigned(x: int) -> int:
    return x % MOD

def to_signed(x: int) -> int:
    return x - MOD if x >= SIGN else x


# stop

def stop(evm):
    evm.stop_flag = True   



# Math
def add(evm):
    a,b = evm.stack.pop(), evm.stack.pop()
    result = (a + b)%MOD
    evm.stack.push(result)
    evm.pc += 1
    evm.gas_dec(3)

def mul(evm):
    a,b = evm.stack.pop(), evm.stack.pop()
    result = (a * b) % MOD  
    evm.stack.push(result)
    evm.pc += 1
    evm.gas_dec(5)

def sub(evm):
    a,b = evm.stack.pop(), evm.stack.pop()
    result=(a-b)%MOD
    evm.stack.push(result)
    evm.pc += 1
    evm.gas_dec(3)    

def div(evm):  #it will give correct result for unsigned integer only so always use it when dealing with unsigned number
    a,b = evm.stack.pop(), evm.stack.pop() #no need of modulo here because div cant overflow
    result = 0 if b == 0 else a // b
    evm.stack.push(result)
    evm.pc += 1
    evm.gas_dec(5)



def sdiv(evm):
    a,b= evm.stack.pop(), evm.stack.pop()
    a, b = to_signed(a), to_signed(b)   # reinterpret inputs as signed

    if b == 0:
        result = 0
    elif a == -(2**255) and b == -1:
        result = -(2**255)  #  case accroding to yellow paper
    else:
        result = int(a / b)   # truncates toward Zeroo in Python 3

    evm.stack.push(to_unsigned(result))  # unsigned form
    evm.pc += 1
    evm.gas_dec(5)

def mod(evm):
    a,b = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(0 if b == 0 else a % b)
    evm.pc += 1
    evm.gas_dec(5)    
def smod(evm):
    a,b = evm.stack.pop(), evm.stack.pop()
    a, b = to_signed(a), to_signed(b)

    if b == 0:
        result = 0
    else:
        result = (abs(a) % abs(b)) * (1 if a >= 0 else -1)

    evm.stack.push(to_unsigned(result))
    evm.pc += 1
    evm.gas_dec(5)
def addmod(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    N = evm.stack.pop()
    result = 0 if N == 0 else (a + b) % N  #according to yellow paper 
    evm.stack.push(result)
    evm.pc += 1
    evm.gas_dec(8)
def mulmod(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    N = evm.stack.pop()
    result = 0 if N == 0 else (a * b) % N  #according to yellow paper 
    evm.stack.push(result)
    evm.pc += 1
    evm.gas_dec(8)

def size_in_bytes(number):
    import math
    if number == 0: return 1
    bits_needed = math.ceil(math.log2(abs(number) + 1))
    return math.ceil(bits_needed / 8)   

#exponent size increase when bytes increase 2**1000 cost more gas that 2**10 
def exp(evm):
    a,exponent = evm.stack.pop(), evm.stack.pop()
    result = pow(a, exponent, MOD)   # safe and efficient  
    # result= (a**exponent)%MOD  same thing but less efficient
    evm.stack.push(result)
    evm.pc += 1
    evm.gas_dec(10 + (50 * size_in_bytes(exponent)))

def signextend(evm):
    b, x = evm.stack.pop(), evm.stack.pop()
    if b <= 31:
        testbit = b * 8 + 7
        sign_bit = 1 << testbit
        if x & sign_bit: result = x | (2**256 - sign_bit)
        else           : result = x & (sign_bit - 1)
    else: result = x
    
    evm.stack.push(result)
    evm.pc += 1
    evm.gas_dec(5)    


def lt(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(1 if a < b else 0)
    evm.pc += 1
    evm.gas_dec(3)

# def unsigned_to_signed(value: int, bits: int = 256) -> int:
#     """
#     Convert unsigned int (0..2^bits-1) into signed int (-2^(bits-1)..2^(bits-1)-1)
#     using two's complement.
#     """
#     if value >= 2**(bits-1):
#         return value - 2**bits
#     else:
#         return value


def slt(evm): # signed less than
    a, b = evm.stack.pop(), evm.stack.pop()
    a = to_signed(a)
    b =to_signed(b)
    evm.stack.push(1 if a < b else 0)
    evm.pc += 1
    evm.gas_dec(3)

def gt(evm): # greater than
    a, b = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(1 if a > b else 0)
    evm.pc += 1
    evm.gas_dec(3)

def sgt(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    a = to_signed(a)
    b = to_signed(b)
    evm.stack.push(1 if a > b else 0)
    evm.pc += 1
    evm.gas_dec(3)

def eq(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(1 if a == b else 0)
    evm.pc += 1
    evm.gas_dec(3)

def iszero(evm):
    a = evm.stack.pop()
    evm.stack.push(1 if a == 0 else 0)
    evm.pc += 1
    evm.gas_dec(3)

def _and(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(a & b)
    evm.pc += 1
    evm.gas_dec(3)

def _or(evm): 
    a, b = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(a | b)
    evm.pc += 1
    evm.gas_dec(3)    
def _xor(evm): 
    a, b = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(a ^ b)
    evm.pc += 1
    evm.gas_dec(3)    

def _not(evm): 
    a = evm.stack.pop()
    evm.stack.push(~a)
    evm.pc += 1
    evm.gas_dec(3)
    


def byte(evm):
    i, x = evm.stack.pop(), evm.stack.pop()
    if i >= 32: result = 0
    else      : result = (x // pow(256, 31 - i)) % 256
    evm.stack.push(result)
    evm.pc += 1
    evm.gas_dec(3)

def shl(evm): 
    shift, value = evm.stack.pop(), evm.stack.pop()
    result=(value << shift)%MOD
    evm.stack.push(result)
    evm.pc += 1
    evm.gas_dec(3)    
def shr(evm): 
    shift, value = evm.stack.pop(), evm.stack.pop()
    result=(value >> shift)%MOD
    evm.stack.push(result)
    evm.pc += 1
    evm.gas_dec(3)    
def sar(evm):
    shift, value = evm.stack.pop(), evm.stack.pop()
    signed_val = to_signed(value)   # interpret as signed

    if shift >= 256:
        result = 0 if signed_val >= 0 else -1
    else:
        result = signed_val >> shift   # Python preserves sign on >>
    
    evm.stack.push(to_unsigned(result))
    evm.pc += 1
    evm.gas_dec(3)

def sha3(evm):
    offset, size = evm.stack.pop(), evm.stack.pop()
    value = evm.memory.access(offset, size)
    evm.stack.push(hash(str(value)))

    evm.pc += 1

    # calculate gas
    minimum_word_size = (size + 31) / 32
    dynamic_gas = 6 * minimum_word_size # TODO: + memory_expansion_cost
    evm.gas_dec(30 + dynamic_gas)    

def balance(evm):
    address = evm.stack.pop()
    evm.stack.push(99999999999)

    evm.pc += 1
    evm.gas_dec(2600) # 100 if warm    
def origin(evm):
    evm.stack.push(evm.sender)
    evm.pc += 1
    evm.gas_dec(2)    

def caller(evm):
    evm.stack.push("0x414b60745072088d013721b4a28a0559b1A9d213")
    evm.pc += 1
    evm.gas_dec(2)    

def callvalue(evm):
    evm.stack.push(evm.value)
    evm.pc += 1
    evm.gas_dec(2)    
def calldataload(evm):
    i = evm.stack.pop()

    delta = 0
    if i+32 > len(evm.calldata):
        delta = i+32 - len(evm.calldata)

    # always has to be 32 bytes
    # if its not we append 0x00 bytes until it is
    calldata = evm.calldata[i:i+32-delta]
    calldata += b"\x00"*delta

    evm.stack.push(calldata)
    evm.pc += 1
    evm.gas_dec(3)    

def calldatasize(evm):
    evm.stack.push(len(evm.calldata))
    evm.pc += 1
    evm.gas_dec(2)    
def calldatacopy(evm):
    destOffset = evm.stack.pop()
    offset = evm.stack.pop()
    size = evm.stack.pop()

    calldata = evm.calldata[offset:offset+size]
    memory_expansion_cost = evm.memory.store(destOffset, calldata) #this memory is equivalent to solidity memory, much like ram of evm

    static_gas = 3
    minimum_word_size = (size + 31) // 32
    dynamic_gas = 3 * minimum_word_size + memory_expansion_cost

    evm.gas_dec(static_gas + dynamic_gas)
    evm.pc += 1    
def codesize(evm):
    evm.stack.push(len(evm.program))
    evm.pc += 1
    evm.gas_dec(2)    


def codecopy(evm):
    destOffset = evm.stack.pop()
    offset     = evm.stack.pop()
    size       = evm.stack.pop()

    code = evm.program[offset:offset+size]
    if len(data) < size:
        data = data + b"\x00" * (size - len(data))
    memory_expansion_cost = evm.memory.store(destOffset, code)

    static_gas = 3
    minimum_word_size = (size + 31) // 32
    dynamic_gas = 3 * minimum_word_size + memory_expansion_cost

    evm.gas_dec(static_gas + dynamic_gas)
    evm.pc += 1    
def gasprice(evm):
    evm.stack.push(0x00)
    evm.pc += 1
    evm.gas_dec(2)    
def extcodesize(evm):
    address = evm.stack.pop()
    evm.stack.push(0x00)
    evm.gas_dec(2600) # 100 if warm
    evm.pc += 1    
def extcodecopy(evm):
    address    = evm.stack.pop()
    destOffset = evm.stack.pop()
    offset     = evm.stack.pop()
    size       = evm.stack.pop()

    extcode = [] # no external code
    memory_expansion_cost = evm.memory.store(destOffset, extcode)

    # refactor this in seperate method
    minimum_word_size = (size + 31) / 32
    dynamic_gas = 3 * minimum_word_size + memory_expansion_cost
    address_access_cost = 100 if warm else 2600

    evm.gas_dec(dynamic_gas + address_access_cost)
    evm.pc += 1    
def returndatasize(evm):
    evm.stack.push(0x00) # no return data
    evm.pc += 1
    evm.gas_dec(2)    

def returndatacopy(evm):
    destOffset = evm.stack.pop()
    offset     = evm.stack.pop()
    size       = evm.stack.pop()

    returndata            = evm.program[offset:offset+size]
    memory_expansion_cost = evm.memory.store(destOffset, returndata)

    minimum_word_size = (size + 31) / 32
    dynamic_gas = 3 * minimum_word_size + memory_expansion_cost

    evm.gas_dec(3 + dynamic_gas)
    evm.pc += 1   

def extcodehash(evm):
    address = evm.stack.pop()
    evm.stack.push(0x00) # no code

    evm.gas_dec(2600) # 100 if warm
    evm.pc += 1    
def blockhash(evm):
    blockNumber = evm.stack.pop()
    if blockNumber > 256: raise Exception("Only last 256 blocks can be accessed")
    evm.stack.push(0x1cbcfa1ffb1ca1ca8397d4f490194db5fc0543089b9dee43f76cf3f962a185e8)
    evm.pc += 1
    evm.gas_dec(20)    
def coinbase(evm):
    evm.stack.push(0x1cbcfa1ffb1ca1ca8397d4f490194db5fc0543089b9dee43f76cf3f962a185e8)
    evm.pc += 1
    evm.gas_dec(2)    
def _pop(evm):
    evm.pc += 1
    evm.gas_dec(2)
    evm.stack.pop(0)
def mload(evm): 
    offset = evm.stack.pop()
    value = evm.memory.load(offset)
    evm.stack.push(value)
    evm.pc += 1        
def mstore(evm): 
    # TODO: should be right aligned
    offset, value = evm.stack.pop(), evm.stack.pop()
    
    evm.memory.store(offset, value)
    evm.pc += 1    
def mstore8(evm): 
    offset, value = evm.stack.pop(), evm.stack.pop()
    evm.memory.store(offset, value & 0xFF)   #one byte only as you said, so made rest bytes 0
    evm.pc += 1    


def sload(evm):
    key=evm.stack.pop()
    warm,value=evm.storage.load(key)
    evm.stack.push(value)


    # gas cost depends on warm/cold
    if warm:
        evm.gas_dec(100)
    else:
        evm.gas_dec(2100)

    evm.pc += 1


def sstore(evm):
    key,value=evm.stack.pop(),evm.stack.pop()
    warm,old_value=evm.storage.load(key)

    base_dynamic_gas=0
    evm.storage.store(key, value)

    if value == old_value:
        base_dynamic_gas = 0
    elif old_value == 0 and value != 0:
        base_dynamic_gas = 20000
    else:
        base_dynamic_gas = 5000 

    access_cost = 100 if warm else 2100


    evm.gas_dec(base_dynamic_gas + access_cost)

    evm.pc += 1
   # TODO: do refunds    

def tload(evm):
    key = evm.stack.pop()
    warm, value = evm.tstorage.load(key)  
    evm.stack.push(value)

  
    evm.gas_dec(100 if warm else 2100)

    evm.pc += 1
def tstore(evm): 
    key, value = evm.stack.pop(), evm.stack.pop()
    warm = evm.tstorage.store(key, value)
    evm.gas_dec(100 if warm else 2100)

    evm.pc += 1

def jump(evm):
    counter = evm.stack.pop()

    # make sure that we jump to an JUMPDEST opcode
    if not evm.program[counter] == JUMPDEST:
        raise Exception("Can only jump to JUMPDEST")

    evm.pc = counter
    evm.gas_dec(8)
def jumpi(evm):
    counter, b = evm.stack.pop(), evm.stack.pop()

    if b != 0: evm.pc = counter
    else     : evm.pc += 1
    
    evm.gas_dec(10)    
def pc(evm):
    evm.stack.push(evm.pc)
    evm.pc += 1
    evm.gas_dec(2)    
def jumpdest(evm):
    evm.pc += 1
    evm.gas_dec(1)  


def _push(evm, n):
    evm.pc += 1                 
    evm.gas_dec(3)

    value = 0
    for _ in range(n):
        value = (value << 8) | evm.peek()
        evm.pc += 1

    evm.stack.push(value % MOD) # enforce 256-bit wraparound
   

def _dup(evm, n):
    # make sure stack is big enough!
    value = evm.stack[n]
    evm.stack.push(value)

    evm.pc += 1
    evm.gas_dec(3)    



def _swap(evm, n):
    # swap top (index 0) with nth item from top (index n)
    value1 = evm.stack.items[-1]       # top of stack
    value2 = evm.stack.items[-(n+1)]   # nth item (1-based)

    evm.stack.items[-1] = value2
    evm.stack.items[-(n+1)] = value1

    evm.pc += 1
    evm.gas_dec(3)    
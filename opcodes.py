# %run utils.ipynb

# import_notebooks(["utils.ipynb"])
UINT_256_MAX = 2**256 - 1
UINT_255_NEGATIVE_ONE = UINT_256_MAX   # alias for clarity

# stop

def stop(evm):
    evm.stop_flag = True   



# Math
def add(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(a+b)
    evm.pc += 1
    evm.gas_dec(3)            

def mul(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(a*b)
    evm.pc += 1
    evm.gas_dec(5)
def sub(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(a-b)
    evm.pc += 1
    evm.gas_dec(3)    

def div(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(0 if b == 0 else a // b)
    evm.pc += 1
    evm.gas_dec(5)

pos_or_neg = lambda number: -1 if number < 0 else 1    
def sdiv(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    sign = pos_or_neg(a*b)
    evm.stack.push(0 if b == 0 else sign * (abs(a) // abs(b)))
    evm.pc += 1
    evm.gas_dec(5)
def mod(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(0 if b == 0 else a % b)
    evm.pc += 1
    evm.gas_dec(5)    
def smod(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    sign = pos_or_neg(a*b)
    evm.stack.push(0 if b == 0 else abs(a) % abs(b) * sign)
    evm.pc += 1
    evm.gas_dec(5)    
def addmod(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    N = evm.stack.pop()
    evm.stack.push((a + b) % N)
    evm.pc += 1
    evm.gas_dec(8)    
def mulmod(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    N = evm.stack.pop()
    evm.stack.push((a * b) % N)
    evm.pc += 1
    evm.gas_dec(8)    
def size_in_bytes(number):
    import math
    if number == 0: return 1
    bits_needed = math.ceil(math.log2(abs(number) + 1))
    return math.ceil(bits_needed / 8)   

#exponent size increase when bytes increase 2**1000 cost more gas that 2**10 
def exp(evm):
    a, exponent = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(a ** exponent)
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

def unsigned_to_signed(value: int, bits: int = 256) -> int:
    """
    Convert unsigned int (0..2^bits-1) into signed int (-2^(bits-1)..2^(bits-1)-1)
    using two's complement.
    """
    if value >= 2**(bits-1):
        return value - 2**bits
    else:
        return value


def slt(evm): # signed less than
    a, b = evm.stack.pop(), evm.stack.pop()
    a = unsigned_to_signed(a)
    b = unsigned_to_signed(b)
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
    a = unsigned_to_signed(a)
    b = unsigned_to_signed(b)
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
    evm.stack.push(value << shift)
    evm.pc += 1
    evm.gas_dec(3)    
def shr(evm): 
    shift, value = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(value >> shift)
    evm.pc += 1
    evm.gas_dec(3)    
def sar(evm):
    shift, value = evm.stack.pop(), evm.stack.pop()
    if shift >= 256:
        result = 0 if value >= 0 else UINT_255_NEGATIVE_ONE
    else:
        result = (value >> shift) & UINT_256_MAX
        
    evm.stack.push(result)
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
    calldata += 0x00*delta

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
    memory_expansion_cost = evm.memory.store(destOffset, calldata)

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
    memory_expansion_cost = evm.memory.store(destOffset, code)

    static_gas = 3
    minimum_word_size = (size + 31) / 32
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
    evm.memory.store(offset, value)
    evm.pc += 1    
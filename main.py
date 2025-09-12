from evm import EVM
from bytecodes import *




GAS=21_000

# evm=EVM(SIMPLE_ADD,GAS,0)
# evm=EVM(SIMPLE_SUB,GAS,0)
# evm=EVM(SIMPLE_MUL,GAS,0)
# evm=EVM(SIMPLE_DIV,GAS,0)
evm=EVM(SIMPLE_EXP,GAS,0)

evm.run()


print(evm.stack)


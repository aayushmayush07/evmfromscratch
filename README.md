EVM From Scratch 🛠️

An  Python implementation of the Mini Ethereum Virtual Machine (EVM), built from scratch.
The goal is to deeply understand how EVM opcodes, stack, memory, and storage interact by re-implementing them in Python.



Features

Stack-based architecture (stack.py)

Memory & persistent storage models (simpleMemory.py, keyvaluestorage.py, keyvalueTransientStorage.py)

Opcode implementations (opcodes.py) mapped to names (opnames.py)

Execution engine (evm.py) with gas accounting

Logging system (log.py)

Pre-built bytecode test cases (bytecodes.py) for math ops, overflow/underflow, signed division, exponentiation, addmod, etc.

Example runner (main.py) to load programs and inspect results.



📂 Project Structure
.
├── main.py                 # Entry point (loads EVM with a test program)
├── evm.py                  # EVM execution engine
├── evmstate.py             # Alternative state container
├── opcodes.py              # All opcode implementations
├── opnames.py              # Opcode → byte mappings
├── bytecodes.py            # Test bytecode cases
├── stack.py                # Stack implementation
├── simpleMemory.py         # Memory implementation
├── keyvaluestorage.py      # Persistent storage
├── keyvalueTransientStorage.py # Transient storage (cleared each tx)
├── log.py                  # LOG opcodes & gas calculation
        




▶️ Running

Clone the repo:

git clone https://github.com/aayushmayush07/evmfromscratch
cd evmfromscratch


Run an example test program:

python3 main.py


By default, main.py runs SIMPLE_ADD.
To test something else, edit main.py and pick any bytecode from bytecodes.py, for example:

# main.py
from evm import EVM
from bytecodes import SIMPLE_ADD, DIV_BY_ZERO

evm = EVM(SIMPLE_ADD, gas=21000, value=0)
evm.run()
print(evm.stack)

🧪 Example Bytecode Tests

Defined in bytecodes.py
:

SIMPLE_ADD → 66 + 255 = 321

ADD_OVERFLOW → (2^256 – 1 + 1) mod 2^256 = 0

SUB_UNDERFLOW → 15 – 255 = -240 mod 2^256

MUL_BIG_SMALL → (2^256 – 1) * 2 = 2^256 – 2

SDIV_NEG_POS → (-1) / 5 = 0 (truncates toward zero)

EXP_OVERFLOW → 2^255 mod 2^256

ADDMOD_OVERFLOW_10 → (1 + (2^256 – 1)) % 10 = 6

🎯 Purpose

This project is not about performance — it’s a learning tool.
It’s meant to help developers understand:

How the EVM executes bytecode

Gas consumption per instruction

Edge cases like overflows, signed math, division by zero

The stack/memory/storage model
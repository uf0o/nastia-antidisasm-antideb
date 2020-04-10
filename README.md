# nastia antidisasm/antidebug techniques

## nastia_antideb - A portable x64 universal antidebugger

What it does:
- Enable the Trap Flag for x64 processes 
- Take decision based on debugger presence.
- Template for x64 + intergrate MASM
 
## nastia_antidis - A tiny but effective ELF anti-disassembler

| inspired by the original work from 'liveoverflow'|

What it does:
- Swap one byte a time from the target ELF binary and generate a fuzzed copy of it.
- Verify that the fuzzed behavior is consistent with the original one.
- If so, each fuzzed copy is loaded into GDB and verified if it gets recognized
 
todo:

- Add exitstatus code monitoring instead of relying on program output
- Add r2 support
- Add incremental byte mutation 

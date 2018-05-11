# nastia_antidebugger
A tiny but effective ELF antidebugger

| inspired by the original work from 'liveoverflow'|

What it does:
- Swap one byte a time from the tested ELF binary and generate a fuzzed binary copy, while checking if gdb is still able to load it without headers.

todo:

- Add exitstatus code monitoring instead of relying on program output
- Add gdb and r2 error code instead of output

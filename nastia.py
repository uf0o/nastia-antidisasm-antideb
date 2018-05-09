# TO DO: verify gdb output and skip if tail fuzz_gdb has assembly lines in it....so 
# - convert to python3
# convert to popenprocess instaed of system

# this program flips a random byte in the binary and verify that both gdb and radare2 are no longer able to load symbols
import optparse
import random
import os
import sys 
import subprocess
import filecmp
import time

current_dir = os.getcwd()
parser = optparse.OptionParser()

parser.add_option('-v', '--verbose',
                  dest='verbose',
                  default=False,
                  action="store_true",
                  help="make lots of noise [optional]")

parser.add_option("-e", '--executable', 
				  dest='binary', 
				  default=False,
				  action="store",
				  type="str",
	              help="the name of the ELF binary file to be fuzzed",)

options, remainder = parser.parse_args()
if not options.binary:
	print("\nWARNING: filename missing:\n")
	parser.print_help()
	sys.exit()

# copies the target binary to a temp fuzzing version
original_bin = options.binary
fuzzed_name  = original_bin+"fuzz"
fuzzed_bin   = current_dir+str(original_bin+"fuzz")

print("original filename is {0}".format(original_bin))
print("fuzzed filename is {0}".format(original_bin+"fuzz"))

subprocess.call(["cp","-p","--preserve",original_bin, fuzzed_name])

def flip_byte(in_bytes):
	i = random.randint(0,len(in_bytes))
	a = random.randint(0,255)
	single_byte = a.to_bytes(1, byteorder='little', signed=False) 
	return in_bytes[:i]+single_byte+in_bytes[i+1:]

# open the original binary and the fuzzing one
def copy_binary(file1, file2):
	with open(file1, "rb") as orig_f, open(file2, "wb") as new_f:
		new_f.write(flip_byte(orig_f.read()))

# check binaries outputs 
def check_output():
	with open('out-original', 'w+') as f1:
		subprocess.Popen(original_bin, stdout=f1,cwd=current_dir)
	with open('out-fuzzed', 'w+') as f2:
		subprocess.Popen(fuzzed_bin, stdout=f2, cwd=current_dir)
	time.sleep(0.1)
	return(filecmp.cmp('out-original', 'out-fuzzed',shallow=False))

# check if gdb works with the fuzzed binary
def check_gdb():
	cmd1 = "echo disassemble main | gdb " + fuzzed_bin +    " > fuzz_gdb"
	cmd2 = "echo disassemble main | gdb " + original_bin + " > orig_gdb"
	subprocess.Popen([cmd1],shell=True)
	subprocess.Popen([cmd2],shell=True)
	time.sleep(0.1)
	return(filecmp.cmp('orig_gdb', 'fuzz_gdb',shallow=False))

# check if radare works with the fuzzed binary
def check_radare():
	cmd1 = "echo -e 'aaa\ns sym.main\npdf' | radare2 " + fuzzed_bin + " > fuzz_radare"
	cmd2 =  "echo -e 'aaa\ns sym.main\npdf' | radare2 " + original_bin + " > orig_radare"
	subprocess.Popen([cmd1],shell=True)
	subprocess.Popen([cmd2],shell=True)
	time.sleep(0.1)
	return(filecmp.cmp('orig_radare', 'fuzz_radare',shallow=False))

while True:
	copy_binary(original_bin, fuzzed_name)
	if check_output() and not check_gdb() and not check_radare():
		print("FOUND POSSIBLE FAIL\n\n\n")
		os.system("tail fuzz_gdb")
		input()

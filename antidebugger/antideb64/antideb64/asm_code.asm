
_TEXT	SEGMENT
 
PUBLIC trap_64
 
trap_64 PROC
	 pushf
     xor rax,rax
     mov rax, 100
     or [rsp], rax
     popf
trap_64 ENDP
 
_TEXT	ENDS
END

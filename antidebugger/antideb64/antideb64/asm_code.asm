_TEXT	SEGMENT
 
PUBLIC trap_64
 
trap_64 PROC
	 pushfq
     or qword ptr[rsp], 100h
     popfq
     ret
trap_64 ENDP
 
_TEXT	ENDS
END 
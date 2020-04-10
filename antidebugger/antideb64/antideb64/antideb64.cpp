#include <SDKDDKVer.h>
#include <stdio.h>
#include <Windows.h>
#include <iostream>

extern "C"
{
    void trap_64();
};


int main(int argc, char* argv[])
{
    system("PAUSE");
    BOOL bExceptionHit = FALSE;
    __try
    {
        trap_64();
    }
    __except (EXCEPTION_EXECUTE_HANDLER)
    {
        bExceptionHit = TRUE;

    }
    if (bExceptionHit == FALSE)
        printf("A debugger is present!\n");
    else
        printf("No debugger is present!\n");

}
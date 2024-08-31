** 
* A minimal program for Atari ST.
*
* Just a call to Pterm0() to terminate immediately.
* 

                move.w  #0,-(sp) ; GEMDOS function code 0 = Pterm0()
                trap    #1      ; Call GEMDOS
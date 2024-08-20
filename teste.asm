
L1: 
L2:
L3:
      add $t0, $s1, $s2 # testes :
    bne $t0, $t1, L1
    mul $t0, $s1, $s2 
    div $t0, $s1
LG: 
   or $t0, $s1, $s2 
   and $t0, $s1, $s2
   bne $t0, $t1, L3
L4:
   sll $t0, $s1, 2
L5:
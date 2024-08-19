L1: add $t0, $s1, $s2 # testes :
L2:   addi $t1, $s3, 7
      beq $t0, $t1, L1
      j L2 # arroz beq

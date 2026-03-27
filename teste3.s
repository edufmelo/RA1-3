.global _start

.data
    .align 3
    const_3_14: .double 3.14
    .align 3
    const_2: .double 2
    .align 3
    const_1_0: .double 1.0
    .align 3
    const_5: .double 5
    .align 3
    const_10: .double 10
    .align 3
    const_3_5: .double 3.5
    .align 3
    const_2_5: .double 2.5
    .align 3
    const_14_25: .double 14.25
    .align 3
    const_20: .double 20
    .align 3
    const_4: .double 4
    .align 3
    mem_MEM: .double 0.0
    .align 3
    const_1_5: .double 1.5
    .align 3
    mem_X: .double 0.0
    .align 3
    resultados: .space 800       @ espaco para 100 doubles
    numResultados: .word 0

.text
_start:

    @ Linha 1
linha1:
    LDR R4, =const_3_14
    VLDR D0, [R4]        @ carrega double 3.14
    LDR R4, =const_2
    VLDR D1, [R4]        @ carrega double 2
    VADD.F64 D2, D0, D1    @ D0 + D1
    @ Armazena resultado no historico
    LDR R0, =numResultados
    LDR R1, [R0]                @ R1 = numResultados atual
    LDR R2, =resultados
    LSL R3, R1, #3              @ offset = R1 * 8 (double = 8 bytes)
    ADD R2, R2, R3
    VSTR D2, [R2]               @ guarda resultado no array
    ADD R1, R1, #1
    STR R1, [R0]                @ numResultados++

    @ Linha 2
linha2:
    LDR R4, =const_3_14
    VLDR D0, [R4]        @ carrega double 3.14
    LDR R4, =const_2
    VLDR D1, [R4]        @ carrega double 2
    VSUB.F64 D2, D0, D1    @ D0 - D1
    @ Armazena resultado no historico
    LDR R0, =numResultados
    LDR R1, [R0]                @ R1 = numResultados atual
    LDR R2, =resultados
    LSL R3, R1, #3              @ offset = R1 * 8 (double = 8 bytes)
    ADD R2, R2, R3
    VSTR D2, [R2]               @ guarda resultado no array
    ADD R1, R1, #1
    STR R1, [R0]                @ numResultados++

    @ Linha 3
linha3:
    LDR R4, =const_3_14
    VLDR D0, [R4]        @ carrega double 3.14
    LDR R4, =const_2
    VLDR D1, [R4]        @ carrega double 2
    VMUL.F64 D2, D0, D1    @ D0 * D1
    @ Armazena resultado no historico
    LDR R0, =numResultados
    LDR R1, [R0]                @ R1 = numResultados atual
    LDR R2, =resultados
    LSL R3, R1, #3              @ offset = R1 * 8 (double = 8 bytes)
    ADD R2, R2, R3
    VSTR D2, [R2]               @ guarda resultado no array
    ADD R1, R1, #1
    STR R1, [R0]                @ numResultados++

    @ Linha 4
linha4:
    LDR R4, =const_3_14
    VLDR D0, [R4]        @ carrega double 3.14
    LDR R4, =const_2
    VLDR D1, [R4]        @ carrega double 2
    VDIV.F64 D2, D0, D1    @ D0 / D1
    @ Armazena resultado no historico
    LDR R0, =numResultados
    LDR R1, [R0]                @ R1 = numResultados atual
    LDR R2, =resultados
    LSL R3, R1, #3              @ offset = R1 * 8 (double = 8 bytes)
    ADD R2, R2, R3
    VSTR D2, [R2]               @ guarda resultado no array
    ADD R1, R1, #1
    STR R1, [R0]                @ numResultados++

    @ Linha 5
linha5:
    LDR R4, =const_3_14
    VLDR D0, [R4]        @ carrega double 3.14
    LDR R4, =const_2
    VLDR D1, [R4]        @ carrega double 2
    @ divisao inteira: D0 // D1
    VDIV.F64 D2, D0, D1
    VCVT.S32.F64 S31, D2    @ trunca para inteiro em temp S31
    VCVT.F64.S32 D2, S31    @ volta para double
    @ Armazena resultado no historico
    LDR R0, =numResultados
    LDR R1, [R0]                @ R1 = numResultados atual
    LDR R2, =resultados
    LSL R3, R1, #3              @ offset = R1 * 8 (double = 8 bytes)
    ADD R2, R2, R3
    VSTR D2, [R2]               @ guarda resultado no array
    ADD R1, R1, #1
    STR R1, [R0]                @ numResultados++

    @ Linha 6
linha6:
    LDR R4, =const_3_14
    VLDR D0, [R4]        @ carrega double 3.14
    LDR R4, =const_2
    VLDR D1, [R4]        @ carrega double 2
    @ resto: D0 % D1
    VDIV.F64 D2, D0, D1    @ quociente double
    VCVT.S32.F64 S31, D2    @ trunca para inteiro em temp S31
    VCVT.F64.S32 D2, S31    @ quociente inteiro como double
    VMUL.F64 D2, D2, D1    @ quociente * divisor
    VSUB.F64 D2, D0, D2    @ resto = dividendo - quociente * divisor
    @ Armazena resultado no historico
    LDR R0, =numResultados
    LDR R1, [R0]                @ R1 = numResultados atual
    LDR R2, =resultados
    LSL R3, R1, #3              @ offset = R1 * 8 (double = 8 bytes)
    ADD R2, R2, R3
    VSTR D2, [R2]               @ guarda resultado no array
    ADD R1, R1, #1
    STR R1, [R0]                @ numResultados++

    @ Linha 7
linha7:
    LDR R4, =const_3_14
    VLDR D0, [R4]        @ carrega double 3.14
    LDR R4, =const_2
    VLDR D1, [R4]        @ carrega double 2
    @ potenciacao: D0 ^ D1 (loop com VMUL)
    VCVT.S32.F64 S31, D1
    VMOV R0, S31              @ R0 = expoente (inteiro)
    @ inicializa resultado com 1.0
    LDR R4, =const_1_0
    VLDR D2, [R4]    @ resultado = 1.0
potencia0:
    CMP R0, #0
    BLE potencia0_fim
    VMUL.F64 D2, D2, D0
    SUB R0, R0, #1
    B potencia0
potencia0_fim:
    @ Armazena resultado no historico
    LDR R0, =numResultados
    LDR R1, [R0]                @ R1 = numResultados atual
    LDR R2, =resultados
    LSL R3, R1, #3              @ offset = R1 * 8 (double = 8 bytes)
    ADD R2, R2, R3
    VSTR D2, [R2]               @ guarda resultado no array
    ADD R1, R1, #1
    STR R1, [R0]                @ numResultados++

    @ Linha 8
linha8:
    LDR R4, =const_5
    VLDR D0, [R4]        @ carrega double 5
    LDR R4, =const_10
    VLDR D1, [R4]        @ carrega double 10
    VMUL.F64 D2, D0, D1    @ D0 * D1
    LDR R4, =const_2
    VLDR D3, [R4]        @ carrega double 2
    LDR R4, =const_5
    VLDR D4, [R4]        @ carrega double 5
    VMUL.F64 D5, D3, D4    @ D3 * D4
    VDIV.F64 D6, D2, D5    @ D2 / D5
    @ Armazena resultado no historico
    LDR R0, =numResultados
    LDR R1, [R0]                @ R1 = numResultados atual
    LDR R2, =resultados
    LSL R3, R1, #3              @ offset = R1 * 8 (double = 8 bytes)
    ADD R2, R2, R3
    VSTR D6, [R2]               @ guarda resultado no array
    ADD R1, R1, #1
    STR R1, [R0]                @ numResultados++

    @ Linha 9
linha9:
    LDR R4, =const_3_5
    VLDR D0, [R4]        @ carrega double 3.5
    LDR R4, =const_2_5
    VLDR D1, [R4]        @ carrega double 2.5
    VMUL.F64 D2, D0, D1    @ D0 * D1
    LDR R4, =const_14_25
    VLDR D3, [R4]        @ carrega double 14.25
    VADD.F64 D4, D2, D3    @ D2 + D3
    @ Armazena resultado no historico
    LDR R0, =numResultados
    LDR R1, [R0]                @ R1 = numResultados atual
    LDR R2, =resultados
    LSL R3, R1, #3              @ offset = R1 * 8 (double = 8 bytes)
    ADD R2, R2, R3
    VSTR D4, [R2]               @ guarda resultado no array
    ADD R1, R1, #1
    STR R1, [R0]                @ numResultados++

    @ Linha 10
linha10:
    LDR R4, =const_10
    VLDR D0, [R4]        @ carrega double 10
    LDR R4, =const_20
    VLDR D1, [R4]        @ carrega double 20
    VMUL.F64 D2, D0, D1    @ D0 * D1
    LDR R4, =const_2
    VLDR D3, [R4]        @ carrega double 2
    LDR R4, =const_5
    VLDR D4, [R4]        @ carrega double 5
    VMUL.F64 D5, D3, D4    @ D3 * D4
    VDIV.F64 D6, D2, D5    @ D2 / D5
    @ Armazena resultado no historico
    LDR R0, =numResultados
    LDR R1, [R0]                @ R1 = numResultados atual
    LDR R2, =resultados
    LSL R3, R1, #3              @ offset = R1 * 8 (double = 8 bytes)
    ADD R2, R2, R3
    VSTR D6, [R2]               @ guarda resultado no array
    ADD R1, R1, #1
    STR R1, [R0]                @ numResultados++

    @ Linha 11
linha11:
    LDR R4, =const_4
    VLDR D0, [R4]        @ carrega double 4
    @ RES: acessa resultado anterior
    VCVT.S32.F64 S31, D0
    VMOV R0, S31              @ R0 = N
    LDR R1, =resultados
    LDR R2, =numResultados
    LDR R2, [R2]
    SUB R2, R2, R0              @ indice = total - N
    LSL R2, R2, #3              @ offset em bytes (double = 8)
    ADD R1, R1, R2
    VLDR D1, [R1]
    @ Armazena resultado no historico
    LDR R0, =numResultados
    LDR R1, [R0]                @ R1 = numResultados atual
    LDR R2, =resultados
    LSL R3, R1, #3              @ offset = R1 * 8 (double = 8 bytes)
    ADD R2, R2, R3
    VSTR D1, [R2]               @ guarda resultado no array
    ADD R1, R1, #1
    STR R1, [R0]                @ numResultados++

    @ Linha 12
linha12:
    LDR R4, =const_2
    VLDR D0, [R4]        @ carrega double 2
    @ RES: acessa resultado anterior
    VCVT.S32.F64 S31, D0
    VMOV R0, S31              @ R0 = N
    LDR R1, =resultados
    LDR R2, =numResultados
    LDR R2, [R2]
    SUB R2, R2, R0              @ indice = total - N
    LSL R2, R2, #3              @ offset em bytes (double = 8)
    ADD R1, R1, R2
    VLDR D1, [R1]
    @ Armazena resultado no historico
    LDR R0, =numResultados
    LDR R1, [R0]                @ R1 = numResultados atual
    LDR R2, =resultados
    LSL R3, R1, #3              @ offset = R1 * 8 (double = 8 bytes)
    ADD R2, R2, R3
    VSTR D1, [R2]               @ guarda resultado no array
    ADD R1, R1, #1
    STR R1, [R0]                @ numResultados++

    @ Linha 13
linha13:
    LDR R0, =mem_MEM        @ load de MEM
    VLDR D0, [R0]
    @ Armazena resultado no historico
    LDR R0, =numResultados
    LDR R1, [R0]                @ R1 = numResultados atual
    LDR R2, =resultados
    LSL R3, R1, #3              @ offset = R1 * 8 (double = 8 bytes)
    ADD R2, R2, R3
    VSTR D0, [R2]               @ guarda resultado no array
    ADD R1, R1, #1
    STR R1, [R0]                @ numResultados++

    @ Linha 14
linha14:
    LDR R4, =const_10
    VLDR D0, [R4]        @ carrega double 10
    LDR R0, =mem_MEM        @ store em MEM
    VSTR D0, [R0]

    @ Linha 15
linha15:
    LDR R4, =const_1_5
    VLDR D0, [R4]        @ carrega double 1.5
    LDR R0, =mem_X        @ store em X
    VSTR D0, [R0]

    @ Linha 16
linha16:
    LDR R0, =mem_MEM        @ load de MEM
    VLDR D0, [R0]
    @ Armazena resultado no historico
    LDR R0, =numResultados
    LDR R1, [R0]                @ R1 = numResultados atual
    LDR R2, =resultados
    LSL R3, R1, #3              @ offset = R1 * 8 (double = 8 bytes)
    ADD R2, R2, R3
    VSTR D0, [R2]               @ guarda resultado no array
    ADD R1, R1, #1
    STR R1, [R0]                @ numResultados++

    @ Linha 17
linha17:
    LDR R0, =mem_X        @ load de X
    VLDR D0, [R0]
    @ Armazena resultado no historico
    LDR R0, =numResultados
    LDR R1, [R0]                @ R1 = numResultados atual
    LDR R2, =resultados
    LSL R3, R1, #3              @ offset = R1 * 8 (double = 8 bytes)
    ADD R2, R2, R3
    VSTR D0, [R2]               @ guarda resultado no array
    ADD R1, R1, #1
    STR R1, [R0]                @ numResultados++

    @ Linha 18
linha18:
    LDR R0, =mem_MEM        @ load de MEM
    VLDR D0, [R0]
    LDR R4, =const_4
    VLDR D1, [R4]        @ carrega double 4
    @ RES: acessa resultado anterior
    VCVT.S32.F64 S31, D1
    VMOV R0, S31              @ R0 = N
    LDR R1, =resultados
    LDR R2, =numResultados
    LDR R2, [R2]
    SUB R2, R2, R0              @ indice = total - N
    LSL R2, R2, #3              @ offset em bytes (double = 8)
    ADD R1, R1, R2
    VLDR D2, [R1]
    VADD.F64 D3, D0, D2    @ D0 + D2
    @ Armazena resultado no historico
    LDR R0, =numResultados
    LDR R1, [R0]                @ R1 = numResultados atual
    LDR R2, =resultados
    LSL R3, R1, #3              @ offset = R1 * 8 (double = 8 bytes)
    ADD R2, R2, R3
    VSTR D3, [R2]               @ guarda resultado no array
    ADD R1, R1, #1
    STR R1, [R0]                @ numResultados++

    @ Fim do programa
fim:
    B fim

"""
Alunos: 
- Daniel de Almeida Santos Bina
- Eduardo Ferreira de Melo
- João Eduardo Faccin Leineker
Grupo: RA1 3
"""

import sys

# Como nos slides (Aula 04), contudo, de forma mais simples com tipo e valor
class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo    # o tipo do token (NUMERO, OPERADOR, PARENTESE, IDENTIFICADOR, KEYWORD, ERRO)
        self.valor = valor  # o texto original do token (ex: '3.14', '+', 'RES')

    def __repr__(self): # útil para realizarmos testes - debug (remover ao final)
        return "Token(" + self.tipo + ", '" + self.valor + "')"

# Lê o arquivo de entrada e armazena cada linha na lista 'linhas'
def lerArquivo(nomeArquivo, linhas):
    try:
        arquivo = open(nomeArquivo, 'r')
        
        for linha in arquivo:
            linhaLimpada = linha.strip() # Limpa espaços em branco no início e fim da linha
       
            if linhaLimpada != '': # Ignora linhas vazias
                linhas.append(linhaLimpada) 
        
        arquivo.close()
    
    except FileNotFoundError: # Se o arquivo não for encontrado
        print("Erro: arquivo '" + nomeArquivo + "' nao encontrado.")
    
    except Exception as e: # Se ocorrer outro erro
        print("Erro ao ler arquivo: " + str(e))

# Deve analisar uma linha de expressão RPN e extrair tokens - age como estado inicial do AFD
def parseExpressao(linha, vetorTokens):
    pos = 0 
    while pos < len(linha):  
        char = linha[pos]
        
        if char == ' ' or char == '\t':  # Ignora espaços ou tab
            pos += 1
        elif char.isdigit() or char == '.':
            pos = estadoNumero(linha, pos, vetorTokens)
        elif char == '-':
            # Olha o último token para decidir se é operador ou número negativo
            ultimoToken = vetorTokens[-1] if len(vetorTokens) > 0 else None

            if ultimoToken is None or ultimoToken.tipo == "ABRE_PAREN" or ultimoToken.tipo == "OPERADOR":
                # Ex: (-2.0 3.0 +) ou (3.0 -2.0 +) -> número negativo
                pos = estadoNumero(linha, pos, vetorTokens)
            else:
                # Ex: (3.0 2.0 -) → operador de subtração
                pos = estadoOperador(linha, pos, vetorTokens)
        elif char in '+*/%^':
            pos = estadoOperador(linha, pos, vetorTokens)
        elif char in '()':  # Implementação separada dos Identificadores para melhor organização
            pos = estadoParenteses(linha, pos, vetorTokens)
        elif char.isalpha(): 
            pos = estadoIdentificador(linha, pos, vetorTokens)
        else:
            pos = estadoErro(linha, pos, vetorTokens)

def estadoNumero(linha, pos, tokens):
    textoNumero = ""
    qtdePontos = 0
    
    # Aceita sinal negativo no início
    if pos < len(linha) and linha[pos] == '-':
        textoNumero += '-'
        pos += 1
    
    while pos < len(linha) and (linha[pos].isdigit() or linha[pos] == '.'):
        if linha[pos] == '.':
            qtdePontos += 1

        # Armazena e soma cada caractere (número ou ponto)
        textoNumero += linha[pos]
        pos += 1

    # Verifica se o número é válido (pode ter até 1 ponto)
    if qtdePontos <= 1:
        novoToken = Token("NUMERO", textoNumero)
    else:
        novoToken = Token("ERRO", "Numero malformado: " + textoNumero)

    tokens.append(novoToken)
    
    return pos

def estadoOperador(linha, pos, tokens):
    char = linha[pos] # Caracter exato que o analisador esta lendo agora
    
    #Verifica se é divisão inteira //
    if char == '/' and pos + 1 < len(linha) and linha[pos + 1] == '/':
        novoToken = Token("OPERADOR", "//")
        tokens.append(novoToken)
        return pos + 2  # avança 2 caracteres
    
    # Instanciamos a classe Token com o tipo OPERADOR e o valor
    # (Mesma lógica para demais funções)
    novoToken = Token("OPERADOR", char)    
    tokens.append(novoToken)
    
    return pos + 1

def estadoParenteses(linha, pos, tokens):
    char = linha[pos]
    
    if char == '(':
        novoToken = Token("ABRE_PAREN", char)
    else:
        novoToken = Token("FECHA_PAREN", char)   
        
    tokens.append(novoToken)
    return pos + 1
    
def estadoIdentificador(linha, pos, tokens):  # para RES, MEM, VAR, etc.
    textoId = ""
    
    # Roda enquanto o caractere atual for uma letra do alfabeto
    while pos < len(linha) and linha[pos].isalpha():
        textoId += linha[pos]
        pos += 1
        
    if textoId == "RES":
        # A única keyword da linguagem nesta fase
        novoToken = Token("KEYWORD", textoId)
    
    elif textoId.isupper():
        # Variável de memória (MEM, X, VAR), se todas maiúsculas
        novoToken = Token("MEMORIA", textoId)
        
    else:
        # Digitar letras minúsculas é inválido
        novoToken = Token("ERRO", "Identificador malformado (use maiusculas): " + textoId)
        
    tokens.append(novoToken)
    return pos

# Numeros malformados, tokens inválidos
def estadoErro(linha, pos, tokens):
    charInvalido = linha[pos]
    novoToken = Token("ERRO", "Caractere invalido: " + charInvalido)
    tokens.append(novoToken)

    return pos + 1

# Avalia as expressões RPN (pilha) e gerencia memoria/RES
def executarExpressao(tokens, resultados, memoria):
    pilha = []
    i = 0

    while i < len(tokens):
        token = tokens[i]

        # Ignora parênteses - estrutura já capturada pela ordem dos tokens
        if token.tipo in ("ABRE_PAREN", "FECHA_PAREN"):
            i += 1

        # Empilha número
        elif token.tipo == "NUMERO":
            pilha.append(float(token.valor))
            i += 1

        # Operações aritméticas
        elif token.tipo == "OPERADOR":
            # Verifica se há operandos suficientes
            if len(pilha) < 2:
                print("Erro: operandos insuficientes para operador '" + token.valor + "'")
                return None

            b = pilha.pop()  # segundo operando
            a = pilha.pop()  # primeiro operando

            if token.valor == "+":
                pilha.append(a + b)

            elif token.valor == "-":
                pilha.append(a - b)

            elif token.valor == "*":
                pilha.append(a * b)

            elif token.valor == "/":
                if b == 0:
                    print("Erro: divisao por zero")
                    return None
                pilha.append(a / b)

            elif token.valor == "//":
                if b == 0:
                    print("Erro: divisao inteira por zero")
                    return None
                pilha.append(float(int(a) // int(b)))

            elif token.valor == "%":
                if b == 0:
                    print("Erro: resto por zero")
                    return None
                pilha.append(float(int(a) % int(b)))

            elif token.valor == "^":
                pilha.append(float(a ** int(b)))

            i += 1

        # Comando (MEM) ou (V MEM)
        elif token.tipo == "MEMORIA":
            nomeMem = token.valor

            if len(pilha) > 0:
                # Há valor na pilha → store: (V MEM)
                memoria[nomeMem] = pilha.pop()
            else:
                # Pilha vazia → load: (MEM)
                if nomeMem in memoria:
                    pilha.append(memoria[nomeMem])
                else:
                    print("Aviso: memoria '" + nomeMem + "' nao inicializada, usando 0.0")
                    pilha.append(0.0)

            i += 1

        # Comando (N RES)
        elif token.tipo == "KEYWORD" and token.valor == "RES":
            # O número N deve estar na pilha (empilhado antes do RES)
            if len(pilha) < 1:
                print("Erro: falta o valor N para RES")
                return None

            n = int(pilha.pop())
            indice = len(resultados) - n

            if indice < 0 or indice >= len(resultados):
                print("Erro: RES(" + str(n) + ") fora do historico disponivel")
                return None

            pilha.append(resultados[indice])
            i += 1

        # Token de erro detectado pelo lexer
        elif token.tipo == "ERRO":
            print("Erro lexico: " + token.valor)
            return None

        else:
            i += 1

    # Ao final, o topo da pilha é o resultado
    if len(pilha) == 1:
        resultado = pilha[0]
        resultados.append(resultado)
        return resultado
    elif len(pilha) == 0:
        # Expressão de store (V MEM) não deixa resultado na pilha
        return None
    else:
        print("Erro: pilha com multiplos valores ao final - expressao mal formada")
        return None

def resolverAninhamento(tokens):
    # Retorna uma lista de grupos de tokens por nível de aninhamento
    # Útil para a gerarAssembly saber a ordem de avaliação
    pilhaGrupos = []
    grupoAtual = []
    grupos = []

    for token in tokens:
        if token.tipo == "ABRE_PAREN":
            pilhaGrupos.append(grupoAtual)
            grupoAtual = []
        elif token.tipo == "FECHA_PAREN":
            grupos.append(grupoAtual)
            grupoAtual = pilhaGrupos.pop()
        else:
            grupoAtual.append(token)

    return grupos

# Gera codigo Assembly ARMv7 (VFP)
def gerarAssembly(listaTokens, codigoAssembly):
    secaoDados = []            # linhas da secao .data (constantes e variaveis)
    secaoTexto = []            # linhas da secao .text (instrucoes)
    contadorLabel = 0          # contador de labels para loops (potenciacao)
    labelsMemoria = set()      # labels de memoria ja criadas no .data
    constantesUsadas = {}      # mapeia valor -> nome do label (deduplicacao)

    for numLinha, tokens in enumerate(listaTokens):
        grupos = resolverAninhamento(tokens)
        pilhaRegistradores = []
        contadorRegistrador = 0    # reseta por expressao (D0, D1, ...)

        # Verifica se ha tokens de erro nesta expressao
        temErro = any(t.tipo == "ERRO" for t in tokens)
        if temErro:
            secaoTexto.append("")
            secaoTexto.append("    @ Linha " + str(numLinha) + " - IGNORADA (erro lexico)")
            continue

        secaoTexto.append("")
        secaoTexto.append("    @ Linha " + str(numLinha))
        secaoTexto.append("linha" + str(numLinha) + ":")

        for grupo in grupos:
            for token in grupo:
                # Numero: carrega constante de 64 bits
                if token.tipo == "NUMERO":
                    valorNumero = token.valor

                    # Deduplicacao: reutiliza label se o valor ja foi declarado
                    if valorNumero in constantesUsadas:
                        nomeConst = constantesUsadas[valorNumero]
                    else:
                        if valorNumero.startswith('-'):
                            sufixo = "neg"
                            valorLimpo = valorNumero[1:]
                        else:
                            sufixo = "pos"
                            valorLimpo = valorNumero

                        valorLabel = valorLimpo.replace('.', '_')
                        nomeConst = "const_" + valorLabel + "_" + sufixo
                        constantesUsadas[valorNumero] = nomeConst
                        secaoDados.append("    .align 3")
                        secaoDados.append("    " + nomeConst + ": .double " + valorNumero)

                    nomeReg = "D" + str(contadorRegistrador)
                    contadorRegistrador += 1
                    secaoTexto.append("    LDR R4, =" + nomeConst)
                    secaoTexto.append("    VLDR " + nomeReg + ", [R4]        @ carrega double " + valorNumero)
                    pilhaRegistradores.append(nomeReg)

                # Operador: desempilha 2 registradores, opera, empilha resultado
                elif token.tipo == "OPERADOR":
                    if len(pilhaRegistradores) < 2:
                        secaoTexto.append("    @ ERRO: operandos insuficientes para '" + token.valor + "'")
                        continue

                    regB = pilhaRegistradores.pop()
                    regA = pilhaRegistradores.pop()
                    regResultado = "D" + str(contadorRegistrador)
                    contadorRegistrador += 1

                    if token.valor == "+":
                        secaoTexto.append("    VADD.F64 " + regResultado + ", " + regA + ", " + regB + "    @ " + regA + " + " + regB)

                    elif token.valor == "-":
                        secaoTexto.append("    VSUB.F64 " + regResultado + ", " + regA + ", " + regB + "    @ " + regA + " - " + regB)

                    elif token.valor == "*":
                        secaoTexto.append("    VMUL.F64 " + regResultado + ", " + regA + ", " + regB + "    @ " + regA + " * " + regB)

                    elif token.valor == "/":
                        secaoTexto.append("    VDIV.F64 " + regResultado + ", " + regA + ", " + regB + "    @ " + regA + " / " + regB)

                    elif token.valor == "//":
                        secaoTexto.append("    @ divisao inteira: " + regA + " // " + regB)
                        secaoTexto.append("    VDIV.F64 " + regResultado + ", " + regA + ", " + regB)
                        secaoTexto.append("    VCVT.S32.F64 S31, " + regResultado + "    @ trunca para inteiro em temp S31")
                        secaoTexto.append("    VCVT.F64.S32 " + regResultado + ", S31    @ volta para double")

                    elif token.valor == "%":
                        secaoTexto.append("    @ resto: " + regA + " % " + regB)
                        secaoTexto.append("    VDIV.F64 " + regResultado + ", " + regA + ", " + regB + "    @ quociente double")
                        secaoTexto.append("    VCVT.S32.F64 S31, " + regResultado + "    @ trunca para inteiro em temp S31")
                        secaoTexto.append("    VCVT.F64.S32 " + regResultado + ", S31    @ quociente inteiro como double")
                        secaoTexto.append("    VMUL.F64 " + regResultado + ", " + regResultado + ", " + regB + "    @ quociente * divisor")
                        secaoTexto.append("    VSUB.F64 " + regResultado + ", " + regA + ", " + regResultado + "    @ resto = dividendo - quociente * divisor")

                    elif token.valor == "^":
                        nomeLabel = "potencia" + str(contadorLabel)
                        contadorLabel += 1
                        secaoTexto.append("    @ potenciacao: " + regA + " ^ " + regB + " (loop com VMUL)")
                        secaoTexto.append("    VCVT.S32.F64 S31, " + regB)
                        secaoTexto.append("    VMOV R0, S31              @ R0 = expoente (inteiro)")
                        secaoTexto.append("    @ inicializa resultado com 1.0")
                        if "1.0" in constantesUsadas:
                            nomeConst1 = constantesUsadas["1.0"]
                        else:
                            nomeConst1 = "const_1_0_pos"
                            constantesUsadas["1.0"] = nomeConst1
                            secaoDados.append("    .align 3")
                            secaoDados.append("    " + nomeConst1 + ": .double 1.0")
                        secaoTexto.append("    LDR R4, =" + nomeConst1)
                        secaoTexto.append("    VLDR " + regResultado + ", [R4]    @ resultado = 1.0")
                        secaoTexto.append(nomeLabel + ":")
                        secaoTexto.append("    CMP R0, #0")
                        secaoTexto.append("    BLE " + nomeLabel + "_fim")
                        secaoTexto.append("    VMUL.F64 " + regResultado + ", " + regResultado + ", " + regA)
                        secaoTexto.append("    SUB R0, R0, #1")
                        secaoTexto.append("    B " + nomeLabel)
                        secaoTexto.append(nomeLabel + "_fim:")

                    pilhaRegistradores.append(regResultado)

                # Memoria: store (pilha com valor) ou load (pilha vazia)
                elif token.tipo == "MEMORIA":
                    nomeMem = token.valor
                    nomeLabel = "mem_" + nomeMem

                    if nomeLabel not in labelsMemoria:
                        secaoDados.append("    .align 3")
                        secaoDados.append("    " + nomeLabel + ": .double 0.0")
                        labelsMemoria.add(nomeLabel)

                    if len(pilhaRegistradores) > 0:
                        # Store: valor da pilha vai para memória
                        regValor = pilhaRegistradores.pop()
                        secaoTexto.append("    LDR R0, =" + nomeLabel + "        @ store em " + nomeMem)
                        secaoTexto.append("    VSTR " + regValor + ", [R0]")
                    else:
                        # Load: valor da memória vai para registrador
                        regCarregado = "D" + str(contadorRegistrador)
                        contadorRegistrador += 1
                        secaoTexto.append("    LDR R0, =" + nomeLabel + "        @ load de " + nomeMem)
                        secaoTexto.append("    VLDR " + regCarregado + ", [R0]")
                        pilhaRegistradores.append(regCarregado)

                # RES: acessa histórico de resultados
                elif token.tipo == "KEYWORD" and token.valor == "RES":
                    if len(pilhaRegistradores) < 1:
                        secaoTexto.append("    @ ERRO: falta N para RES")
                        continue

                    regN = pilhaRegistradores.pop()
                    regResultado = "D" + str(contadorRegistrador)
                    contadorRegistrador += 1

                    secaoTexto.append("    @ RES: acessa resultado anterior")
                    secaoTexto.append("    VCVT.S32.F64 S31, " + regN)
                    secaoTexto.append("    VMOV R0, S31              @ R0 = N")
                    secaoTexto.append("    LDR R1, =resultados")
                    secaoTexto.append("    LDR R2, =numResultados")
                    secaoTexto.append("    LDR R2, [R2]")
                    secaoTexto.append("    SUB R2, R2, R0              @ indice = total - N")
                    secaoTexto.append("    LSL R2, R2, #3              @ offset em bytes (double = 8)")
                    secaoTexto.append("    ADD R1, R1, R2")
                    secaoTexto.append("    VLDR " + regResultado + ", [R1]")
                    pilhaRegistradores.append(regResultado)

    # Se alguma expressao usou RES, adiciona resultados e numResultados ao .data
    usaRES = any(any(t.tipo == "KEYWORD" and t.valor == "RES" for t in tokens) for tokens in listaTokens)
    if usaRES:
        secaoDados.append("    .align 3")
        secaoDados.append("    resultados: .space 800       @ espaco para 100 doubles")
        secaoDados.append("    numResultados: .word 0")

    # Adiciona fim do programa
    secaoTexto.append("")
    secaoTexto.append("    @ Fim do programa")
    secaoTexto.append("fim:")
    secaoTexto.append("    B fim")

    # Monta o código Assembly completo
    codigoAssembly.append(".global _start")
    codigoAssembly.append("")
    codigoAssembly.append(".data")
    for linha in secaoDados:
        codigoAssembly.append(linha)
    codigoAssembly.append("")
    codigoAssembly.append(".text")
    codigoAssembly.append("_start:")
    for linha in secaoTexto:
        codigoAssembly.append(linha)

# Exibe os resultados formatados
def exibirResultados(exibicao):
    print("\nResultados das expressoes (CPULATOR)")
    
    if not exibicao:
        print("Nenhum resultado para exibir.")
        return

    # Percorre a lista de resultados e imprime com 1 casa decimal
    for num_linha, valor in exibicao:
        if valor is not None:
            print(f"Linha {num_linha}: {valor:.1f}")
        else:
            print(f"Linha {num_linha}: ---")
    print("\n")
        
def testarAnalisadorLexico():
    print("=" * 50)
    print("Testes do analisador lexico\n")

    # Cada caso tem: (descrição, entrada, True se valido / False se invalido)
    casos = [
        # Casos válidos
        ("Adicao simples",           "(3.0 2.0 +)",           True),
        ("Subtracao simples",        "(5.0 1.0 -)",           True),
        ("Multiplicacao simples",    "(3.0 4.0 *)",           True),
        ("Divisao real",             "(10.0 2.0 /)",          True),
        ("Divisao inteira",          "(10 3 //)",             True),
        ("Resto",                    "(10 3 %)",              True),
        ("Potenciacao",              "(2.0 8 ^)",             True),
        ("Numero negativo",          "(-2.0 3.0 +)",          True),
        ("Expressao aninhada",       "((2.0 3.0 *) 4.0 +)",  True),
        ("Comando RES",              "(2 RES)",               True),
        ("Comando store MEM",        "(5.0 X)",               True),
        ("Comando load MEM",         "(X)",                   True),

        # Casos inválidos
        ("Numero malformado",        "(3.14.5 2.0 +)",        False),
        ("Separador virgula",        "(3,14 2.0 +)",          False),
        ("Operador invalido",        "(3.0 2.0 &)",           False),
        ("Identificador minusculo",  "(3.0 var +)",           False),
    ]

    aprovados = 0
    reprovados = 0

    for descricao, entrada, esperaValido in casos:
        tokens = []
        parseExpressao(entrada, tokens)

        # Verifica se há algum token de ERRO na saída
        temErro = any(t.tipo == "ERRO" for t in tokens)

        # O teste passa se:
        # - esperava válido e não tem erro
        # - esperava inválido e tem erro
        passou = (esperaValido and not temErro) or (not esperaValido and temErro)

        status = "OK" if passou else "FALHOU"

        if passou:
            aprovados += 1
        else:
            reprovados += 1

        # print(status + " | " + descricao)
        # print("     Entrada : " + entrada)
        # print("     Tokens  : " + str(tokens))
        # print()

    print("Resultado: " + str(aprovados) + " aprovados, " + str(reprovados) + " reprovados")
    print("=" * 50 + "\n")

def testarExecutarExpressao():
    print("=" * 50)
    print("Testes do executar expressao\n")

    memoria = {}

    # Teste 1 - (1 RES) deve retornar 20.0
    resultados1 = []
    tokens1 = []
    parseExpressao("(3.14 2.0 +)", tokens1)
    executarExpressao(tokens1, resultados1, memoria)   # resultados1 = [5.14]

    tokens2 = []
    parseExpressao("(10.0 2.0 *)", tokens2)
    executarExpressao(tokens2, resultados1, memoria)   # resultados1 = [5.14, 20.0]

    tokens3 = []
    parseExpressao("(1 RES)", tokens3)
    resultado = executarExpressao(tokens3, resultados1, memoria)
    passou = resultado == 20.0
    print(("OK" if passou else "FALHOU") + " | (1 RES) deve retornar 20.0, retornou: " + str(resultado))

    # Teste 2 - (2 RES) deve retornar 5.14 → histórico separado!
    resultados2 = []
    tokens4 = []
    parseExpressao("(3.14 2.0 +)", tokens4)
    executarExpressao(tokens4, resultados2, memoria)   # resultados2 = [5.14]

    tokens5 = []
    parseExpressao("(10.0 2.0 *)", tokens5)
    executarExpressao(tokens5, resultados2, memoria)   # resultados2 = [5.14, 20.0]

    tokens6 = []
    parseExpressao("(2 RES)", tokens6)
    resultado = executarExpressao(tokens6, resultados2, memoria)
    passou = abs(resultado - 5.14) < 0.001
    print(("OK" if passou else "FALHOU") + " | (2 RES) deve retornar 5.14, retornou: " + str(resultado))

    # Teste 3 - store e load de memoria
    resultados3 = []
    tokens7 = []
    parseExpressao("(9.0 CONT)", tokens7)
    executarExpressao(tokens7, resultados3, memoria)

    tokens8 = []
    parseExpressao("(CONT)", tokens8)
    resultado = executarExpressao(tokens8, resultados3, memoria)
    passou = resultado == 9.0
    print(("OK" if passou else "FALHOU") + " | (CONT) deve retornar 9.0, retornou: " + str(resultado))

    print("=" * 50 + "\n")
    
def testarResolverAninhamento():
    print("=" * 50)
    print("Testes do resolver aninhamento\n")

    # ((2.0 3.0 *) 4.0 +) deve gerar 2 grupos:
    # grupo 1: [NUMERO(2.0), NUMERO(3.0), OPERADOR(*)]
    # grupo 2: [NUMERO(4.0), OPERADOR(+)]
    tokens = []
    parseExpressao("((2.0 3.0 *) 4.0 +)", tokens)
    grupos = resolverAninhamento(tokens)

    print("Entrada: ((2.0 3.0 *) 4.0 +)")
    print("Grupos encontrados: " + str(len(grupos)))
    for i, grupo in enumerate(grupos):
        print("  Grupo " + str(i) + ": " + str(grupo))

    passou = len(grupos) == 2
    print(("OK" if passou else "FALHOU") + " | deve ter 2 grupos")
    print("=" * 50 + "\n")

def testarGerarAssembly():
    print("=" * 50)
    print("Testes da geracao de assembly\n")

    # Testa com todas as expressoes obrigatorias de uma vez
    entradas = [
        "(3.14 2.0 +)",
        "((1.5 2.0 *) (3.0 4.0 *) /)",
        "(5.0 MEM)",
        "(MEM)",
        "(2 RES)",
        "(10 3 //)",
        "(10 3 %)",
        "(2.0 8 ^)",
        "(-2.0 3.0 +)",
    ]

    listaTokens = []
    for entrada in entradas:
        tokens = []
        parseExpressao(entrada, tokens)
        listaTokens.append(tokens)

    codigoAssembly = []
    gerarAssembly(listaTokens, codigoAssembly)

    # Verificacoes
    temGlobal = any(".global _start" in linha for linha in codigoAssembly)
    temSecaoDados = any(".data" in linha for linha in codigoAssembly)
    temSecaoTexto = any(".text" in linha for linha in codigoAssembly)
    temFim = any("B fim" in linha for linha in codigoAssembly)
    temLinhas = any("linha0:" in linha for linha in codigoAssembly)

    # Verifica deduplicacao de constantes (2.0 aparece varias vezes, deve ter so 1 label)
    contagem2_0 = sum(1 for linha in codigoAssembly if "const_2_0_pos" in linha and ".double" in linha)
    deduplicou = contagem2_0 == 1

    testes = [
        ("Tem .global _start", temGlobal),
        ("Tem .data", temSecaoDados),
        ("Tem .text", temSecaoTexto),
        ("Tem B fim", temFim),
        ("Tem labels linha0:", temLinhas),
        ("Deduplicou constantes (2.0 aparece 1x no .data)", deduplicou),
    ]

    aprovados = 0
    reprovados = 0

    for descricao, passou in testes:
        if passou:
            aprovados += 1
            status = "OK"
        else:
            reprovados += 1
            status = "FALHOU"
        print(status + " | " + descricao)

    print("Resultado: " + str(aprovados) + " aprovados, " + str(reprovados) + " reprovados")
    print("=" * 50 + "\n")

def main():
    if len(sys.argv) < 2:
        print("Uso: python analisador.py <arquivo_teste>")
        return

    print("Realização dos testes:\n")
    testarAnalisadorLexico()      
    testarExecutarExpressao()
    testarResolverAninhamento()
    testarGerarAssembly()

    nomeArquivo = sys.argv[1]
    linhas = []
    lerArquivo(nomeArquivo, linhas)

    resultados = []   # historico de resultados para RES
    memoria = {}      # dicionario de variaveis para MEM
    listaTokens = []  # acumula tokens de todas as linhas

    exibicao = []     # lista de tuplas (num_linha, valor) para exibir os resultados

    # Para cada linha, faz a analise lexica e executa
    for i, linha in enumerate(linhas):
        vetorTokens = []
        parseExpressao(linha, vetorTokens)
        listaTokens.append(vetorTokens)

        # Captura o retorno (pode ser um float ou None se der erro/for V MEM)
        res = executarExpressao(vetorTokens, resultados, memoria)
        # Salva o número da linha (i + 1) e o resultado dela para o terminal
        exibicao.append((i + 1, res))

    # Manda a lista focada na saída
    exibirResultados(exibicao)

    codigoAssembly = []
    gerarAssembly(listaTokens, codigoAssembly)

    # Salva o Assembly em arquivo .s
    nomeAssembly = nomeArquivo.replace('.txt', '.s')

    try:
        with open(nomeAssembly, 'w') as arquivoAssembly:
            for linhaAssembly in codigoAssembly:
                arquivoAssembly.write(linhaAssembly + '\n')
        print(f"Arquivo Assembly salvo em: {nomeAssembly}\n")
    except Exception as e:
        print(f"Erro ao salvar arquivo Assembly: {e}")

if __name__ == "__main__":
    main()

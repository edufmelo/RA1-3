import sys

# Deve ler o arquivo e chamar a função parseExpressao para cada linha
def lerArquivo(nomeArquivo, linhas):
    pass

# Deve analisar uma linha de expressão RPN e extrair tokens
def parseExpressao(linha, vetorTokens):
    estadoInicial()

# Estados do AFD (cada estado é uma função) 
def estadoInicial(): 
    pass

def estadoNumero():
    pass

def estadoOperador():
    pass

def estadoParenteses():
    pass

def estadoIdentificador():  # para RES, MEM, VAR, etc.
    pass

# Numeros malformados, tokens inválidos
def estadoErro():
    pass

# Avalia as expressões RPN (pilha) e gerencia memoria/RES
def executarExpressao(tokens, resultados, memoria):
    pass

# Gera código Assembly a partir dos tokens
def gerarAssembly(tokens, codigoAssembly):
    pass

# Exibe os resultados formatados
def exibirResultados(resultados):
    pass

def main():
    if len(sys.argv) < 2:
        print("Uso: python analisador.py <arquivo_teste>")
        return
    
    nomeArquivo = sys.argv[1]
    linhas = []
    lerArquivo(nomeArquivo, linhas)

if __name__ == "__main__":
    main()
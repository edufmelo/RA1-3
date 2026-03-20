import sys

# Como nos slides (Aula 04), contudo, de forma mais simples com tipo e valor
class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo    # o tipo do token (NUMERO, OPERADOR, PARENTESE, IDENTIFICADOR, KEYWORD, ERRO)
        self.valor = valor  # o texto original do token (ex: '3.14', '+', 'RES')

    def __repr__(self): # útil para realizarmos testes - debug (remover ao final)
        return "Token(" + self.tipo + ", " + self.valor + ")"

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

# Deve analisar uma linha de expressão RPN e extrair tokens
def parseExpressao(linha, vetorTokens):
    pos = 0     
    while pos < len(linha):  
        char = linha[pos]
        
        # O parseExpressao age como o estado inicial do AFD
        if char == ' ' or char == '\t':  # Ignora espaços ou tab
            pos += 1
        elif char.isdigit() or char == '.':
            pos = estadoNumero(linha, pos, vetorTokens)
        elif char in '+-*/%^':
            pos = estadoOperador(linha, pos, vetorTokens)
        elif char in '()':
            pos = estadoParenteses(linha, pos, vetorTokens)
        elif char.isalpha(): 
            pos = estadoIdentificador(linha, pos, vetorTokens)
        else:
            pos = estadoErro(linha, pos, vetorTokens)

# Falta implementação
def estadoNumero(linha, pos, tokens):
    return pos + 1

def estadoOperador(linha, pos, tokens):
    return pos + 1

def estadoParenteses(linha, pos, tokens):
    return pos + 1

def estadoIdentificador(linha, pos, tokens):  # para RES, MEM, VAR, etc.
    return pos + 1

# Numeros malformados, tokens inválidos
def estadoErro(linha, pos, tokens):
    return pos + 1

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

    # Para cada linha, faz a analise lexica e mostra os tokens
    for i in range(len(linhas)):
        vetorTokens = []
        parseExpressao(linhas[i], vetorTokens)
        
        # Utilizado para debugar
        print("Linha " + str(i) + ": " + linhas[i])
        print("Tokens: " + str(vetorTokens)) 
        print()

if __name__ == "__main__":
    main()
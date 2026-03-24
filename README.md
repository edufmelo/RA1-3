# Fase 1 - Analisador Léxico e Gerador de Assembly para ARMv7

**Instituição:** PUCPR
**Disciplina:** Linguagens Formais e Compiladores  
**Professor:** Frank Coelho de Alcantara  
**Grupo:** RA1-3  

## Integrantes do Grupo
- Daniel de Almeida Santos Bina (GitHub: @danielbina) 
- Eduardo Ferreira de Melo (GitHub: @edufmelo) 
- João Eduardo Faccin Leineker (GitHub: @joaooleineker) 

*(Nota: O repositório está organizado com commits claros e as contribuições de cada integrante foram registradas na forma de Pull Requests, conforme a especificação).*

---

## Sobre o Projeto
Este projeto compõe a primeira fase da construção de um compilador. O objetivo é desenvolver um programa capaz de ler um arquivo de texto contendo expressões aritméticas em **Notação Polonesa Reversa (RPN)** e analisá-las utilizando um **Analisador Léxico** baseado em Autômatos Finitos Determinísticos (AFDs). 

A partir da string de *tokens* gerada pelo analisador léxico, o programa traduz as operações para um código Assembly funcional e compatível com a arquitetura **ARMv7 DEC1-SOC(v16.1)**, para ser validado no simulador **CPULATOR**.

---

## Compilação e Pré-requisitos
O projeto foi desenvolvido inteiramente em **Python**. Portanto, não há processo de compilação (geração de binários) prévio. O código é interpretado diretamente.

**Requisitos:**
* Python 3.x instalado no sistema.

---

## Como Executar
O programa não possui menus interativos. Ele deve ser executado via linha de comando, passando o arquivo de teste como argumento.

1. Abra o terminal na raiz do projeto.
2. Execute o comando abaixo:

```bash
python analisador.py <nome_do_arquivo.txt>
```

O que o programa fará:

1. Lerá o arquivo de entrada linha por linha.
2. Imprimirá no terminal a lista de Tokens gerada pela análise léxica (para fins de depuração).
3. Gerará um código Assembly compatível com o ARMv7.
4. Salvará a saída Assembly (ex: teste1.s) ou a imprimirá no terminal para ser copiada.

## Testes e Validação no CPULATOR
O repositório contém um mínimo de 3 arquivos de texto para testes, cada um contendo pelo menos 10 linhas de expressões.

**Os arquivos incluem testes para:**

- Operações aritméticas básicas e aninhadas (+, -, *, /, //, %, ^).
- Comandos especiais de manipulação de memória (N RES, V MEM, MEM).
- Entradas inválidas e números malformados para testar o tratamento de erros do Autômato Finito Determinístico.

**Como validar o Assembly:**

1. Gere o código Assembly executando o programa com um arquivo de teste.
2. Acesse o Simulador CPULATOR configurado para ARMv7 DEC1-SOC(v16.1).
3. Abra o arquivo .s gerado no simulador, pressione o botão "Compile and Load (F5)" na linguagem ARMv7 e execute passo a passo com Step Over (F2) ou Resume (F3) para verificar se as operações estão ocorrendo corretamente.

## Observações e Decisões de Projeto
- **Nomenclatura do Repositório:** O nome do grupo registrado no Canvas é "RA1 3". No entanto, como o GitHub não permite o uso de espaços na criação de URLs de repositórios, adaptamos o nome para RA1-3.

- **Integração e Divisão de Tarefas:** A equipe buscou seguir a sugestão de divisão de responsabilidades apresentada na especificação, assim, nomeando as branchs de acordo com a divisão de tarefas sugerida na especificação, com o formato `feature/aluno-X`. No entanto, para garantir um fluxo de desenvolvimento contínuo, realizamos algumas adaptações práticas. Funções de infraestrutura básica, como exemplo a função `lerArquivo` (originalmente sugerida para o Aluno 3), foram implementadas de forma antecipada durante a construção da base do analisador léxico. Essa abordagem nos permitiu realizar testes isolados do Autômato Finito Determinístico desde o primeiro dia e adiantou os passos de integração estrutural do projeto como um todo.


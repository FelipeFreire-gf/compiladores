# Semana 1 - Prática: Configuração do Ambiente de Desenvolvimento

## Ferramentas Básicas

- **Flex** ou **Lex** (analisador léxico)
- **Bison** ou **Yacc** (gerador de parser sintático)
- **ANTLR** (ferramenta alternativa que combina análise léxica e sintática)
- **Editor/IDE**: Visual Studio Code, Eclipse, CLion ou outros
- **Compilador de apoio**: `gcc`, `clang`, etc.

---

## Instalação e Configuração (Linux)

- Atualizar repositório:
  ```bash
  sudo apt-get update
  ```
- Instalar ferramentas:
  ```bash
  sudo apt-get install flex bison
  ```
- Verificar versões:
  ```bash
  flex --version
  bison --version
  ```

---

## Instalação e Configuração (Windows)

- Usar **MSYS2**, **Cygwin** ou **WSL** (Windows Subsystem for Linux)
- Instalar `flex` e `bison` via gerenciadores de pacotes compatíveis

---

## Estrutura de Projeto

- **Pasta para analisador léxico** (`lex/lexer`)
- **Pasta para analisador sintático** (`parser`)
- **Pasta para testes**
- **Pasta para artefatos compilados** (`build/bin`)

### Controle de Versão

- Uso de **Git** e **GitHub/GitLab**
- Convenções de **commit** e **branching**

---

## Primeiros Testes

- Testar o exemplo `hello.*` ("Hello, World!") usando **flex + bison**:
  - Criar analisador léxico mínimo (tokens de `Hello` e `World`)
  - Integrar no parser e gerar saída confirmando os tokens
- Verificar compilação e execução
- Analisar os códigos `hello.l` e `hello.y`

---

## Atividade PBL do Dia

**Objetivo:**  
Garantir que todos os grupos tenham um ambiente de desenvolvimento funcional.

**Tarefas:**

1. Verificar instalação das ferramentas
2. Criar repositório Git para o projeto do compilador
3. Subir um teste simples de analisador léxico ou parser

**Entrega:**  
Apresentação de evidências do funcionamento do setup (prints ou demonstração).

# Tabela de Versionamento 

| Versão | Data       | Descrição da Alteração              | Nome(s) Integrante(s) |
| :----: | :--------: | :---------------------------------: | :-------------------: |
| 1.0    | 28/04/2025 | Criação da atividade de desenvolvimento 1  | [Júlio Cesar](https://github.com/Julio1099)        |

---
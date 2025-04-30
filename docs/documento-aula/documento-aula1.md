# Semana 2 - Prática: Construção de Analisador Léxico Simples

## Objetivos da Aula

- Aplicar conceitos de autômatos e expressões regulares para identificar tokens
- Apresentar ferramentas de análise léxica (ex.: flex, bison, etc.)
- Implementar um scanner simples para uma linguagem de exemplo

---

## Revisão: Expressões Regulares

### Definição

- Notação formal para descrever padrões em cadeias de caracteres

### Símbolos Básicos

- **Σ**: alfabeto
- **Operadores**: `*`, `+`, `?`, `|`, `()`

> Consulte o "Guia rápido de expressões regulares" no GitHub da disciplina (semana 02).

### Exemplo

- `[a-zA-Z_][a-zA-Z0-9_]*` representa identificadores simples em muitas linguagens

---

## Fluxo de um Analisador Léxico

1. Leitura da entrada caractere a caractere
2. Reconhecimento de tokens com base em padrões (ER)
3. Produção de tokens para a análise sintática
4. Tratamento de erros léxicos (símbolos inesperados)

---

## Fluxo de Criação e Execução do Exemplo

- Definição de regras em arquivo `.l`
- Geração de código em C
- Compilação e execução do scanner

---

## Ferramentas e Prática

### Exemplo de Ferramenta (flex)

- Arquivo `.l` com regras de token e ações
- Geração do arquivo em C para a etapa de análise léxica

### Exercício Prático

- Criação de um arquivo `scanner.l` que reconheça:
  - Identificadores
  - Números inteiros
  - Espaços em branco

### Boas Práticas

- Testar incrementos pequenos de cada regra
- Implementar tratamento de erro (caracteres inválidos)

---

## Tarefa

1. Configurar e compilar um analisador léxico básico usando flex (ou outra ferramenta disponível)
2. Validar se identificadores, números e operadores simples são reconhecidos corretamente

---

# Tabela de Versionamento 

| Versão | Data       | Descrição                           | Autor(es) | Revisor(es) |
|--------|------------|-------------------------------------|-----------|-------------|
| 1.0    | 28/04/2025 | Criação da atividade de desenvolvimento 1        | [Júlio Cesar](https://github.com/Julio1099) | [Felipe das Neves](https://github.com/FelipeFreire-gf) |
=======
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
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
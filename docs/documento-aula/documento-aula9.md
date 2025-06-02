# Compiladores 1 - Semana 9: Prática

## Otimização de Código - Introdução

### Objetivos da Aula Prática

- Implementar técnicas básicas de otimizaçãao de código
- Integrar o protótipo Flex+Bison ao fluxo de construção
- Automatizar a verificação através de testes em `tests/*.in`
- Analisar o impacto das otimizações no código gerado

---

### Configuração do Projeto

**Estrutura do Makefile:**

```makefile
# Variáveis essenciais
CC = gcc
FLEX = flex
BISON = bison
CFLAGS = -Wall -O2
LDFLAGS = -lfl

# Arquivos fonte
SRC = main.c
LEX = scanner.l
YACC = parser.y
TARGET = optimize
TESTS = tests/*.in
```

**Comandos principais:**

```bash
make       # Compila o otimizador (gera executável 'optimize')
make test  # Executa todos os testes automatizados
make clean # Limpa arquivos gerados
```

---

### Fluxo de Trabalho

**Compilação:**

```bash
make
```

**Execução de Testes:**

```bash
make test
```

Exibe para cada teste em `tests/`:

- Nome do caso de teste
- Entrada fornecida
- Saída do otimizador

**Adição de Novos Testes:**

- Criar arquivos `.in` no diretório `tests/`
- Padrão: `testeXX.in` (onde XX é número sequencial)

---

### Tarefas Práticas

**Análise de Resultados:**

- Executar `make test` e examinar as saídas
- Verificar a correção das otimizações aplicadas

**Expansão do Projeto:**

- Implementar novas técnicas de otimização
- Adicionar casos de teste representativos

**Gerenciamento de Código:**

```bash
git add .
git commit -m "Implementa otimizações básicas"
git push origin main
```

**Desenvolvimento Contínuo:**

- Avançar na implementação do trabalho em equipe
- Documentar as otimizações implementadas

---

### Tabela de Versionamento

| Versão | Data       | Descrição                                | Autor(es) | Revisor(es) |
|--------|------------|------------------------------------------|-----------|-------------|
| 1.0    | 01/06/2025 | Criação da atividade de desenvolvimento 9 | [Júlio Cesar](https://github.com/Julio1099) |  |

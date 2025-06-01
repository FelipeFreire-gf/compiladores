
# Compiladores 1 - Semana 10: Prática

## Geração de Código Final (Bitcode)

### Objetivos da Prática

- Implementar reconhecimento de expressões Java simples usando Flex+Bison
- Gerar código intermediário em formato bitcode textual
- Automatizar o processo de compilação e testes via Makefile
- Compreender o mapeamento entre operações da linguagem fonte e instruções de bitcode
- Validar a correta geração de código através de testes automatizados

---

### Estrutura do Projeto
```
projeto/
├── src/
│   ├── lexer.l      # Especificação do analisador léxico
│   ├── parser.y     # Especificação do analisador sintático
│   ├── ast.c/h      # Implementação da AST
├── tests/
│   ├── *.java       # Casos de teste em Java
├── Makefile         # Automação do build
├── README.md        # Documentação do projeto
```

**Artefatos gerados:**
- Executável: `./generate` (compilador que gera bitcode)
- Arquivos temporários durante a compilação

---

### Fluxo de Trabalho

1. **Compilação:**
   ```bash
   make        # Gera o compilador completo
   ```

2. **Execução de Testes:**
   ```bash
   make test   # Roda todos os casos de teste
   ```

3. **Limpeza:**
   ```bash
   make clean  # Remove arquivos gerados
   ```

**Exemplo de Teste:**

- Entrada (`tests/sum.java`):
    ```java
    int x = 3 + 4;
    ```

- Saída (bitcode gerado):
    ```
    LOAD_CONST 3
    LOAD_CONST 4
    ADD
    STORE x
    ```

---

### Tarefas Práticas

#### Exploração do Código:
- Analisar e modificar os exemplos existentes
- Compreender a relação entre gramática e geração de código

#### Expansão de Testes:
- Adicionar novos casos de teste em `tests/*.java`
- Verificar a correta geração de bitcode

#### Desenvolvimento do Projeto:
- Implementar novas funcionalidades no compilador da equipe
- Documentar as decisões de implementação

#### Versionamento:
```bash
git add .
git commit -m "Implementa geração de bitcode para expressões aritméticas"
git push origin main
```

### Tabela de Versionamento

| Versão | Data       | Descrição                                | Autor(es) | Revisor(es) |
|--------|------------|------------------------------------------|-----------|-------------|
| 1.0    | 01/06/2025 | Criação da atividade de desenvolvimento 10 | [Júlio Cesar](https://github.com/Julio1099) |  |
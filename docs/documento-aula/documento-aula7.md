# Semana 7 - Prática: Integração da Análise Semântica no Compilador

## Objetivos da Aula

1. Integrar a análise semântica ao compilador Flex+Bison.
2. Implementar verificações de:
   - Declaração de variáveis.
   - Redeclaração de identificadores.
   - Compatibilidade de tipos.
3. Gerar e analisar a AST (Árvore Sintática Abstrata) anotada.
4. Validar a implementação por meio de testes automatizados.
5. Adaptar o código à estrutura dos projetos individuais.

---

## Conexão com as Sprints

- **Sprint anterior:** Finalização do parser com tratamento de erros sintáticos.
- **Sprint atual:**
  - Implementar e testar análise semântica.
  - Anotar a AST com informações de tipo e escopo.
  - Adicionar ao backlog: verificação semântica, anotações na árvore, e testes com erros semânticos.

---

## Conceito: Análise Semântica

1. **Verificação de declaração:** Identificar uso de variáveis não declaradas.
2. **Redeclaração de identificadores:** Impedir múltiplas declarações de uma mesma variável no mesmo escopo.
3. **Verificação de tipo:** Comparar tipos entre operandos e expressões.
4. **AST anotada:** Estrutura de árvore com metadados semânticos (tipo, escopo, etc.).

---

# Tabela de Versionamento 

| Versão | Data       | Descrição                           | Autor(es) | Revisor(es) |
|--------|------------|-------------------------------------|-----------|-------------|
| 1.0    | 01/06/2025 | Criação da atividade de desenvolvimento 7        | [Júlio Cesar](https://github.com/Julio1099) | |

# Semana 8 - Prática: Geração de Código Intermediário (TAC)

## Objetivos da Aula

1. Desenvolver um protótipo funcional para geração de TAC (Three-Address Code)
2. Integrar a travessia da AST com a geração de instruções intermediárias
3. Compreender:
   - O uso de variáveis temporárias
   - O formato linear do código intermediário
4. Validar a geração de TAC através de testes automatizados

---

## Conexão com as Sprints

- **Sprint anterior:** Implementação de análise semântica e anotação da AST.
- **Sprint atual:**
  - Início da geração de código intermediário (TAC).
  - Adição de estrutura de geração e uso de temporárias.
  - Planejamento da integração com o interpretador ou próxima etapa do backend.

---

## Conceito: Código Intermediário (TAC)

1. **Formato linear:** Instruções com três endereços (ex: `t1 = a + b`).
2. **Temporárias:** Variáveis geradas durante a análise (ex: `t1`, `t2`).
3. **Abstração da máquina:** Independente da arquitetura alvo.

---

## Protótipo: Gerador de TAC

### Passos

1. **Preparação**
   ```bash
   unzip tac_prototipo_com_tests.zip
   cd tac_prototipo
   ```

2. **Compilação**
   ```bash
   make clean && make
   ```

3. **Testes**
   ```bash
   ./run_tests.sh
   ```

4. **Verificações**
   - A correta geração de TAC para expressões válidas
   - A estrutura esperada das instruções intermediárias

---

## Tarefa para a Aula Prática

1. Estudar a implementação da AST e da função `gerarTAC()`.
2. Adicionar casos de teste no diretório `tests/` cobrindo:
   - Expressões aritméticas simples e compostas
   - Uso de variáveis e temporárias
3. Documentar:
   - As funções principais do gerador
   - Estratégias de alocação de temporárias
4. Integrar o protótipo ao projeto do grupo.
5. Planejar o próximo passo do backend (interpretador ou gerador final).

---

## Alinhamento com a Disciplina

- **Cronograma:** Aula prática 8, após conclusão da análise semântica.
- **Objetivo:** Início da geração de código no compilador.
- **Próximos passos:**
  - Expansão da geração de TAC
  - Implementação de um interpretador para o código intermediário
  - Otimizações simples de TAC

---

## Conclusões e Recomendações

1. TAC é a ponte entre a AST e o código executável.
2. Geradores devem ser organizados e facilmente depuráveis.
3. Mensagens e logs de geração ajudam na validação.
4. A integração ao projeto deve ser incremental.
5. A documentação clara facilita a colaboração em equipe.

---

# Tabela de Versionamento 

| Versão | Data       | Descrição                           | Autor(es) | Revisor(es) |
|--------|------------|-------------------------------------|-----------|-------------|
| 1.0    | 01/06/2025 | Criação da atividade de desenvolvimento 8 | [Júlio Cesar](https://github.com/Julio1099) | |

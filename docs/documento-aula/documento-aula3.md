# Semana 3 - Prática: Projeto Inicial do Compilador (Fase Léxica)
 


 

## Objetivo
 


 

Iniciar o desenvolvimento efetivo do compilador/interpretador, concentrando-se na etapa de análise léxica.
 


 

---
 


 

## Objetivos da Aula
 


 

- Retomar a ideia de cada equipe sobre o compilador/interpretador escolhido
 

- Implementar a fase léxica (analisador léxico) com base em tokens principais
 

- Entregar um protótipo funcional e documentado, que servirá para o P1
 


 

---
 


 

## Importância da Fase Léxica
 


 

- Transforma cadeias de caracteres em tokens (ex.: `IDENT`, `NUM`, `OP`)
 

- Fornece a base para a análise sintática
 

- Requisito mínimo para demonstrar progresso no P1 (30/04)
 


 

---
 


 

## Tarefas de Hoje
 


 

1. Definir tokens do projeto: identificadores, números, palavras-chave, símbolos
 

2. Criar arquivo léxico (exemplo em Flex)
 

3. Testar o scanner usando entradas curtas (verificação rápida dos tokens)
 

4. Documentar: atualizar repositório (código, README, anotações)
 


 

---
 


 

## Exemplo de Ponto de Partida (Flex)
 


 

- Disponível via GitHub (semana 03/scanner.l)
 


 

---
 


 

## Tarefa (Parte 1 de 2)
 


 

- **Personalizar:** adicionar ou remover tokens conforme a linguagem de cada equipe
 

- **Inserir tratamento para comentários**:
 

  - `//` até o fim da linha
 

  - `/* bloco */`
 

- **Gerar o scanner:**
 

  ```bash
 

  flex scanner.l
 

  gcc -o scanner lex.yy.c
 

  ./scanner
 

  ```
 


 

---
 


 

## Tarefa (Parte 2 de 2)
 


 

- **Testar** usando um arquivo de exemplo, ex.:
 


 

  ```text
 

  if x1 == 10
 

  {
 

      while _flag
 

          x1 = x1 + 2
 

  }
 

  ```
 


 

- Observar tokens gerados e avaliar se precisam de ajustes
 

- **Publicar commits** no repositório (GitHub) e atualizar README:
 

  - Como rodar o scanner
 

  - Lista de tokens implementados
 

  - Planejamento para a próxima fase
 


 
---

## Histórico de Versões

| Versão | Data       | Descrição                           | Autor(es) | Revisor(es) |
|--------|------------|-------------------------------------|-----------|-------------|
| 1.0    | 28/04/2025 | Desenvolvimento do Artefato         | [Julio Cesar](https://github.com/Julio1099) | [Felipe as Neves](https://github.com/FelipeFreire-gf) |
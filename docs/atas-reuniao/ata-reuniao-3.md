# Ata de Reunião 

**Data:** 09/04/2025  

**Hora Prevista:** 14:00 - 16:00  
**Hora Realizada:** 14:00 até 16:00  
**Local:** Presencial

---

## Participantes

<font size="3"><p style="text-align: left">Tabela 1: Presença</p></font>

| Nome              | Presença |
|-------------------|----------|
| Felipe das Neves  | ✔️        |
| Breno Alexandre   | ✔️        |
| Julio Cesar       | ✔️        |
| Lucas Soares      | ✔️        |
| Kaleb Macedo    | ✔️        |
| Othavio Araujo    | ✔️        |

<font size="3"><p style="text-align: left">Fonte: [Kaleb Macedo](https://github.com/kalebmacedo), 2025.</p></font>

---

## Discussões

- Iniciada a fase de construção do interpretador, com foco na análise léxica.
- Revisão dos conceitos de tokens e definição dos tokens do projeto: identificadores, números, palavras-chave e símbolos.
- Criação de um arquivo léxico `scanner.l` com base na ferramenta **Flex**.
- Implementado o tratamento de comentários do tipo `//` (linha) e `/* */` (bloco).
- Execução do scanner com os comandos:
  - `flex scanner.l`
  - `gcc -o scanner lex.yy.c`
  - `./scanner`
- Testes realizados com entradas curtas para identificar os tokens e validar se estão corretamente reconhecidos.
- Observada a necessidade de ajustar regras para operadores e caracteres especiais.
---

### Decisões:

- Confirmado uso de Flex como ferramenta oficial para a análise léxica.
- O scanner deve ser personalizado conforme a linguagem-alvo de cada grupo.
- Todos devem implementar tratamento para erros e comentários no scanner.
---

### Próxima Reunião
**29/04/2025 às 22h**

---

# Tabela de Versionamento 

| Versão | Data       | Descrição da Alteração                    | Nome(s) Integrante(s) |
| :----: | :--------: | :---------------------------------------: | :-------------------: |
| 1.0    | 25/04/2025 | Criação da ata da reunião 03 (fase léxica)  | [Kaleb Macedo](https://github.com/kalebmacedo)        |

---


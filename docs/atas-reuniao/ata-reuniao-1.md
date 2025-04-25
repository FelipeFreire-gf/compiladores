# Ata de Reunião 01

**Data:** 26/03/2025  

**Hora Prevista:** 14:00 - 16:00  
**Hora Realizada:** 14:00 - 16:00   
**Local:** Presencial 

**Redator:** [Kaleb Macedo](https://github.com/kalebmacedo)

---

## Participantes

<font size="3"><p style="text-align: left">Tabela 1: Presença</p></font>

| Nome              | Presença |
|-------------------|----------|
| Felipe das Neves  | ✔️        |
| Breno Alexandre   | ✔️        |
| Julio Cesar       | ✔️        |
| Lucas Soares      | ✔️        |
| Kaleb de Macedo   | ✔️        |
| Othávio Araujo    | ✔️        |

<font size="3"><p style="text-align: left">Fonte: [Kaleb Macedo](https://github.com/kalebmacedo), 2025.</p></font>

---

## Discussões

- Estrutura de projeto para o compilador foi definida:
  - Pasta para analisador léxico (`lex` ou `lexer`)
  - Pasta para analisador sintático (`parser`)
  - Pasta para testes
  - Pasta para artefatos compilados (`build` ou `bin`)
- Implementado controle de versão com uso de `Git`, com repositórios no GitHub/GitLab e uso de convenções de `commit` e `branching`.
- Realização de primeiros testes com `flex` + `bison`:
  - Analisador léxico mínimo que identifica tokens como `Hello` e `World`
  - Integração com o parser e geração de saída para confirmação
  - Verificação de compilação e execução
  - Análise dos arquivos `hello.l` e `hello.y`

---

### Decisões:

- O teste com `hello.l` e `hello.y` é obrigatório para todos os integrantes do grupo.
- Possivelmente será criado um Interpretador.

---

### Próxima Reunião
**02/04/2025 às 14h**

---

# Tabela de Versionamento 

| Versão | Data       | Descrição da Alteração      | Nome(s) Integrante(s) |
| :----: | :--------: | :-------------------------: | :-------------------: |
| 1.0    | 24/04/2025 | Criação da ata da reunião 01   | [Kaleb Macedo](https://github.com/kalebmacedo)       |

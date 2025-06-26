# Testes

> Este documento detalha a implementação da suíte de testes do projeto para garantir a corretude e a estabilidade do interpretador, além da documentação técnica das funcionalidades implementadas.

---

## Estratégia de Testes

Para validar o interpretador, adotamos uma abordagem de testes unitários e de integração utilizando a biblioteca `pytest`. A estratégia foi dividida em duas categorias principais:

1.  **Testes de Sucesso (Happy Path)**: Verificam se o interpretador executa corretamente códigos C válidos e produz o resultado esperado.
2.  **Testes de Erro (Sad Path)**: Asseguram que o interpretador identifica e lida adequadamente com erros, sejam eles sintáticos (código malformado) ou semânticos/runtime (erros durante a execução).

A estrutura de testes consiste em alimentar o interpretador com pequenos trechos de código C e comparar o resultado (ou o erro gerado) com um valor esperado.

### 1. Testes de Sucesso

Estes testes cobrem todas as funcionalidades implementadas, como operações aritméticas, estruturas de controle, manipulação de arrays, etc.

*   **Objetivo**: Garantir que a lógica do interpretador está correta para entradas válidas.
*   **Implementação (Exemplo Hipotético)**: Criamos uma função de teste para cada cenário. A função define um código C, o executa através do interpretador e usa a declaração `assert` do `pytest` para verificar se o valor de retorno é o esperado.

```python
# test_interpreter.py (Exemplo)
import pytest
from main import run_interpreter # Supondo uma função principal que executa o interpretador

def test_while_loop_sum():
    """
    Testa um laço 'while' que calcula a soma dos números de 1 a 5.
    """
    code = """
        int i = 1;
        int sum = 0;
        while (i < 6) {
            sum = sum + i;
            i = i + 1;
        }
        return sum;
    """
    result = run_interpreter(code)
    assert result == 15 # 1 + 2 + 3 + 4 + 5 = 15
```

### 2. Testes de Erro

Esses são cruciais para a robustez do interpretador. Eles verificam se os erros são capturados nos momentos certos (parsing ou execução) e se as mensagens de erro são informativas.

*   **Objetivo**: Validar o tratamento de exceções e a detecção de erros.
*   **Implementação (Exemplo Hipotético)**: Utilizamos o `pytest.raises` para afirmar que um determinado tipo de erro é lançado ao tentar executar um código C inválido.

```python
# test_interpreter.py (Exemplo)
def test_undeclared_variable_error():
    """
    Testa se um NameError é lançado ao tentar usar uma variável não declarada.
    """
    code = """
        int x = 5;
        y = x + 2; // 'y' não foi declarada
        return y;
    """
    with pytest.raises(NameError, match="Variable 'y' not declared."):
        run_interpreter(code)
```

---

## Tabela de Versionamento

| Versão | Data       | Descrição                                | Autor(es)                                              | Revisor(es)                                  |
| ------ | ---------- | ---------------------------------------- | ------------------------------------------------------ | -------------------------------------------- |
| 1.0    | 26/06/2025 | Desenvolvimento do artefato para docuementação | [Felipe das Neves](https://github.com/FelipeFreire-gf) | [Lucas Soares](https://github.com/lucaaassb) |
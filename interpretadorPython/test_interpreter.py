import unittest
import os
import sys
from io import StringIO
from lexer import lexer
from parser import parser 
from interpreter import Interpreter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FILES_DIR = os.path.join(BASE_DIR, "Testes")

PROJECT_DIR = BASE_DIR

class TestInterpreter(unittest.TestCase):

    def _run_interpreter(self, c_code_str, mock_input_values=None):
        """
        Método auxiliar para executar o interpretador com uma string de código C.
        Reinicia o lexer, faz o parse, interpreta e captura a saída.
        """
        
        lexer.input(c_code_str)
        lexer.lineno = 1 

        
        ast = parser.parse(c_code_str, lexer=lexer)

        if ast is None:
            self.fail(f"O parsing falhou e não retornou AST para o código C:\n---\n{c_code_str}\n---")

        interpreter_instance = Interpreter()

        if isinstance(__builtins__, dict):
            original_builtin_input = __builtins__.get('input')
        else:
            original_builtin_input = getattr(__builtins__, 'input', None)
            
        original_sys_stdout = sys.stdout
        
        captured_stdout = StringIO()
        
        sys.stdout = captured_stdout

        mock_input_iterator = None
        if mock_input_values:
            mock_input_iterator = iter(mock_input_values)
            def mocked_input_func(*args, **kwargs): 
                try:
                    return next(mock_input_iterator)
                except StopIteration:
                    self.fail("Valores de mock para input esgotados, mas input() foi chamado novamente.")
            if isinstance(__builtins__, dict):
                __builtins__['input'] = mocked_input_func
            else:
                __builtins__.input = mocked_input_func
        
        return_value_from_interpreter = None
        try:
            return_value_from_interpreter = interpreter_instance.interpret(ast)
        finally:
            if isinstance(__builtins__, dict):
                __builtins__['input'] = original_builtin_input
            else:
                __builtins__.input = original_builtin_input
            sys.stdout = original_sys_stdout

        results = {
            "return_value": return_value_from_interpreter,
            "globals": interpreter_instance.env_stack[0], 
            "arrays": interpreter_instance.arrays,
            "pointers": interpreter_instance.pointers, 
            "stdout": captured_stdout.getvalue()
        }
        return results

    def _load_and_run_test_file(self, c_file_path, mock_input_values=None):
        """Lê um arquivo .c e executa o interpretador com seu conteúdo."""
        try:
            with open(c_file_path, 'r', encoding='utf-8') as f:
                code = f.read()
        except FileNotFoundError:
            self.fail(f"Arquivo de teste não encontrado: {c_file_path}")
        return self._run_interpreter(code, mock_input_values)


    def test_01_arrays(self):
        file_path = os.path.join(TEST_FILES_DIR, "teste_arrays.c")
        result = self._load_and_run_test_file(file_path)
        self.assertEqual(result["return_value"], 3, "Valor de retorno incorreto para teste_arrays.c")
        self.assertIn('x', result["arrays"], "Array 'x' não encontrado em interpreter.arrays para teste_arrays.c")
        self.assertEqual(result["arrays"]['x'], [1, 2, 3], "Conteúdo do array 'x' incorreto para teste_arrays.c")
        self.assertEqual(result["globals"], {}, "Variáveis globais deveriam estar vazias para teste_arrays.c")

    def test_02_atribuicao(self):
        file_path = os.path.join(TEST_FILES_DIR, "teste_atribuicao.c")
        result = self._load_and_run_test_file(file_path)
        self.assertEqual(result["return_value"], 10, "Valor de retorno incorreto para teste_atribuicao.c")
        self.assertEqual(result["globals"], {}, "Variáveis globais deveriam estar vazias para teste_atribuicao.c")

    def test_03_blocos_escopo(self):
        file_path = os.path.join(TEST_FILES_DIR, "teste_blocos_escopo.c")
        result = self._load_and_run_test_file(file_path)
        self.assertEqual(result["return_value"], 3, "Valor de retorno incorreto para teste_blocos_escopo.c")
        self.assertEqual(result["globals"], {}, "Variáveis globais deveriam estar vazias para teste_blocos_escopo.c")

    def test_04_comparacoes(self):
        file_path = os.path.join(TEST_FILES_DIR, "teste_comparacoes.c")
        result = self._load_and_run_test_file(file_path)
        self.assertEqual(result["return_value"], 1, "Valor de retorno incorreto para teste_comparacoes.c")
        self.assertEqual(result["globals"], {}, "Variáveis globais deveriam estar vazias para teste_comparacoes.c")

    def test_05_declarar_variavel(self):
        file_path = os.path.join(TEST_FILES_DIR, "teste_declarar_variavel.c")
        result = self._load_and_run_test_file(file_path)
        self.assertEqual(result["return_value"], 0, "Valor de retorno incorreto para teste_declarar_variavel.c")
        self.assertEqual(result["globals"], {}, "Variáveis globais deveriam estar vazias para teste_declarar_variavel.c")

    def test_06_funcoes(self):
        file_path = os.path.join(TEST_FILES_DIR, "teste_funcoes.c")
        result = self._load_and_run_test_file(file_path)
        self.assertEqual(result["return_value"], 1, "Valor de retorno incorreto para teste_funcoes.c")
        self.assertEqual(result["globals"], {}, "Variáveis globais deveriam estar vazias para teste_funcoes.c")

    def test_07_if_else(self):
        file_path = os.path.join(TEST_FILES_DIR, "teste_if_else.c")
        result = self._load_and_run_test_file(file_path)
        self.assertEqual(result["return_value"], 1, "Valor de retorno incorreto para teste_if_else.c")
        self.assertEqual(result["globals"], {}, "Variáveis globais deveriam estar vazias para teste_if_else.c")

    def test_08_operadores_aritmeticos(self):
        file_path = os.path.join(TEST_FILES_DIR, "teste_operadores_aritmeticos.c")
        result = self._load_and_run_test_file(file_path)
        self.assertEqual(result["return_value"], 5, "Valor de retorno incorreto para teste_operadores_aritmeticos.c")
        self.assertEqual(result["globals"], {}, "Variáveis globais deveriam estar vazias para teste_operadores_aritmeticos.c")

    def test_09_operadores_logicos(self):
        file_path = os.path.join(TEST_FILES_DIR, "teste_operadores_logicos.c")
        result = self._load_and_run_test_file(file_path)
        self.assertEqual(result["return_value"], 1, "Valor de retorno incorreto para teste_operadores_logicos.c")
        self.assertEqual(result["globals"], {}, "Variáveis globais deveriam estar vazias para teste_operadores_logicos.c")

    def test_10_ponteiros(self):
        file_path = os.path.join(TEST_FILES_DIR, "teste_ponteiros.c")
        result = self._load_and_run_test_file(file_path)
        self.assertEqual(result["return_value"], 15, "Valor de retorno incorreto para teste_ponteiros.c")
        self.assertEqual(result["globals"], {}, "Variáveis globais deveriam estar vazias para teste_ponteiros.c")

    def test_11_print(self):
        file_path = os.path.join(TEST_FILES_DIR, "teste_print.c")
        result = self._load_and_run_test_file(file_path, mock_input_values=["5"])
        
        self.assertEqual(result["return_value"], 10, "Valor de retorno incorreto para teste_print.c (esperado 5*2)")
        
        actual_stdout = result["stdout"]
        self.assertIn("Digite um número:", actual_stdout, "Esperado 'Digite um número:' no stdout para teste_print.c")
        
        self.assertIn("O dobro de 5 é 10", actual_stdout, "Esperado 'O dobro de 5 é 10' no stdout para teste_print.c")
        
        self.assertEqual(result["globals"], {}, "Variáveis globais deveriam estar vazias para teste_print.c")

    def test_12_return_funcao(self):
        file_path = os.path.join(TEST_FILES_DIR, "teste_return_funcao.c")
        result = self._load_and_run_test_file(file_path)
        self.assertEqual(result["return_value"], 7, "Valor de retorno incorreto para teste_return_funcao.c")
        self.assertEqual(result["globals"], {}, "Variáveis globais deveriam estar vazias para teste_return_funcao.c")

    def test_13_variaveis_globais(self):
        file_path = os.path.join(TEST_FILES_DIR, "teste_variaveis_globais.c")
        result = self._load_and_run_test_file(file_path)
        self.assertEqual(result["return_value"], 2, "Valor de retorno incorreto para teste_variaveis_globais.c")
        self.assertIn('counter', result["globals"], "Variável global 'counter' não encontrada para teste_variaveis_globais.c")
        self.assertEqual(result["globals"]['counter'], 2, "Valor da variável global 'counter' incorreto para teste_variaveis_globais.c")

    def test_14_while(self):
        file_path = os.path.join(TEST_FILES_DIR, "teste_while.c")
        result = self._load_and_run_test_file(file_path)
        self.assertEqual(result["return_value"], 3, "Valor de retorno incorreto para teste_while.c")
        self.assertEqual(result["globals"], {}, "Variáveis globais deveriam estar vazias para teste_while.c")

    def test_15_user_testes_c(self): 
        file_path = os.path.join(PROJECT_DIR, "testes.c")
        result = self._load_and_run_test_file(file_path)
        self.assertEqual(result["return_value"], 1, "Valor de retorno incorreto para testes.c")
        self.assertEqual(result["globals"], {}, "Variáveis globais deveriam estar vazias para testes.c")

if __name__ == '__main__':
    unittest.main()
import unittest
import os
from io import StringIO
import sys

# Adicionar o diretório do projeto ao path para que os módulos possam ser importados
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from parser import parser
from lexer import lexer

# Diretório onde os arquivos de teste com erros estão localizados
TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "Testes_Erros")

class TestParserErrors(unittest.TestCase):

    def setUp(self):
        """
        Este método é executado antes de cada teste.
        Ele redireciona a saída padrão (stdout) para que possamos capturar
        as mensagens de erro impressas pelo parser.
        """
        self.held, sys.stdout = sys.stdout, StringIO()
        # Garante que o diretório de testes de erro exista
        if not os.path.exists(TEST_FILES_DIR):
            os.makedirs(TEST_FILES_DIR)

    def tearDown(self):
        """
        Este método é executado após cada teste.
        Ele restaura a saída padrão original.
        """
        sys.stdout = self.held

    def _run_parser_test(self, c_code_str, expected_error_msg_part):
        """
        Método auxiliar para executar o parser e verificar os resultados.
        """
        # Reinicia o estado do lexer para cada teste
        lexer.lineno = 1
        
        # Executa o parser
        ast = parser.parse(c_code_str, lexer=lexer)

        # 1. Verifica se a AST não foi gerada (retornou None)
        self.assertIsNone(ast, f"O parser deveria retornar None para o código com erro:\n---\n{c_code_str}\n---")

        # 2. Verifica se a mensagem de erro esperada foi impressa
        captured_output = sys.stdout.getvalue()
        self.assertIn(expected_error_msg_part, captured_output, 
                      f"A mensagem de erro esperada '{expected_error_msg_part}' não foi encontrada na saída.\nSaída capturada:\n{captured_output}")

    def test_erro_ponto_virgula_faltando(self):
        """
        Testa um código onde falta um ponto e vírgula entre duas instruções.
        """
        file_path = os.path.join(TEST_FILES_DIR, "erro_ponto_virgula.c")
        with open(file_path, 'r') as f:
            c_code = f.read()
            
        # O parser deve falhar no token 'return' porque esperava um ';'
        self._run_parser_test(c_code, "Erro de sintaxe em 'return'")

    def test_erro_parenteses_desbalanceado(self):
        """
        Testa um código com um parêntese de fechamento faltando em uma condição 'if'.
        """
        file_path = os.path.join(TEST_FILES_DIR, "erro_parenteses.c")
        with open(file_path, 'r') as f:
            c_code = f.read()

        # O parser deve falhar no token '{' porque esperava um ')'
        self._run_parser_test(c_code, "Erro de sintaxe em '{'")

    def test_erro_operador_invalido(self):
        """
        Testa um código com uma expressão inválida (dois operadores seguidos).
        """
        file_path = os.path.join(TEST_FILES_DIR, "erro_operador_invalido.c")
        with open(file_path, 'r') as f:
            c_code = f.read()
            
        # O parser deve falhar no segundo '+'
        self._run_parser_test(c_code, "Erro de sintaxe em '+'")

    def test_erro_fim_de_arquivo_inesperado(self):
        """
        Testa um código onde falta uma chave de fechamento, causando um erro de EOF.
        """
        file_path = os.path.join(TEST_FILES_DIR, "erro_eof.c")
        with open(file_path, 'r') as f:
            c_code = f.read()

        # O parser deve reportar um erro no final do arquivo
        self._run_parser_test(c_code, "Erro de sintaxe no final do arquivo")

if __name__ == '__main__':
    unittest.main()

import unittest
import os
from io import StringIO
import sys

# Adicionar o diretório do projeto ao path para que os módulos possam ser importados
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parser import parser
from lexer import lexer

# Diretório onde os arquivos de teste com erros estão localizados
TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "Testes_Erros")

class TestParserErrors(unittest.TestCase):

    def setUp(self):
        """
        Este método é executado antes de cada teste.
        Ele redireciona a saída padrão (stdout) para que possamos capturar
        as mensagens de erro impressas pelo parser.
        """
        self.held, sys.stdout = sys.stdout, StringIO()
        # Garante que o diretório de testes de erro exista
        if not os.path.exists(TEST_FILES_DIR):
            os.makedirs(TEST_FILES_DIR)

    def tearDown(self):
        """
        Este método é executado após cada teste.
        Ele restaura a saída padrão original.
        """
        sys.stdout = self.held

    def _run_parser_test(self, c_code_str, expected_error_msg_part):
        """
        Método auxiliar para executar o parser e verificar os resultados.
        """
        # Reinicia o estado do lexer para cada teste
        lexer.lineno = 1

        # Executa o parser
        ast = parser.parse(c_code_str, lexer=lexer)

        # 1. Verifica se a AST não foi gerada (retornou None)
        self.assertIsNone(ast, f"O parser deveria retornar None para o código com erro:\n---\n{c_code_str}\n---")

        # 2. Verifica se a mensagem de erro esperada foi impressa
        captured_output = sys.stdout.getvalue()
        self.assertIn(expected_error_msg_part, captured_output,
                      f"A mensagem de erro esperada '{expected_error_msg_part}' não foi encontrada na saída.\nSaída capturada:\n{captured_output}")

    def test_erro_ponto_virgula_faltando(self):
        """
        Testa um código onde falta um ponto e vírgula entre duas instruções.
        """
        file_path = os.path.join(TEST_FILES_DIR, "erro_ponto_virgula.c")
        with open(file_path, 'r') as f:
            c_code = f.read()

        # O parser deve falhar no token 'return' porque esperava um ';'
        self._run_parser_test(c_code, "Erro de sintaxe em 'return'")

    def test_erro_parenteses_desbalanceado(self):
        """
        Testa um código com um parêntese de fechamento faltando em uma condição 'if'.
        """
        file_path = os.path.join(TEST_FILES_DIR, "erro_parenteses.c")
        with open(file_path, 'r') as f:
            c_code = f.read()

        # O parser deve falhar no token '{' porque esperava um ')'
        self._run_parser_test(c_code, "Erro de sintaxe em '{'")

    def test_erro_operador_invalido(self):
        """
        Testa um código com uma expressão inválida (dois operadores seguidos).
        """
        file_path = os.path.join(TEST_FILES_DIR, "erro_operador_invalido.c")
        with open(file_path, 'r') as f:
            c_code = f.read()

        # O parser deve falhar no segundo '+'
        self._run_parser_test(c_code, "Erro de sintaxe em '+'")

    def test_erro_fim_de_arquivo_inesperado(self):
        """
        Testa um código onde falta uma chave de fechamento, causando um erro de EOF.
        """
        file_path = os.path.join(TEST_FILES_DIR, "erro_eof.c")
        with open(file_path, 'r') as f:
            c_code = f.read()

        # O parser deve reportar um erro no final do arquivo
        self._run_parser_test(c_code, "Erro de sintaxe no final do arquivo")

if __name__ == '__main__':
    unittest.main()

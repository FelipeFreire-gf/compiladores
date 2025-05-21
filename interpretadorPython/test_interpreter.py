from interpreter import Interpreter  

interpreter = Interpreter()

address = interpreter.allocate_memory()
print(f"Endereço alocado: {address}")

interpreter.pointers["ptr1"] = address
print(f"Ponteiro 'ptr1' criado, apontando para o endereço {address}")

interpreter.memory[address][0] = 42  
print(f"Valor no endereço {address} após modificação: {interpreter.memory[address][0]}")

pointer_value = interpreter.memory[interpreter.pointers["ptr1"]][0]
print(f"Valor acessado via ponteiro 'ptr1': {pointer_value}")

interpreter.memory[interpreter.pointers["ptr1"]][0] = 99
print(f"Novo valor no endereço {address}: {interpreter.memory[address][0]}")
print(f"Novo valor acessado via ponteiro 'ptr1': {interpreter.memory[interpreter.pointers['ptr1']][0]}")

# Verificação final
assert interpreter.memory[address][0] == 99, "O valor na memória não foi atualizado corretamente."
assert pointer_value == 42, "O valor inicial acessado via ponteiro está incorreto."
print("Todos os testes passaram!")
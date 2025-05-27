#include <stdio.h>

int calcular_dobro(int num) {
    return num * 2;
}

int main() {
    print("Digite um número:");
    int x = input();
    int resultado = calcular_dobro(x);
    print("O dobro de", x, "é", resultado);
    return resultado;
}
int main() {
    int y = 5;
    int *ptr = &y;  // ptr armazena o endereço de y
    *ptr = 15;      // altera o valor de y para 15
    return y;       // retorna 15
}
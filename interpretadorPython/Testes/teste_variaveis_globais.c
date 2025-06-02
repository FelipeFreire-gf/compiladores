int counter = 0;

void increment() {
    counter = counter + 1;
}

int main() {
    increment();
    increment();
    return counter; // Retorna 2
}
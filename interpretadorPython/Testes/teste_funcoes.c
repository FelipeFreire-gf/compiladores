int eh_par(int num) {
    if (num % 2 == 0) {
        return 1;
    } else {
        return 0;
    }
}

int main() {
    return eh_par(10) + eh_par(7);
}
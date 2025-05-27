int main() {
    int x = 1;
    {
        int x = 2;
        {
            int x = 3;
            {
                int x = 4;
            }
            return x;  // Deve retornar 3 (escopo atual)
        }
    }
}
echo "Executando testes de análise semântica..."

make > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "Erro na compilação. Verifique o código."
    exit 1
fi

for file in tests/*.txt; do
    echo "=========================="
    echo "Arquivo: $file"
    echo "--------------------------"
    ./interpretador < "$file"
    echo ""
done
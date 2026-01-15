p1

compilar:

g++ -std=c++11 -O3 -Wall p1.cpp -o p1 -lm

testar:

./p1 < teste.txt

testar todos os testes

clear && g++ -std=c++11 -O3 -Wall p1.cpp -o p1 -lm && echo 'Comparing outputs with *.sol.out files'; for f in tests/*.in; do base="${f%.in}"; sol="${base}.sol.out"; if [ -f "$sol" ]; then printf "== %s ==\n" "$f"; timeout 10s ./p1 < "$f" > /tmp/my_out 2>/dev/null || { code=$?; if [ $code -eq 124 ]; then echo "TIMEOUT"; continue; else echo "EXIT $code"; continue; fi; }; if diff -q "$sol" /tmp/my_out > /dev/null 2>&1; then echo "MATCH"; else echo "DIFF:"; echo "--- Expected ($sol):"; head -20 "$sol"; echo "--- Got:"; head -20 /tmp/my_out; fi; else echo "== $f == (no .sol.out)"; fi; done; echo 'Done.'


GERADOR DE INSTANCIAS

compilar:

g++ -std=c++11 -O3 -Wall gerador_p1.cpp -o gerador_p1 -lm

testar:

./gerador_p1 N M

N = nº aminoacidos
M = valor máximo da energia potencial de cada aminoacido


#include <cstdio>
#include <functional>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

#define P 1  // polar
#define N 2  // não-polar
#define A 3  // ácido
#define B 4  // base
#define T 5  // terminal

int charToIndex(char c) {
    switch (c) {
        case 'P':
            return P;
        case 'N':
            return N;
        case 'A':
            return A;
        case 'B':
            return B;
        case 'T':
            return T;
        default:
            return 0;
    }
}

vector<vector<int>> createAffinity() {
    const int SIZE = 6;
    vector<vector<int>> af(SIZE, vector<int>(SIZE, 0));

    af[P] = {0, 1, 3, 1, 3, 1};
    af[N] = {0, 5, 1, 0, 1, 1};
    af[A] = {0, 0, 1, 0, 4, 1};
    af[B] = {0, 1, 3, 2, 3, 1};
    af[T] = {0, 1, 1, 1, 1, 1};

    return af;
}

void readPotentials(int n, vector<unsigned long long>& pot) {
    pot.assign(n + 2, 1);
    for (int i = 1; i <= n; ++i) {
        cin >> pot[i];
    }
}

void readClasses(int n, vector<char>& cl) {
    string s;
    cin >> s;
    cl.assign(n + 2, 'T');
    for (int i = 1; i <= n; ++i) {
        if ((size_t)(i - 1) < s.length()) {
            cl[i] = s[i - 1];
        }
    }
}

void showResults(unsigned long long energy, const vector<int>& order) {
    printf("%llu\n", energy);
    for (size_t i = 0; i < order.size(); ++i) {
        printf("%d", order[i]);
        if (i < order.size() - 1) {
            printf(" ");
        }
    }
    printf("\n");
}

void solve(int n, const vector<vector<int>>& af, const vector<char>& cl,
           const vector<unsigned long long>& pot) {
    int sz = n + 2;

    vector<vector<unsigned long long>> dp(sz,
                                          vector<unsigned long long>(sz, 0));
    vector<vector<int>> split(sz, vector<int>(sz, -1));

    vector<int> clIdx(sz);
    for (int i = 0; i < sz; ++i)
        clIdx[i] = charToIndex(cl[i]);

    for (int len = 2; len < sz; ++len) {
        int maxL = sz - len;
        for (int l = 0; l < maxL; ++l) {
            int r = l + len;
            unsigned long long best = 0;
            int best_k = -1;

            int idx_left = clIdx[l];
            int idx_right = clIdx[r];

            for (int chosen = l + 1; chosen <= r - 1; ++chosen) {
                unsigned long long dp_left = dp[l][chosen];
                unsigned long long dp_right = dp[chosen][r];
                int idx_chosen = clIdx[chosen];

                unsigned long long removal_energy =
                    pot[l] * af[idx_left][idx_chosen] * pot[chosen] +
                    pot[chosen] * af[idx_chosen][idx_right] * pot[r];

                unsigned long long candidateValue =
                    dp_left + dp_right + removal_energy;

                if (candidateValue >= best) {
                    best = candidateValue;
                    best_k = chosen;
                }
            }

            dp[l][r] = best;
            split[l][r] = best_k;
        }
    }

    vector<int> order;
    function<void(int, int)> buildOrder = [&](int l, int r) {
        int k = split[l][r];
        if (k == -1)
            return;

        buildOrder(l, k);
        buildOrder(k, r);

        order.push_back(k);
    };

    buildOrder(0, n + 1);

    unsigned long long energy_total = dp[0][n + 1];
    showResults(energy_total, order);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    vector<unsigned long long> potenciais;
    vector<char> classes;

    cin >> n;
    readPotentials(n, potenciais);
    readClasses(n, classes);

    vector<vector<int>> af = createAffinity();

    solve(n, af, classes, potenciais);

    return 0;
}
template <typename T>
map<T, T> Factorize_naive(T n){
    map<T, T> ans = {};
    T sqrt_n = static_cast<T>(sqrt(n));
    for (T p = 2; p <= sqrt_n; p++) {
        if (n % p == 0) {
            T ct = 0;
            while (n % p == 0) {
                ct += 1;
                n /= p;
            }
            ans[p] = ct;
        }
        if (n == 1) break;
    }
    if (n > 1) ans[n] = 1;
    return ans;
}


template <typename T>
map<T, T> Factorize(T n) {
    if (n < 1000) return Factorize_naive(n);
    
    map<T, T> ans = {};
    
    // divide 2
    if (n % 2 == 0) {
        ans[2] = __builtin_ctz(n);
        n >>= __builtin_ctz(n);
    }
    
    if (n == 1) return ans;
    
    // Miller-Rabin test
    bool is_composite = false;
    size_t ct_2 = __builtin_ctz(n - 1);
    for (__uint128_t a = 2; a < n && a < 39; a++) {
        __uint128_t v_now = pow(a, static_cast<__uint128_t>(n - 1) >> ct_2, static_cast<__uint128_t>(n)) % n;
        if (v_now == 1 || v_now == n - 1) continue;
        for (size_t c = 1; c <= ct_2; c++) {
            v_now *= v_now;
            v_now %= n;
            if (v_now == n - 1) break;
            if (c == ct_2) is_composite = true;
        }
        if (is_composite) break;
    }
    if (!is_composite) { // n is prime
        if (ans.count(n)) ans[n] += 1;
        else ans[n] = 1;
        return ans;
    }
    
    // Froid detection
    for (;;) {
        __uint128_t a = static_cast<__uint128_t>(rand()) % n;
        __uint128_t b = static_cast<__uint128_t>(rand()) % n;
        
        __uint128_t x, y;
        x = a;
        y = a;
        while (true) {
            x = (x * x + b) % n;
            y = (y * y + b) % n;
            y = (y * y + b) % n;
                
            auto [_1, _2, d] = ext_gcd(static_cast<__uint128_t>(y > x ? y - x : x - y), static_cast<__uint128_t>(n));
            
            print("  :", n, a, b, x, y, d);
            if (d == n) break;
            if (d == 1) continue;
            if ((1 < d) && (d < n)) {
                auto m1 = Factorize(d);
                auto m2 = Factorize(n / d);
                
                for (auto [p, c] : m1) {
                    if (ans.count(p)) ans[p] += c;
                    else ans[p] = c;
                }
                for (auto [p, c] : m2) {
                    if (ans.count(p)) ans[p] += c;
                    else ans[p] = c;
                }
                return ans;
            }
        }
    }
}

int main() {
    
    long long L = 9ULL * pow(10LL, 9);
    long long R = L + 2;
    
    print(Factorize(9000000001));
    /*
    auto t1 = chrono::system_clock::now();
    rep_range(i, L, R) Factorize(i);
    auto t2 = chrono::system_clock::now();
    chrono::duration<double, std::milli> elapsed_1 = t2 - t1;
    cout << elapsed_1.count() << "ms" << std::endl;
    */
    
    /*
    auto t3 = chrono::system_clock::now();
    rep_range(i, L, R) Factorize_naive(i);
    auto t4 = chrono::system_clock::now();
    chrono::duration<double, std::milli> elapsed_2 = t4 - t3;
    cout << elapsed_2.count() << "ms" << std::endl;
    */
    
}

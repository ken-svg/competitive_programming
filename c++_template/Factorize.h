unordered_map<long long, long long> Factorize_naive(long long n){
    unordered_map<long long, long long> ans = {};
    long long sqrt_n = static_cast<long long>(sqrt(n));
    for (long long p = 2; p * p <= n; p++) {
        if (n % p == 0) {
            long long ct = 0;
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

random_device rd;
mt19937_64 mt(rd());
uniform_int_distribution<uint64_t> dist(0, UINT_MAX);

unordered_map<long long, long long> Factorize_small(long long n) {
    // for n <= 1e9
    if (n < 1e6) return Factorize_naive(n);
    
    unordered_map<long long, long long> ans;
    
    // divide 2
    while (n % 2 == 0) {
        ans[2] = __builtin_ctz(n);
        n >>= __builtin_ctz(n);
    }
    
    if (n == 1) return ans;
    
    // Miller-Rabin test
    bool is_composite = false;
    size_t ct_2 = __builtin_ctz(n - 1);
    for (long long a : {2ULL, 325ULL, 9375ULL, 28178ULL, 450775ULL, 9780504ULL, 1795265022ULL}) {
        a = a % n;
        if (a == 0) continue;
        long long v_now = 1;
        long long b = (n - 1) >> ct_2;
        long long q = a;
        while (b > 0) {
            if (b % 2 == 1) {
                v_now = (v_now * q) % n;
            }
            q = (q * q) % n;
            b /= 2;
        }
        
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
    
    long long r = 1 << 32;
    
    // Froid detection
    for (;;) {
        long long a = dist(mt) % n;
        long long b = dist(mt) % n;
        long long a2 = dist(mt) % n;
        long long b2 = dist(mt) % n;
        
        long long x, y;
        long long x2, y2;
        x = a;
        y = a;
        x2 = a2;
        y2 = a2;
        
        while (true) {
            x = (x * x + b) % n;
            y = (y * y + b) % n;
            y = (y * y + b) % n;
                
            long long d = (x > y) ? (x - y) : (y - x);
            long long y0 = n;
            while (d != 0 && y0 % d != 0) {
                y0 %= d;
                swap(d, y0);
            }
            
            x2 = (x2 * x2 + b2) % n;
            y2 = (y2 * y2 + b2) % n;
            y2 = (y2 * y2 + b2) % n;
                
            // derive gcd
            long long d2 = (x2 > y2) ? (x2 - y2) : (y2 - x2);
            long long y02 = n;
            //if (d > y0) swap(d, y0);
            while (d2 != 0 && y02 % d2 != 0) {
                y02 %= d2;
                swap(d2, y02);
            }
            
            if (d == 0) {
                a = dist(mt) % n;
                b = dist(mt) % n;
                x = (a * a + b) % n;
                y = (x * x + b) % n;
            }
            if (d2 == 0) {
                a2 = dist(mt) % n;
                b2 = dist(mt) % n;
                x2 = (a2 * a2 + b2) % n;
                y2 = (x2 * x2 + b2) % n;
            }
            
            if (d <= 1) d = d2;
            if (d <= 1) continue;
            n /= d;
                
            for (auto [p, c] : Factorize_small(d)) {
                if (ans.count(p)) ans[p] += c;
                else ans[p] = c;
                while (n % p == 0) {
                    ans[p] += 1;
                    n /= p;
                }
            }
                
            for (auto [p, c] : Factorize_small(n)) {
                if (ans.count(p)) ans[p] += c;
                else ans[p] = c;
            }
            return ans;
        }
    }
}

unordered_map<long long, long long> Factorize(long long n) {
    if (n < 1e6) return Factorize_naive(n);
    if (n < 1e9) return Factorize_small(n);
    
    unordered_map<long long, long long> ans;
    
    // divide 2
    while (n % 2 == 0) {
        ans[2] = __builtin_ctz(n);
        n >>= __builtin_ctz(n);
    }
    
    if (n == 1) return ans;
    
    
    // Miller-Rabin test
    bool is_composite = false;
    size_t ct_2 = __builtin_ctz(n - 1);
    __uint128_t n_uns = n;
    for (__uint128_t a : {2ULL, 325ULL, 9375ULL, 28178ULL, 450775ULL, 9780504ULL, 1795265022ULL}) {
        a = a % n_uns;
        if (a == 0) continue;
        __uint128_t v_now = 1;
        __uint128_t b = (n - 1) >> ct_2;
        __uint128_t q = a;
        while (b > 0) {
            if (b % 2 == 1) {
                v_now = (v_now * q) % n_uns;
            }
            q = (q * q) % n_uns;
            b /= 2;
        }
        
        if (v_now == 1 || v_now == n_uns - 1) continue;
        for (size_t c = 1; c <= ct_2; c++) {
            v_now *= v_now;
            v_now %= n_uns;
            if (v_now == n_uns - 1) break;
            if (c == ct_2) is_composite = true;
        }
        if (is_composite) break;
    }
    if (!is_composite) { // n is prime
        if (ans.count(n_uns)) ans[n_uns] += 1;
        else ans[n_uns] = 1;
        return ans;
    }
    
    // Froid detection
    for (;;) {
        __uint128_t a = static_cast<__uint128_t>(dist(mt)) % n_uns;
        __uint128_t b = static_cast<__uint128_t>(dist(mt)) % n_uns;
        __uint128_t a2 = static_cast<__uint128_t>(dist(mt)) % n_uns;
        __uint128_t b2 = static_cast<__uint128_t>(dist(mt)) % n_uns;
        
        __uint128_t x, y;
        __uint128_t x2, y2;
        x = a;
        y = a;
        x2 = a2;
        y2 = a2;
        
        while (true) {
            x = (x * x + b) % n_uns;
            y = (y * y + b) % n_uns;
            y = (y * y + b) % n_uns;
                
            // derive gcd
            __uint128_t d = (x > y) ? (x - y) : (y - x);
            __uint128_t y0 = n_uns;
            while (d != 0 && y0 % d != 0) {
                y0 %= d;
                swap(d, y0);
            }
            
            x2 = (x2 * x2 + b2) % n_uns;
            y2 = (y2 * y2 + b2) % n_uns;
            y2 = (y2 * y2 + b2) % n_uns;
                
            // derive gcd
            __uint128_t d2 = (x2 > y2) ? (x2 - y2) : (y2 - x2);
            __uint128_t y02 = n_uns;
            while (d2 != 0 && y02 % d2 != 0) {
                y02 %= d2;
                swap(d2, y02);
            }
            
            if (d == 0) {
                a = static_cast<__uint128_t>(dist(mt)) % n_uns;
                b = static_cast<__uint128_t>(dist(mt)) % n_uns;
                x = (a * a + b) % n_uns;
                y = (x * x + b) % n_uns;
            }
            if (d2 == 0) {
                a2 = static_cast<__uint128_t>(dist(mt)) % n_uns;
                b2 = static_cast<__uint128_t>(dist(mt)) % n_uns;
                x2 = (a2 * a2 + b2) % n_uns;
                y2 = (x2 * x2 + b2) % n_uns;
            }
            
            if (d <= 1) d = d2;
            if (d <= 1) continue;
            n_uns /= d;
                
            for (auto [p, c] : Factorize(d)) {
                if (ans.count(p)) ans[p] += c;
                else ans[p] = c;
                while (n_uns % p == 0) {
                    ans[p] += 1;
                    n_uns /= p;
                }
            }
                
            for (auto [p, c] : Factorize(n_uns)) {
                if (ans.count(p)) ans[p] += c;
                else ans[p] = c;
            }
            return ans;
        }
    }
}
unordered_map<long long, long long> Factorize_naive(long long n){
    unordered_map<long long, long long> ans = {};
    long long sqrt_n = static_cast<long long>(sqrt(n));
    for (long long p = 2; p * p <= n; p++) {
        if (n % p == 0) {
            long long ct = 0;
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


unordered_map<long long, long long> Factorize(long long n) {
    if (n < 1e7) return Factorize_naive(n);
    
    unordered_map<long long, long long> ans;
    
    // divide 2
    while (n % 2 == 0) {
        ans[2] = __builtin_ctz(n);
        n >>= __builtin_ctz(n);
    }
    
    if (n == 1) return ans;
    
    
    // Miller-Rabin test
    bool is_composite = false;
    size_t ct_2 = __builtin_ctz(n - 1);
    // print(ct_2);
    __uint128_t n_uns = n;
    for (__uint128_t a : {2ULL, 325ULL, 9375ULL, 28178ULL, 450775ULL, 9780504ULL, 1795265022ULL}) {
        
        // pow(a, (n - 1) >> ct_2) % n
        __uint128_t v_now = 1;
        __uint128_t b = (n - 1) >> ct_2;
        __uint128_t q = a;
        while (b > 0) {
            if (b % 2 == 1) {
                v_now = (v_now * q) % n_uns;
            }
            q = (q * q) % n_uns;
            b /= 2;
        }
        
        if (v_now == 1 || v_now == n_uns - 1) continue;
        for (size_t c = 1; c <= ct_2; c++) {
            v_now *= v_now;
            v_now %= n_uns;
            // print(ll(n_uns), ll(a), c, ll(v_now));
            if (v_now == n_uns - 1) break;
            if (c == ct_2) is_composite = true;
        }
        if (is_composite) break;
    }
    if (!is_composite) { // n is prime
        if (ans.count(n_uns)) ans[n_uns] += 1;
        else ans[n_uns] = 1;
        return ans;
    }
    
    random_device rd;
    mt19937_64 mt(rd());
    uniform_int_distribution<uint64_t> dist(0, UINT_MAX);
    
    // Froid detection
    for (size_t c2 = 0; c2 < 1e2; c2++) {
        __uint128_t a = static_cast<__uint128_t>(dist(mt)) % n_uns;
        __uint128_t b = static_cast<__uint128_t>(dist(mt)) % n_uns;
        //__uint128_t c = static_cast<__uint128_t>(dist(mt)) % n_uns;
        
        __uint128_t x, y;
        x = a;
        y = a;
        size_t cv = 0;
        while (cv < 6e4) {
            cv += 1;
            
            x = (x * x + b) % n_uns;
            y = (y * y + b) % n_uns;
            y = (y * y + b) % n_uns;
                
            // derive gcd
            __uint128_t d = (x > y) ? (x - y) : (y - x);
            __uint128_t y0 = n_uns;
            if (d > y0) swap(d, y0);
            while (d != 0 && y0 % d != 0) {
                y0 %= d;
                swap(d, y0);
            }
            // print(ll(n_uns), ll(x), ll(y), ll(d));
            
            if (d == 0) break;
            if (d == 1) continue;
            if ((1 < d) && (d < n_uns)) {
                auto m1 = Factorize(d);
                __uint128_t n_res = n_uns / d;
                
                for (auto [p, c] : m1) {
                    if (ans.count(p)) ans[p] += c;
                    else ans[p] = c;
                    while (n_res % p == 0) {
                        ans[p] += 1;
                        n_res /= p;
                    }
                }
                
                auto m2 = Factorize(n_res);
                for (auto [p, c] : m2) {
                    if (ans.count(p)) ans[p] += c;
                    else ans[p] = c;
                }
                return ans;
            }
        }
    }
    ans[static_cast<loon long>(n_uns)] = 1;
    return ans;
}

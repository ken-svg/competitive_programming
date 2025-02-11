template <typename T>
T Chinese_Remainder_Theorem(vector<T>& R, vector<T>& M) {
    size_t n = R.size();
    T rem = R[0];
    T mod = M[0];
    rem %= mod;
    for (size_t i = 1; i < n; i++) {
        T next_rem = R[i];
        T next_mod = M[i];
        auto [p, q, d] = ext_gcd(mod, next_mod);
        if ((next_rem - rem) % d != 0) return -1;
        T s = (next_rem - rem) / d;
        rem += s * mod * p;
        mod *= next_mod;
        rem %= mod;
        if (rem < 0) rem += mod;
    }
    return rem;
}

// mod 冪乗
template <typename T>
T pow(T x, T n, const T mod) {
  T ret = 1;
  while (n > 0) {
    if (n & 1) {
      (ret *= x) %= p;
    }
    (x *= x) %= p;
    n >>= 1;
  }
  return ret;
}

// ユークリッド互助法
// 戻り値dは最小公約数。 参照変数x, yには、ax + by = dの解が入る
template <typename T>
T ext_gcd(T a, T b, T &x, T &y) {
  if (b == 0) {
    x = 1;
    y = 0;
    return a;
  }
  T d = ext_gcd(b, a % b, y, x);
  y -= (a / b) * x;
  return d;
}

// modでの階乗 (ext_gcdを引くこと！！)
template <typename T>
void mod_factorial(vector<T> &F, vector<T> &F_inv, T N, const T mod){
  F = {1};
  F_inv = {1};
  for (T i = 1; i < N; i++){
    F.push_back((F.back() * i) % mod);
    T i_inv, dum;
    ext_gcd(i, mod, i_inv, dum);
    F_inv.push_back((F_inv.back() * i_inv) % mod);
  }
  return ;
}

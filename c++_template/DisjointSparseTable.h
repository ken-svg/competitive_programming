template <typename T>
class DisjointSparseTable {
private:
    using F = function<T(const T&, const T&)>; // 集約関数型
    vector<vector<T>> table;             // Disjoint Sparse Table
    F func;                                        // 集約関数
    ll n;                                      // 要素数

public:
    // コンストラクタ1: 要素数、初期値、集約関数を受け取る
    DisjointSparseTable(ll size, T init_value, F f = [](const T& a, const T& b) { return min(a, b); }) 
        : func(f), n(size) {
        build(vector<T>(size, init_value));
    }

    // コンストラクタ2: vectorと集約関数を受け取る
    DisjointSparseTable(const std::vector<T>& v, F f = [](const T& a, const T& b) { return min(a, b); }) 
        : func(f), n(v.size()) {
        build(v);
    }

    // 区間 [l, r) に対するクエリ
    T apply(ll l, ll r) const {
        assert(l < r && r <= n);
        if (l + 1 == r) return table[0][l]; // 1要素の場合
        ll k = 63 - __builtin_clzll(l ^ (r - 1)); // lとr-1の異なるビットの最上位桁
        return func(table[k][l], table[k][r - 1]);
    }

private:
    // Disjoint Sparse Table の構築
    void build(const std::vector<T>& v) {
        table = {};

        // 0段目: 元の配列
        table.push_back(vector<T>(n));
        for (ll i = 0; i < n; ++i) {
            table[0][i] = v[i];
        }
        
        // 各段を構築
        for (ll k = 1; (1u << k) <= n; ++k) {
            ll len = 1 << (k + 1); // セグメントの長さ
            table.push_back(vector<T>(n));
            
            for (ll i = 0; i < n; i += len) {
                
                ll mid = min(i + (len >> 1), n);
                ll right = min(i + len, n);

                // 左側 (mid - 1 から i 方向)
                table[k][mid - 1] = v[mid - 1];
                for (ll j = mid - 2; j >= i; --j) { 
                    table[k][j] = func(v[j], table[k][j + 1]);
                }

                // 右側 (mid から right 方向)
                if (mid < n) {
                    table[k][mid] = v[mid];
                    for (ll j = mid + 1; j < right; ++j) {
                        table[k][j] = func(table[k][j - 1], v[j]);
                    }
                }
            }
        }
    }
};

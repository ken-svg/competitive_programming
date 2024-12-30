template <typename T, typename S>
class LazySegmentTree {
private:
    int n, size;  // n: 内部の2冪サイズ, size: 元のデータサイズ
    vector<T> tree;
    vector<S> lazy;
    function<T(T, T)> op;          // 演算
    T op_id;                       // 演算単位元
    function<T(T, S)> act;         // 作用
    function<S(S, S)> cp;          // 作用の合成
    S act_id;                      // 作用の単位元

    void eval(int k, int l, int r) {
        if (lazy[k] == act_id) return;  // 遅延がなければ何もしない
        tree[k] = act(tree[k], lazy[k]);
        if (r - l > 1) {  // 葉でない場合、遅延を子ノードに伝播
            lazy[2 * k] = cp(lazy[2 * k], lazy[k]);
            lazy[2 * k + 1] = cp(lazy[2 * k + 1], lazy[k]);
        }
        lazy[k] = act_id;  // 自分の遅延をクリア
    }

    void action(int a, int b, S x, int k, int l, int r) {
        eval(k, l, r);
        if (a >= r || b <= l) return;  // 完全に外側
        if (a <= l && r <= b) {  // 完全に内側
            lazy[k] = cp(lazy[k], x);
            eval(k, l, r);
        } else {  // 部分的に重なる場合
            int m = (l + r) / 2;
            action(a, b, x, 2 * k, l, m);
            action(a, b, x, 2 * k + 1, m, r);
            tree[k] = op(tree[2 * k], tree[2 * k + 1]);
        }
    }

    T apply(int a, int b, int k, int l, int r) {
        eval(k, l, r);
        if (a >= r || b <= l) return op_id;  // 完全に外側
        if (a <= l && r <= b) return tree[k];  // 完全に内側
        int m = (l + r) / 2;
        T vl = apply(a, b, 2 * k, l, m);
        T vr = apply(a, b, 2 * k + 1, m, r);
        return op(vl, vr);
    }

public:
    // コンストラクタ (サイズ指定)
    LazySegmentTree(int size_, 
                    function<T(T, T)> op = [](T a, T b) { return min(a, b); }, 
                    T op_id = numeric_limits<T>::max(),
                    function<T(T, S)> act = [](T x, S a) { return (a == S(-1) ? x : T(a)); },
                    function<S(S, S)> cp = [](S a, S b) { return (b == S(-1) ? a : b); },
                    S act_id = S(-1)) 
        : size(size_), op(op), op_id(op_id), act(act), cp(cp), act_id(act_id) {
        n = 1;
        while (n < size) n *= 2;
        tree.assign(2 * n, op_id);  // 根を1とするため2*nに
        lazy.assign(2 * n, act_id);
    }

    // コンストラクタ (データ指定)
    LazySegmentTree(const vector<T>& data, 
                    function<T(T, T)> op = [](T a, T b) { return min(a, b); }, 
                    T op_id = numeric_limits<T>::max(),
                    function<T(T, S)> act = [](T x, S a) { return (a == S(-1) ? x : T(a)); },
                    function<S(S, S)> cp = [](S a, S b) { return (b == S(-1) ? a : b); },
                    S act_id = S(-1)) 
        : LazySegmentTree(data.size(), op, op_id, act, cp, act_id) {
        for (int i = 0; i < data.size(); ++i) tree[n + i] = data[i];
        for (int i = n - 1; i >= 1; --i) tree[i] = op(tree[2 * i], tree[2 * i + 1]);
    }

    // 区間更新
    void action(int a, int b, S x) {
        action(a, b, x, 1, 0, n);
    }

    // 区間クエリ
    T apply(int a, int b) {
        return apply(a, b, 1, 0, n);
    }
};

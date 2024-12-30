template<typename T>
class SegmentTree {
private:
    int n;
    int original_n;
    vector<T> tree;
    function<T(T, T)> op;
    T identity;

    void build(const vector<T>& data) {
        for (int i = 0; i < data.size(); ++i) {
            tree[n + i] = data[i];
        }
        for (int i = data.size(); i < n; ++i) {
            tree[n + i] = identity;
        }
        for (int i = n - 1; i > 0; --i) {
            tree[i] = op(tree[2 * i], tree[2 * i + 1]);
        }
    }

    int nextPowerOfTwo(int x) {
        if ((x & (x - 1)) == 0) return x;
        int power = 1;
        while (power < x) power <<= 1;
        return power;
    }

public:
    // Constructor with size and optional operation and identity
    SegmentTree(int size, function<T(T, T)> operation = plus<T>(), T id = T())
        : op(operation), identity(id) {
        n = nextPowerOfTwo(size);
        original_n = size;
        tree.resize(2 * n, id);
    }

    // Constructor with vector and optional operation and identity
    SegmentTree(const vector<T>& data, function<T(T, T)> operation = plus<T>(), T id = T())
        : op(operation), identity(id) {
        n = nextPowerOfTwo(data.size());
        original_n = data.size();
        tree.resize(2 * n, id);
        build(data);
    }

    // Update a single point
    void update(int idx, T value) {
        idx += n;
        tree[idx] = value;
        while (idx > 1) {
            idx >>= 1;
            tree[idx] = op(tree[2 * idx], tree[2 * idx + 1]);
        }
    }

    // Query a range [l, r)
    T apply(int l, int r) const {
        l += n;
        r += n;
        T res_left = identity;
        T res_right = identity;
        while (l < r) {
            if (l % 2 == 1) {
                res_left = op(res_left, tree[l++]);
            }
            if (r % 2 == 1) {
                res_right = op(tree[--r], res_right);
            }
            l >>= 1;
            r >>= 1;
        }
        return op(res_left, res_right);
    }
    
    int bisect_left(T v, int l = 0) {
        //apply(l, r) < vなる最大のrを求める
        if (apply(l, n) < v) return original_n;  // 全体の演算結果がv未満ならnを返す
        T accumulated = identity;
        int pos = l + n;
        // 親方向への探索
        while (pos > 1) {  // 根ノードに到達するまで
            if (pos % 2 == 1) {  // 右の子である場合
                if (op(accumulated, tree[pos]) < v) {
                    accumulated = op(accumulated, tree[pos]);
                    pos++;  // 次のノード（右側）に進む
                } else {
                    break;  // 探索の目的を満たしたので終了
                }
            }
            pos /= 2;  // 親ノードに移動
        }
        
        // 子方向への探索
        while (pos < n) {  // 葉に到達するまで探索
            int left_child = 2 * pos;
            if (op(accumulated, tree[left_child]) < v) {
                accumulated = op(accumulated, tree[left_child]);
                pos = left_child + 1;  // 右子ノードに進む
            } else {
                pos = left_child;  // 左子ノードに進む
            }
        }
        return (pos - n);  // 0-based のインデックスを返す
    }
    
    int bisect_left_cond(function<bool(T)> cond, int l = 0) {
        // cond(apply(l, r)) が true となる最大のrを求める
        if (cond(apply(l, n))) return original_n;  // 全体の演算結果が条件を満たすならnを返す
        T accumulated = identity;
        int pos = l + n;
        // 親方向への探索
        while (pos > 1) {  // 根ノードに到達するまで
            if (pos % 2 == 1) {  // 右の子である場合
                if (cond(op(accumulated, tree[pos]))) {
                    accumulated = op(accumulated, tree[pos]);
                    pos++;  // 次のノード（右側）に進む
                } else {
                    break;  // 探索の目的を満たしたので終了
                }
            }
            pos /= 2;  // 親ノードに移動
        }
        
        // 子方向への探索
        while (pos < n) {  // 葉に到達するまで探索
            int left_child = 2 * pos;
            if (cond(op(accumulated, tree[left_child]))) {
                accumulated = op(accumulated, tree[left_child]);
                pos = left_child + 1;  // 右子ノードに進む
            } else {
                pos = left_child;  // 左子ノードに進む
            }
        }
        return (pos - n);  // 0-based のインデックスを返す
    }
};

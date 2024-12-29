template <typename T>
class SegmentTree {
private:
    int n;
    vector<T> tree;
    function<T(T, T)> operation; // 演算
    T identity;                  // 単位元

    // ツリーを構築する
    void construct(const vector<T>& data, int node, int start, int end) {
        if (start == end) {
            // 葉ノード
            tree[node] = data[start];
        } else {
            int mid = (start + end) / 2;
            construct(data, 2 * node, start, mid);
            construct(data, 2 * node + 1, mid + 1, end);
            tree[node] = operation(tree[2 * node], tree[2 * node + 1]);
        }
    }

    // 一点更新
    void update(int node, int start, int end, int idx, T val) {
        if (start == end) {
            // 葉ノードを更新
            tree[node] = val;
        } else {
            int mid = (start + end) / 2;
            if (idx <= mid) {
                update(2 * node, start, mid, idx, val);
            } else {
                update(2 * node + 1, mid + 1, end, idx, val);
            }
            tree[node] = operation(tree[2 * node], tree[2 * node + 1]);
        }
    }

    // 区間演算
    T apply(int node, int start, int end, int l, int r) {
        if (r < start || l > end) {
            // 範囲外
            return identity;
        }
        if (l <= start && end <= r) {
            // 完全に範囲内
            return tree[node];
        }
        // 部分的に重なる場合、左右の子ノードを再帰的に計算
        int mid = (start + end) / 2;
        return operation(apply(2 * node, start, mid, l, r),
                         apply(2 * node + 1, mid + 1, end, l, r));
    }

public:
    // コンストラクタ
    SegmentTree(const vector<T>& data,
                function<T(T, T)> op = [](T a, T b) { return a + b; },
                T id = T()) : operation(op), identity(id) {
        n = data.size();
        tree.assign(4 * n, identity);
        construct(data, 1, 0, n - 1);
    }

    void update(int idx, T val) {
        update(1, 0, n - 1, idx, val);
    }

    T apply(int l, int r) {
        return apply(1, 0, n - 1, l, r);
    }
};

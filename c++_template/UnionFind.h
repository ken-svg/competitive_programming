class UnionFind {
public:
    // コンストラクタ: n は要素数
    UnionFind(int n) {
        parent.resize(n);
        for (int i = 0; i < n; ++i) {
            parent[i] = -1;  // 初期状態では各要素が親で、サイズは -1（自己を親とする）
        }
    }

    // 要素 x が属する連結成分の代表元を返す（経路圧縮あり）
    int find(int x) {
        if (parent[x] < 0) {
            return x;  // 親が負の値なら、xが代表元（自分自身を親としている）
        }
        // 経路圧縮
        parent[x] = find(parent[x]);
        return parent[x];
    }

    // x と y の連結成分を統合する（ランクによる統合）
    void merge(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);

        if (rootX != rootY) {
            // ランクによる統合
            if (parent[rootX] < parent[rootY]) {  // rootX の方が大きい（負の値なので絶対値が大きい）
                parent[rootX] += parent[rootY];  // rootY を rootX に統合
                parent[rootY] = rootX;  // rootY の親を rootX に設定
            } else {
                parent[rootY] += parent[rootX];  // rootX を rootY に統合
                parent[rootX] = rootY;  // rootX の親を rootY に設定
            }
        }
    }

    // x と y が同じ連結成分に属しているかを判定する
    bool same(int x, int y) {
        return find(x) == find(y);
    }

    // 要素 x が属する連結成分のサイズを返す
    int size(int x) {
        int rootX = find(x);
        return -parent[rootX];  // 親が負の値の場合、その絶対値がサイズになる
    }

private:
    vector<int> parent;  // 親ノード（負の値の場合、その絶対値が連結成分のサイズ）
};

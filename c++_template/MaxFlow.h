// 1. Dinic法(O(V^2 E))
//  計算量について:
//   辺の容量平均がkのとき、O(k E^(3/2))かつO(k N^(3/2)E)
//   さらに頂点の容量(出入のうち小さい方)の平均がkのとき、O(k N^(1/2)E)
//    *とくに二部マッチングでは0(N^(1/2) E)
//    *kは平均なので、定数個の例外を許す

class MaxFlow {
private:
    int V; // 頂点数

    vector<vector<int>> adj; // 隣接リスト (辺のインデックスを持つ)
    vector<int> level; // レベルグラフ用
    vector<int> start; // DFS用開始点
    vector<vector<ll>> edges; // {from, to, capacity, flow}

    // BFSによるレベルグラフの構築
    bool buildLevelGraph(int source, int sink) {
        fill(level.begin(), level.end(), -1);
        level[source] = 0;
        queue<int> q;
        q.push(source);

        while (!q.empty()) {
            int u = q.front();
            q.pop();

            for (int idx : adj[u]) {
                auto& e = edges[idx];
                if (level[e[1]] == -1 && e[3] < e[2]) { // e[3]: flow, e[2]: capacity
                    level[e[1]] = level[u] + 1;
                    q.push(e[1]);
                }
            }
        }

        return level[sink] != -1;
    }

    // DFSで増加パスを探す
    ll sendFlow(int u, ll flow, int sink) {
        if (u == sink) return flow;

        for (; start[u] < adj[u].size(); ++start[u]) {
            int idx = adj[u][start[u]];
            auto& e = edges[idx];

            if (level[e[1]] == level[u] + 1 && e[3] < e[2]) {
                ll curr_flow = min(flow, e[2] - e[3]);
                ll temp_flow = sendFlow(e[1], curr_flow, sink);

                if (temp_flow > 0) {
                    e[3] += temp_flow;
                    edges[idx ^ 1][3] -= temp_flow; // 対応する逆辺
                    return temp_flow;
                }
            }
        }

        return 0;
    }

public:
    MaxFlow(int vertices) : V(vertices), adj(vertices), level(vertices), start(vertices) {}

    // 辺を登録
    void add_edge(int u, int v, ll cap) {
        edges.push_back({u, v, cap, 0}); // 順方向の辺
        edges.push_back({v, u, 0, 0});   // 逆方向の辺
        adj[u].push_back(edges.size() - 2);
        adj[v].push_back(edges.size() - 1);
    }

    // 最大流計算（Dinic法）
    ll flow(int source, int sink) {
        ll max_flow = 0;

        while (buildLevelGraph(source, sink)) {
            fill(start.begin(), start.end(), 0);

            while (ll f = sendFlow(source, LLONG_MAX, sink)) {
                max_flow += f;
            }
        }

        return max_flow;
    }

    // 最小カットを取得
    vector<int> min_cut(int source) {
        vector<bool> visited(V, false);
        queue<int> q;
        q.push(source);
        visited[source] = true;

        while (!q.empty()) {
            int u = q.front();
            q.pop();

            for (int idx : adj[u]) {
                auto& e = edges[idx];
                if (!visited[e[1]] && e[3] < e[2]) {
                    visited[e[1]] = true;
                    q.push(e[1]);
                }
            }
        }

        vector<int> cut;
        for (int i = 0; i < V; ++i) {
            if (visited[i]) {
                cut.push_back(i);
            }
        }
        return cut;
    }

    // 辺の情報を取得
    vector<ll> get_edge(int j) {
        return edges[j];
    }

    // 全ての辺の情報を取得
    vector<vector<ll>> get_edges() {
        vector<vector<ll>> output_edges;
        for (int j = 0; j < edges.size(); j += 2){
          output_edges.push_back(edges[j]);
        }
        return output_edges;
    }
};

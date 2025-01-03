class MinCostFlow {
public:
    MinCostFlow(int n) : n(n), adj(n), edges(), potential(n, 0) {}

    void add_edge(int from, int to, ll cap, ll cost) {
        adj[from].push_back(edges.size());
        edges.push_back({from, to, cap, 0, cost});
        adj[to].push_back(edges.size());
        edges.push_back({to, from, 0, 0, -cost});
    }

    // j番目に追加した辺を返す
    vector<ll> get_edge(int j) {
        return edges[j];
    }

    // 全ての辺を返す
    vector<vector<ll>> get_edges() {
        return edges;
    }

    // 最小費用流の下凸スロープを計算 (ダイクストラ法 + ポテンシャル)
    vector<pair<ll, ll>> flow_slope(int s, int t, ll max_flow = LLONG_MAX) {
        ll total_cost = 0;
        ll total_flow = 0;
        vector<pair<ll, ll>> slope; // 履歴

        while (max_flow > 0) {
            // 距離と親を初期化
            vector<ll> dist(n, LLONG_MAX), parent(n, -1), parent_edge(n, -1);
            dist[s] = 0;
            priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<>> pq;
            pq.emplace(0, s);

            // ダイクストラ法で最短経路探索
            while (!pq.empty()) {
                auto [d, u] = pq.top();
                pq.pop();

                if (dist[u] < d) continue;

                for (int i : adj[u]) {
                    auto& e = edges[i];
                    ll cost_with_potential = e[4] + potential[u] - potential[e[1]];
                    if (e[2] > e[3] && dist[e[1]] > dist[u] + cost_with_potential) {
                        dist[e[1]] = dist[u] + cost_with_potential;
                        parent[e[1]] = u;
                        parent_edge[e[1]] = i;
                        pq.emplace(dist[e[1]], e[1]);
                    }
                }
            }

            // tに到達不可
            if (dist[t] == LLONG_MAX) break;

            // ポテンシャルを更新
            for (int i = 0; i < n; ++i) {
                if (dist[i] < LLONG_MAX) {
                    potential[i] += dist[i];
                }
            }

            // 流せるフローの量を計算
            ll curr_flow = max_flow;
            for (int u = t; u != s; u = parent[u]) {
                int edge_index = parent_edge[u];
                curr_flow = min(curr_flow, edges[edge_index][2] - edges[edge_index][3]);
            }

            // フローを流しながらコスト計算
            for (int u = t; u != s; u = parent[u]) {
                int edge_index = parent_edge[u];
                edges[edge_index][3] += curr_flow;
                edges[edge_index ^ 1][3] -= curr_flow; // 逆辺
                total_cost += edges[edge_index][4] * curr_flow;
            }

            max_flow -= curr_flow;
            total_flow += curr_flow;

            // 現在のコストと流量を履歴に追加
            slope.emplace_back(total_cost, total_flow);
        }

        return slope;
    }

private:
    int n;  // ノード数
    vector<vector<ll>> edges;  // 辺の情報: {from, to, cap, flow, cost}
    vector<vector<int>> adj;   // 隣接リスト
    vector<ll> potential;      // ポテンシャル値
};

tuple<vector<vector<ll>>, vector<vector<ll>>, vector<ll>> strongly_connected_components(const vector<vector<ll>>& I) {
    ll n = I.size();
    vector<vector<ll>> I_rev(n); // 逆グラフ
    vector<bool> visited(n, false);
    stack<ll> order; // 頂点の帰りがけ順を格納
    vector<ll> vertex_to_component(n, -1); // 各頂点が属する成分番号
    vector<vector<ll>> components; // 強連結成分ごとの頂点リスト
    vector<vector<ll>> I_reduced; // 強連結成分分解後の隣接リスト

    // 逆グラフを構築
    for (ll u = 0; u < n; ++u) {
        for (ll v : I[u]) {
            I_rev[v].push_back(u);
        }
    }

    // 1. 帰りがけ順を記録（DFS on the original graph）
    auto dfs1 = [&](auto&& self, ll u) -> void {
        visited[u] = true;
        for (ll v : I[u]) {
            if (!visited[v]) self(self, v);
        }
        order.push(u);
    };

    for (ll i = 0; i < n; ++i) {
        if (!visited[i]) dfs1(dfs1, i);
    }

    // 2. 強連結成分を見つける（DFS on the reversed graph）
    visited.assign(n, false); // 再利用するためにリセット
    auto dfs2 = [&](auto&& self, ll u, ll component_id) -> void {
        visited[u] = true;
        vertex_to_component[u] = component_id;
        components.back().push_back(u);
        for (ll v : I_rev[u]) {
            if (!visited[v]) self(self, v, component_id);
        }
    };

    // 強連結成分を求める
    while (!order.empty()) {
        ll u = order.top();
        order.pop();
        if (!visited[u]) {
            components.emplace_back(); // 新しい成分を追加
            dfs2(dfs2, u, components.size() - 1);
        }
    }

    // 3. SCC後の縮約グラフを構築
    I_reduced.resize(components.size());
    for (ll u = 0; u < n; ++u) {
        for (ll v : I[u]) {
            ll from = vertex_to_component[u];
            ll to = vertex_to_component[v];
            if (from != to) {
                I_reduced[from].push_back(to);
            }
        }
    }

    // SCC後の隣接リストの重複を削除
    for (auto& adj : I_reduced) {
        sort(adj.begin(), adj.end());
        adj.erase(unique(adj.begin(), adj.end()), adj.end());
    }

    return {I_reduced, components, vertex_to_component};
}

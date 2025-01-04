vector<ll> topological_sort(const vector<vector<ll>>& I) {
    ll n = I.size();
    vector<ll> in_degree(n, 0); // 各ノードの入次数
    vector<ll> topo_order; // トポロジカル順序を格納するベクター

    // 入次数を計算
    for (ll u = 0; u < n; ++u) {
        for (ll v : I[u]) {
            in_degree[v]++;
        }
    }

    // 入次数が0のノードをキューに追加
    queue<ll> q;
    for (ll i = 0; i < n; ++i) {
        if (in_degree[i] == 0) {
            q.push(i);
        }
    }

    // トポロジカルソート
    while (!q.empty()) {
        ll u = q.front();
        q.pop();
        topo_order.push_back(u);

        for (ll v : I[u]) {
            in_degree[v]--;
            if (in_degree[v] == 0) {
                q.push(v);
            }
        }
    }

    // トポロジカル順序の長さがグラフの頂点数と一致しない場合、DAGではない
    if (topo_order.size() != n) {
        return {}; // 空ベクターを返す
    }

    return topo_order;
}

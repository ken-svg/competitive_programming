// 二部グラフの最大マッチングをO(E^(3/2))で行う。
// 左側、右側の頂点数をそれぞれ与える。頂点の番号付けは左右独立。
// add_edge(左側、右側)で辺を追加し、max_matching()で最大マッチ数を計算。get_matching()で具体的なマッチングを返す。
class BipartiteMatching {
private:
    int n, m; // Sizes of left and right sets
    vector<vector<int>> adj; // Adjacency list
    vector<int> pairU, pairV, dist; // Pairings and distance for BFS

    bool bfs() {
        // Initialize distances
        for (int u = 0; u < n; ++u) {
            dist[u] = INT_MAX;
        }
        dist[n] = INT_MAX; // Sentinel node
    
        queue<int> q;
        for (int u = 0; u < n; ++u) {
            if (pairU[u] == -1) { // Unmatched node
                dist[u] = 0;
                q.push(u);
            }
        }
    
        while (!q.empty()) {
            int u = q.front();
            q.pop();
    
            if (dist[u] < dist[n]) {
                for (int v : adj[u]) {
                    if (dist[pairV[v]] == INT_MAX) {
                        dist[pairV[v]] = dist[u] + 1;
                        q.push(pairV[v]);
                    }
                }
            }
        }
        return dist[n] != INT_MAX; // Return true if there is an augmenting path
    }

    bool dfs(int u) {
        if (u != n) { // Sentinel node check
            for (int v : adj[u]) {
                if (dist[pairV[v]] == dist[u] + 1 && dfs(pairV[v])) {
                    pairV[v] = u;
                    pairU[u] = v;
                    return true;
                }
            }
            dist[u] = INT_MAX; // Mark as visited
            return false;
        }
        return true; // Sentinel node
    }

public:
    BipartiteMatching(int leftSize, int rightSize) {
        n = leftSize;
        m = rightSize;
        adj.resize(n);
        pairU.assign(n, -1);
        pairV.assign(m, n);
        dist.resize(n + 1); // Include extra index for sentinel node
    }

    void add_edge(int u, int v) {
        adj[u].push_back(v); // u is 0-indexed, v is also 0-indexed
    }

    int max_matching() {
        int maxMatch = 0;
        while (bfs()) {
            for (int u = 0; u < n; ++u) {
                if (pairU[u] == -1 && dfs(u)) {
                    ++maxMatch;
                }
            }
        }
        
        return maxMatch;
    }

    vector<pair<int, int>> get_matching() {
        vector<pair<int, int>> matching;
        for (int u = 0; u < n; ++u) {
            if (pairU[u] != -1) {
                matching.emplace_back(u, pairU[u]);
            }
        }
        return matching;
    }
};

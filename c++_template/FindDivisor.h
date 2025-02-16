vector<long long> FindDevisor(long long n) {
    vector<long long> ans = {};
    vector<long long> ans2 = {};
    for (long long q = 1; q * q <= n; q++) {
        if (n % q == 0) {
            ans.push_back(q);
            if (q * q != n) ans2.push_back(n / q);
        }
    }
    reverse(ans2.begin(), ans2.end());
    for (auto a : ans2) ans.push_back(a);
    return ans;
}

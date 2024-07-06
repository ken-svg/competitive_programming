// 行列積
template <typename T>
vector<vector<T>> mat_pow(const vector<vector<T>> &P, const vector<vector<T>> &Q, const T mod = 0){
  vector<vector<T>> R(P.size(), vector<T>(Q.at(0).size(), 0));
  for (int i = 0; i < P.size(); i++){
    for (int j = 0; j < Q.at(0).size(); j++){
      for (int k = 0; k < Q.size(); k++){
        R[i][j] += (P[i][k] * Q[k][j]);
        if (mod != 0){
          R[i][j] %= mod;
        }
      }
      //r.push_back(tmp);
    }
    //R.push_back(r);
  }
  return R;
}

// 行列累乗
template <typename T>
vector<vector<T>> mat_pow(const vector<vector<T>> A, T K, const T mod = 0){
  vector<vector<T>> F(0);
  // 単位行列の準備
  for (int i = 0; i < A.size(); i++){
    vector<T> f(0);
    for (int j = 0; j < A.size(); j++){
      f.push_back(T(i == j));
    }
    F.push_back(f);
  }
  
  for (int b = 62; b >= 0; b--){
    F = mat_pow(F, F, mod);
    if ((K >> b) & 1){
      F = mat_pow(F, A, mod);
    }
  }
  return F;
}

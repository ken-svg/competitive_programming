template <typename T>
void print(vector<T> &A){
  cout << "(";
  for (auto a : A) {
    cout << a << ", ";
  }
  cout << ")";
}
template <typename T>
void print(vector<vector<T>> &A){
  cout << "[";
  for (auto a : A) {
    print(a);
    cout << ", ";
  }
  cout << "]";
}

#include <bits/stdc++.h>
using namespace std;

// 型エイリアス
using str = string;
using chr = char;
using ll = long long;
using ld = long double;
template <typename K, typename V>
using umap = unordered_map<K, V>;
template <typename T>
using uset = unordered_set<T>;
template <typename T>
using mset = multiset<T>;
template <typename T>
using umset = unordered_multiset<T>;
template <typename T>
using gpque = priority_queue<T>;
template <typename T>
using lpque = priority_queue<T, vector<T>, greater<T>>;
template <typename T>
using pque = priority_queue<T, vector<T>, greater<T>>;

// pairの三つ組版
template <typename T1, typename T2, typename T3>
struct triplet {
    T1 first;    // 第一の要素
    T2 second;   // 第二の要素
    T3 third;    // 第三の要素

    // コンストラクタ
    triplet(const T1& f, const T2& s, const T3& t)
        : first(f), second(s), third(t) {}
    
    // 比較演算子の定義
    bool operator==(const triplet& other) const {
        return first == other.first && second == other.second && third == other.third;
    }

    bool operator!=(const triplet& other) const {
        return !(*this == other);
    }

    bool operator<(const triplet& other) const {
        if (first != other.first) return first < other.first;
        if (second != other.second) return second < other.second;
        return third < other.third;
    }

    bool operator<=(const triplet& other) const {
        return *this < other || *this == other;
    }

    bool operator>(const triplet& other) const {
        return !(*this <= other);
    }

    bool operator>=(const triplet& other) const {
        return !(*this < other);
    }
};
// pair のハッシュ関数を定義
template <typename T1, typename T2>
struct hash<pair<T1, T2>> {
    size_t operator()(const pair<T1, T2>& p) const {
        // 各要素のハッシュを組み合わせる方法
        size_t h1 = hash<T1>()(p.first); // first のハッシュ
        size_t h2 = hash<T2>()(p.second); // second のハッシュ
        return h1 ^ (h2 << 1) ;  // ハッシュ値を組み合わせる
    }
};
// triplet のハッシュ関数を定義
template <typename T1, typename T2, typename T3>
struct hash<triplet<T1, T2, T3>> {
    size_t operator()(const triplet<T1, T2, T3>& t) const {
        size_t h1 = hash<T1>()(t.first); // 1つ目の要素
        size_t h2 = hash<T2>()(t.second); // 2つ目の要素
        size_t h3 = hash<T3>()(t.third); // 3つ目の要素
        return h1 ^ (h2 << 1) ^ (h3 << 2);  // ハッシュ値を組み合わせる
    }
};

// vectorのエイリアス
#define DEFINE_VECTOR(A) using v_##A = vector<A>; using vv_##A = vector<vector<A>>; using vvv_##A = vector<vector<vector<A>>>;
#define DEFINE_VECTORS(A, B, C, D, E) DEFINE_VECTOR(A) DEFINE_VECTOR(B) DEFINE_VECTOR(C) DEFINE_VECTOR(D) DEFINE_VECTOR(E)
DEFINE_VECTORS(ll, ld, chr, str, bool);

// pairのエイリアス
#define _DEFINE_PAIRS(A, B, C, D, E, F) using p_##A##_##B = pair<A, B>; using p_##A##_##C = pair<A, C>; using p_##A##_##D = pair<A, D>; using p_##A##_##E = pair<A, E>; using p_##A##_##F = pair<A, F>;
#define DEFINE_PAIRS(A, B, C, D, E) _DEFINE_PAIRS(A, A, B, C, D, E) _DEFINE_PAIRS(B, A, B, C, D, E) _DEFINE_PAIRS(C, A, B, C, D, E) _DEFINE_PAIRS(D, A, B, C, D, E) _DEFINE_PAIRS(E, A, B, C, D, E)
DEFINE_PAIRS(ll, ld, chr, str, bool);

// tripletのエイリアス
#define __DEFINE_TRIPLETS(A, B, C, D, E, F, G) using t_##A##_##B##_##C = triplet<A, B, C>; using t_##A##_##B##_##D = triplet<A, B, D>; using t_##A##_##B##_##E = triplet<A, B, E>; using t_##A##_##B##_##F = triplet<A, B, F>; using t_##A##_##B##_##G = triplet<A, B, G>;
#define _DEFINE_TRIPLETS(A, B, C, D, E, F) __DEFINE_TRIPLETS(A, B, B, C, D, E, F) __DEFINE_TRIPLETS(A, C, B, C, D, E, F) __DEFINE_TRIPLETS(A, D, B, C, D, E, F) __DEFINE_TRIPLETS(A, E, B, C, D, E, F) __DEFINE_TRIPLETS(A, F, B, C, D, E, F)
#define DEFINE_TRIPLETS(A, B, C, D, E) _DEFINE_TRIPLETS(A, A, B, C, D, E) _DEFINE_TRIPLETS(B, A, B, C, D, E) _DEFINE_TRIPLETS(C, A, B, C, D, E) _DEFINE_TRIPLETS(D, A, B, C, D, E) _DEFINE_TRIPLETS(E, A, B, C, D, E)
DEFINE_TRIPLETS(ll, ld, chr, str, bool);

//function<A(B)>のエイリアス
#define _DEFINE_FUNCITONS1(A, B, C, D, E, F) using f_##A##_##B = function<A(B)>; using f_##A##_##C = function<A(C)>; using f_##A##_##D = function<A(D)>; using f_##A##_##E = function<A(E)>; using f_##A##_##F = function<A(F)>;
#define DEFINE_FUNCITONS1(A, B, C, D, E) _DEFINE_FUNCITONS1(A, A, B, C, D, E) _DEFINE_FUNCITONS1(B, A, B, C, D, E) _DEFINE_FUNCITONS1(C, A, B, C, D, E) _DEFINE_FUNCITONS1(D, A, B, C, D, E) _DEFINE_FUNCITONS1(E, A, B, C, D, E)
DEFINE_FUNCITONS1(ll, ld, chr, str, bool);

// 定数とマクロ
const ll MOD = 998244353;
#define elif else if
#define rep(i, n) for(ll i = 0; i < n; i++)
#define rep_range(i, s, t) for(ll i = s; i < t; i++)
#define rep_step(i, s, t, b) for(ll i = s; (i - t) * b < 0; i += b)
#define rep_in(a, A) for(auto a: A)
#define rep_pair(f, s, A) for(auto [f, s]: A)
#define rep_triplet(f, s, t, A) for(auto [f, s, t]: A)

// コンテナの標準出力をオーバーロード
template <typename T1, typename T2>
ostream& operator<<(ostream& os, const pair<T1, T2>& t) {
    os << "(" << t.first << ", " << t.second << ")";
    return os;
}
template <typename T1, typename T2, typename T3>
ostream& operator<<(ostream& os, const triplet<T1, T2, T3>& t) {
    os << "(" << t.first << ", " << t.second << ", " << t.third << ")";
    return os;
}
template <typename Tuple, size_t Index = 0>
void print_tuple(std::ostream& os, const Tuple& t) {
    if constexpr (Index < std::tuple_size<Tuple>::value) {
        if (Index > 0) os << ", ";  // 2番目以降の要素にコンマを追加
        os << std::get<Index>(t);
        print_tuple<Tuple, Index + 1>(os, t);  // 再帰呼び出し
    }
} // helper for tuple
template <typename... Args>
ostream& operator<<(std::ostream& os, const std::tuple<Args...>& t) {
    os << "(";
    print_tuple(os, t);  // 再帰的にtupleを出力
    os << ")";
    return os;
}
template <typename T>
ostream& operator<<(ostream& os, const vector<T>& vec) {
    os << "[";
    for (size_t i = 0; i < vec.size(); ++i) {
        os << vec[i];
        if (i != vec.size() - 1) os << ", ";
    }
    os << "]";
    return os;
}
template <typename K, typename V>
ostream& operator<<(ostream& os, const unordered_map<K, V>& um) {
    os << "{(unordered) ";
    bool first = true;
    for (const auto& [key, value] : um) {
        if (!first) os << ", ";
        os << "(" << key << "): " << value;
        first = false;
    }
    os << "}";
    return os;
}
template <typename K, typename V>
ostream& operator<<(ostream& os, const map<K, V>& um) {
    os << "{(ordered) ";
    bool first = true;
    for (const auto& [key, value] : um) {
        if (!first) os << ", ";
        os << "(" << key << "): " << value;
        first = false;
    }
    os << "}";
    return os;
}
template <typename T>
ostream& operator<<(ostream& os, const unordered_set<T>& us) {
    os << "{(unordered) ";
    bool first = true;
    for (const auto& elem : us) {
        if (!first) os << ", ";
        os << elem;
        first = false;
    }
    os << "}";
    return os;
}
template <typename T>
ostream& operator<<(ostream& os, const set<T>& us) {
    os << "{(ordered) ";
    bool first = true;
    for (const auto& elem : us) {
        if (!first) os << ", ";
        os << elem;
        first = false;
    }
    os << "}";
    return os;
}
template <typename T>
ostream& operator<<(ostream& os, const multiset<T>& ms) {
    os << "{(ordered) ";
    bool first = true;
    for (const auto& elem : ms) {
        if (!first) os << ", ";
        os << elem;
        first = false;
    }
    os << "}";
    return os;
}
template <typename T>
ostream& operator<<(ostream& os, const unordered_multiset<T>& ums) {
    os << "{(unordered) ";
    bool first = true;
    for (const auto& elem : ums) {
        if (!first) os << ", ";
        os << elem;
        first = false;
    }
    os << "}";
    return os;
}
template <typename T>
ostream& operator<<(ostream& os, const deque<T>& dq) {
    os << "[(deque) ";
    bool first = true;
    for (const auto& elem : dq) {
        if (!first) os << ", ";
        os << elem;
        first = false;
    }
    os << "]";
    return os;
}
template <typename T>
ostream& operator<<(ostream& os, const priority_queue<T>& pq) {
    priority_queue<T> temp = pq;
    os << "[(max_priority_queue)";
    bool first = true;
    while (!temp.empty()) {
        if (!first) os << ", ";
        os << temp.top();
        temp.pop();
        first = false;
    }
    os << "]";
    return os;
}
template <typename T>
ostream& operator<<(ostream& os, const lpque<T>& pq) {
    lpque<T> temp = pq;
    os << "[(min_priority_queue)";
    bool first = true;
    while (!temp.empty()) {
        if (!first) os << ", ";
        os << temp.top();
        temp.pop();
        first = false;
    }
    os << "]";
    return os;
}

// 標準出力
template <typename T, typename... Args>
void _print(T&& first, Args&&... rest) {
    cout << first;  // 最初の引数を出力
    if constexpr (sizeof...(rest) > 0) {  // 残りの引数があれば
        cout << " ";  // スペースを挿入
        _print(forward<Args>(rest)...);  // 残りの引数を再帰的に処理
    }
}
template <typename T, typename... Args>
void print(T&& first, Args&&... rest) {
    cout << first;  // 最初の引数を出力
    if constexpr (sizeof...(rest) > 0) {  // 残りの引数があれば
        cout << " ";  // スペースを挿入
        _print(forward<Args>(rest)...);  // 残りの引数を再帰的に処理
    }
    cout << endl;
}
// 指定文字(delimiter)区切りで標準出力（コンテナのみ）
template <typename T>
void print_elements(const T& container, char delimiter = ' ') {
    if (container.empty()) {
        cout << endl;
        return;
    }
    bool first = true;
    for (const auto& element : container) {
        if (!first) {
            cout << delimiter;  // 最初の要素以外に区切り文字を挿入
        }
        cout << element;  // 要素を出力
        first = false;  // 最初の要素を過ぎたら区切り文字を挿入する
    }
    cout << endl;  // 最後に改行
}

// 事前に定義された変数に標準入力
template <typename... Args>
void input(Args&... args) {
    (cin >> ... >> args);
}
// 標準入力の一行を指定された型でvectorに格納
template <typename T>
vector<T> input_to_vector() {
    vector<T> result;
    string line;
    bool flag = false;
    while (!flag) {
      getline(cin, line);
      stringstream ss(line);
      T value;
      while (ss >> value) {  // 1行の中に空白で区切られた値を読み取る
          result.push_back(value);
          flag = true;
      }
    }
    return result;
}

// コンテナの二分探索
template <typename T>
ll bisect_left(const vector<T>& vec, const T& value) {
    auto it = lower_bound(vec.begin(), vec.end(), value);
    return distance(vec.begin(), it);  // 小さいものの数 = lower_boundの位置
}
template <typename T>
ll bisect_right(const vector<T>& vec, const T& value) {
    auto it = upper_bound(vec.begin(), vec.end(), value);
    return distance(vec.begin(), it);  // 以下のものの数 = upper_boundの位置
}
template <typename T>
ll bisect_left(const set<T>& s, const T& value) {
    auto it = s.lower_bound(value);
    return distance(s.begin(), it);  // 小さいものの数 = lower_boundの位置
}
template <typename T>
ll bisect_right(const set<T>& s, const T& value) {
    auto it = s.upper_bound(value);
    return distance(s.begin(), it);  // 以下のものの数 = upper_boundの位置
}
template <typename T>
ll bisect_left(const multiset<T>& ms, const T& value) {
    auto it = ms.lower_bound(value);
    return distance(ms.begin(), it);  // 小さいものの数 = lower_boundの位置
}
template <typename T>
ll bisect_right(const multiset<T>& ms, const T& value) {
    auto it = ms.upper_bound(value);
    return distance(ms.begin(), it);  // 以下のものの数 = upper_boundの位置
}
template <typename K, typename V>
ll bisect_left(const map<K, V>& m, const K& key) {
    auto it = m.lower_bound(key);
    return distance(m.begin(), it);  // 小さいものの数 = lower_boundの位置
}
template <typename K, typename V>
ll bisect_right(const map<K, V>& m, const K& key) {
    auto it = m.upper_bound(key);
    return distance(m.begin(), it);  // 以下のものの数 = upper_boundの位置
}

// 各コンテナへの変換
template <typename T>
vector<typename T::value_type> to_vector(const T& container) {
    vector<typename T::value_type> result;
    if constexpr (is_same<T, priority_queue<typename T::value_type>>::value || is_same<T, lpque<typename T::value_type>>::value) {
        // priority_queueの場合、while文を使って取り出す
        auto pq = container;
        while (!pq.empty()) {
            result.push_back(pq.top());
            pq.pop();
        }
    } else result = vector<typename T::value_type>(container.begin(), container.end());
    return result;
}
template <typename T>
set<typename T::value_type> to_set(const T& container) {
    set<typename T::value_type> result;
    if constexpr (is_same<T, priority_queue<typename T::value_type>>::value || is_same<T, lpque<typename T::value_type>>::value) {
        // priority_queueの場合、while文を使って取り出す
        auto pq = container;
        while (!pq.empty()) {
            result.insert(pq.top());
            pq.pop();
        }
    } else result = set<typename T::value_type>(container.begin(), container.end());
    return result;
}
template <typename T>
unordered_set<typename T::value_type> to_uset(const T& container) {
    unordered_set<typename T::value_type> result;
    if constexpr (is_same<T, priority_queue<typename T::value_type>>::value || is_same<T, lpque<typename T::value_type>>::value) {
        // priority_queueの場合、while文を使って取り出す
        auto pq = container;
        while (!pq.empty()) {
            result.insert(pq.top());
            pq.pop();
        }
    } else result = unordered_set<typename T::value_type>(container.begin(), container.end());
    return result;
}
template <typename T>
multiset<typename T::value_type> to_mset(const T& container) {
    multiset<typename T::value_type> result;
    if constexpr (is_same<T, priority_queue<typename T::value_type>>::value || is_same<T, lpque<typename T::value_type>>::value) {
        // priority_queueの場合、while文を使って取り出す
        auto pq = container;
        while (!pq.empty()) {
            result.insert(pq.top());
            pq.pop();
        }
    } else result = multiset<typename T::value_type>(container.begin(), container.end());
    return result;
}
template <typename T>
unordered_multiset<typename T::value_type> to_umset(const T& container) {
    unordered_multiset<typename T::value_type> result;
    if constexpr (is_same<T, priority_queue<typename T::value_type>>::value || is_same<T, lpque<typename T::value_type>>::value) {
        // priority_queueの場合、while文を使って取り出す
        auto pq = container;
        while (!pq.empty()) {
            result.insert(pq.top());
            pq.pop();
        }
    } else result = unordered_multiset<typename T::value_type>(container.begin(), container.end());
    return result;
}
template <typename T>
deque<typename T::value_type> to_deque(const T& container) {
    deque<typename T::value_type> result;
    if constexpr (is_same<T, priority_queue<typename T::value_type>>::value || is_same<T, lpque<typename T::value_type>>::value) {
        // priority_queueの場合、while文を使って取り出す
        auto pq = container;
        while (!pq.empty()) {
            result.push_back(pq.top());
            pq.pop();
        }
    } else result = deque<typename T::value_type>(container.begin(), container.end());
    return result;
}
template <typename T>
priority_queue<typename T::value_type> to_gpque(const T& container) {
    priority_queue<typename T::value_type> result;
    if constexpr (is_same<T, priority_queue<typename T::value_type>>::value || is_same<T, lpque<typename T::value_type>>::value) {
        // priority_queueの場合、while文を使って取り出す
        auto pq = container;
        while (!pq.empty()) {
            result.push(pq.top());
            pq.pop();
        }
    } else result = priority_queue<typename T::value_type>(container.begin(), container.end());
    return result;
}
template <typename T>
lpque<typename T::value_type> to_lpque(const T& container) {
    lpque<typename T::value_type> result;
    if constexpr (is_same<T, priority_queue<typename T::value_type>>::value || is_same<T, lpque<typename T::value_type>>::value) {
        // priority_queueの場合、while文を使って取り出す
        auto pq = container;
        while (!pq.empty()) {
            result.push(pq.top());
            pq.pop();
        }
    } else result = lpque<typename T::value_type>(container.begin(), container.end());
    return result;
}
template <typename T>
pque<typename T::value_type> to_pque(const T& container) {
    return to_lpque(container);
}

// sort_vector 関数：単純ソート
template <typename T>
void sort_vector(vector<T>& vec, bool reverse = false) {
    if (reverse) {
      sort(vec.begin(), vec.end(), greater<T>());
    } else {
      sort(vec.begin(), vec.end());
    }
}
// sort_by_cmp 関数：比較関数によるソート
template <typename T>
void sort_by_cmp(vector<T>& vec, function<bool(T, T)> cmp) {
    // ソート基準を決定するラムダ式
    sort(vec.begin(), vec.end(), cmp);
}
// sort_by_key 関数：key関数によるソート
template <typename T, typename V>
void sort_by_key(vector<T>& vec, function<V(T)> key) {
    // ソート基準を決定するラムダ式
    auto comparator = [key](T a, T b) {
        V key_a = key(a);
        V key_b = key(b);
        return key_a < key_b;  // 昇順
    };
    // ソート
    sort(vec.begin(), vec.end(), comparator);
}

// gpque, lpqueの定義用
template <typename T>
gpque<T> make_gpque(initializer_list<T> init_list) {
    gpque<T> pq;
    for (const auto& elem : init_list) {
        pq.push(elem);  
    }
    return pq;
}
template <typename T>
lpque<T> make_lpque(initializer_list<T> init_list) {
    lpque<T> pq;
    for (const auto& elem : init_list) {
        pq.push(elem);  
    }
    return pq;
}
template <typename T>
pque<T> make_pque(initializer_list<T> init_list) {
    return make_lpque(init_list);
}

// 任意のコンテナのサイズを返す関数
template <typename Container>
long long len(const Container& container) {
    return static_cast<long long>(container.size()); // サイズをll型に変換して返す
}

// llについての算術操作
// 整数の商
long long idiv(long long a, long long b) {
    return (a >= 0) ? a / b : ((a + 1) / b) - 1;
}
// 最小非負の余り
long long imod(long long a, long long b = MOD) {
    long long r = a % b;
    return r < 0 ? r + b : r;
}
// 小数での除算
long double fdiv(long long a, long long b) {
    return static_cast<long double>(a) / b; 
}
// べき
long long pow(long long a, long long b, const long long m = 0) {
    long long result = 1;
    if (m == 0) {
        // m が 0 の場合、単に a^b を計算（繰り返し二乗法）
        while (b > 0) {
            if (b % 2 == 1) {
                result = result * a;  // b が奇数なら掛け算して mod
            }
            a = a * a;  // a を2乗して mod
            b /= 2;  // b を半分にする
        }
        
    } else {
        // m が 0 でない場合は、(a^b) % m を計算（繰り返し二乗法）
        a = a % m;  // a を mod m で初期化
        while (b > 0) {
            if (b % 2 == 1) {
                result = (result * a) % m;  // b が奇数なら掛け算して mod
            }
            a = (a * a) % m;  // a を2乗して mod
            b /= 2;  // b を半分にする
        }
        if (result < 0) result += m;
    }
    return result;
}

// 拡張ユークリッド互除法
template <typename T>
tuple<T, T, T> ext_gcd(T a, T b){
  if (b == 0) return {1 * a / abs(a), 0, abs(a)};
  else {
    auto [x, y, d] = ext_gcd(b, a % b);
    return {y, x - y * (a / b), d};
  }
} // a * f + b * s = t(gcd)
// mod逆元
template <typename T>
T mod_inv(T x, const T mod = MOD){
  auto [x_inv, _, d] = ext_gcd(x, mod);
  if (d != 1) return 0;
  else {
    x_inv %= mod;
    if (x_inv < 0) x_inv += mod;
    return x_inv;
  }
}

// vector<string> を結合する関数
string join(const vector<string>& vec) {
    string result;
    for (const auto& str : vec) {
        result += str;  // 文字列を追加
    }
    return result;
}
// vector<char> を結合する関数
string join(const vector<char>& vec) {
    string result;
    for (const auto& ch : vec) {
        result += ch;  // char を追加
    }
    return result;
}

// 文字列を long long に変換する関数
long long to_ll(const string& str) {
    long long result;
    stringstream ss(str);

    if (!(ss >> result)) {
        throw invalid_argument("Invalid input for long long conversion");
    }

    return result;
}
// 1文字を long double に変換する関数
long double to_ll(char c) {
    if (!isdigit(c)) {
        throw invalid_argument("Input character is not a valid digit");
    }
    return static_cast<long long>(c - '0');
}
// 文字列を long double に変換する関数
long double to_ld(const string& str) {
    long double result;
    stringstream ss(str);

    if (!(ss >> result)) {
        throw invalid_argument("Invalid input for long double conversion");
    }

    return result;
}
// 1文字を long double に変換する関数
long double to_ld(char c) {
    if (!isdigit(c)) {
        throw invalid_argument("Input character is not a valid digit");
    }
    return static_cast<long double>(c - '0');
}


// max関数 (可変長引数を取る)
template <typename T, typename... Args>
T max(T first, T second, T third, Args... args) {
    if constexpr (sizeof...(args) > 0) {  // 残りの引数があれば
        return max(first, max(second, third, args...)); // 再帰的処理
    }
    return max(first, max(second, third));
}
// max関数 (containerを引数に取る)
template <typename Container>
typename Container::value_type max(const Container& container) {
    return *max_element(container.begin(), container.end());
}

// min関数 (可変長引数を取る)
template <typename T, typename... Args>
T min(T first, T second, T third, Args... args) {
    if constexpr (sizeof...(args) > 0) {  // 残りの引数があれば
        return min(first, min(second, third, args...)); // 再帰的処理
    }
    return min(first, min(second, third));
}
// min関数 (containerを引数に取る)
template <typename Container>
typename Container::value_type min(const Container& container) {
    return *min_element(container.begin(), container.end());
}

// sum関数 (可変長引数を取る)
template <typename T, typename... Args>
T sum(T first, T second, Args... args) {
    if constexpr (sizeof...(args) > 0) {  // 残りの引数があれば
        return first + sum(second, args...); // 再帰的処理
    }
    return first + second;
}
// sum関数 (containerを引数に取る)
template <typename Container>
typename Container::value_type sum(const Container& container) {
    return accumulate(container.begin(), container.end(), typename Container::value_type(0));
}
// 全てtrueか
bool all_true(vector<bool> vec) {
  bool ans = true;
  for (bool tf : vec) {
    ans &= tf;
  }
  return ans;
}
// 少なくとも一つtrueか
bool any_true(vector<bool> vec) {
  bool ans = false;
  for (bool tf : vec) {
    ans |= tf;
  }
  return ans;
}

// vectorを一定値で生成する関数
template <typename T>
vector<T> make_vector(long long size, T initial_value) {
    if (size < 0) {
        throw invalid_argument("Size cannot be negative");
    }
    return vector<T>(static_cast<size_t>(size), initial_value);
}
template <typename T>
vector<vector<T>> make_vector(long long rows, long long cols, T initial_value) {
    if (rows < 0 || cols < 0) {
        throw invalid_argument("Rows and cols cannot be negative");
    }
    return vector<vector<T>>(static_cast<size_t>(rows), 
                             vector<T>(static_cast<size_t>(cols), initial_value));
}
template <typename T>
vector<vector<vector<T>>> make_vector(long long depth, long long rows, long long cols, T initial_value) {
    if (depth < 0 || rows < 0 || cols < 0) {
        throw invalid_argument("Depth, rows, and cols cannot be negative");
    }
    return vector<vector<vector<T>>>(static_cast<size_t>(depth), 
                                      vector<vector<T>>(static_cast<size_t>(rows), 
                                                        vector<T>(static_cast<size_t>(cols), initial_value)));
}

// pair, triplet, tupleの展開
template <typename T1, typename T2>
void unfold(T1& f, T2& s, pair<T1, T2>& pr) {
  f = pr.first;
  s = pr.second;
}
template <typename T1, typename T2, typename T3>
void unfold(T1& f, T2& s, T3& t, triplet<T1, T2, T3>& tr) {
  f = tr.first;
  s = tr.second;
  t = tr.third;
}
template <typename T1, typename T2, typename T3>
void unfold(T1& f, T2& s, T3& t, tuple<T1, T2, T3>& tr) {
  f = get<0>(tr);
  s = get<1>(tr);
  t = get<2>(tr);
}
template <typename T1, typename T2, typename T3, typename T4>
void unfold(T1& f, T2& s, T3& t, T4& q, tuple<T1, T2, T3, T4>& tr) {
  f = get<0>(tr);
  s = get<1>(tr);
  t = get<2>(tr);
  q = get<3>(tr);
}

// 説明
//  型エイリアス：
//   ll: long long
//   ld: long double
//   str: string
//   chr: char
//   [コンテナ]
//    v_(**): vector<**>
//    vv_(**): vector<vector<**>>
//    vvv_(**): vector<vector<vector<**>>>
//    p_(**1)_(**2): pair<**1, **2>
//    t_(**1)_(**2)_(**3): triplet<**1, **2, **3>  pairの３つ組版
//    f_(**1)_(**2): function<**1(**2)>  function (**1) -> (**2)
//    umap: unordered_map;
//    uset: unordered_set;
//    mset: multiset;
//    umset: unordered_multiset;
//    gpque: max-priority_queue;
//    lpque: min-priority_queue;

//　定数：
//   MOD = 998244353

//  マクロ：
//   rep(i, n) for(ll i = 0; i < n; i++)   変数iをとる
//   rep_range(i, s, t) for(ll i = s; i < t; i++)   sからt-1まで
//   rep_step(i, s, t, b) for(ll i = s; (i - t) * b < 0; i += b) sから、tの直前まで。stepはb
//   rep_in(a, A) for(auto a: A)   変数aがコンテナAを走る
//   rep_pair(f, s, A) for(auto [f, s]: A)
//   rep_triplet(f, s, t, A) for(auto [f, s, t]: A)
//   elif else if

//  よく使う関数：
//   [標準入力]
//    input(可変長): 標準入力（変数は事前定義）
//    input_to_vector<T>(): 標準入力の次の改行までで、vector<T>を作る
//   [標準出力]
//    print(可変長): 標準出力
//    print_elements(コンテナ, 区切り文字): コンテナ要素の出力 
//   [算術演算]
//    idiv, imod, fdiv: 商, 余り, 小数の除算
//    pow: べき（オプションで剰余）
//    ext_gcd: 拡張ユークリッド互助法 a * f + b * s = t(gcd>0)となるtuple({f, s, t})
//    mod_inv: mod逆元
//   [文字列の結合]
//    join(vector<string or char>) 結合
//    to_ll(char or string) 整数への変換
//    to_ld(char or string) 小数への変換
//   [二分探索]
//    biect_left(コンテナ, 文字): 指定値未満の個数
//    biect_right(コンテナ, 文字): 指定値以下の個数
//   [コンテナ関係]
//    ・ソート
//     sort_vector(vector, reverse) *reverse = false(デフォルト) trueのとき降順
//     sort_by_key(vector, key)  * V key(T a) | key(a) < key(b) ⇄ a < b
//     sort_by_cmp(vector, cmp)  * bool cmp(T a, T b) | cmp(a, b) ⇄ a < b
//    ・コンテナ変換
//     to_{vector/set/mset/uset/umset/deque/gpque/lpqueのいずれか}(container) 
//    ・lpque, gpque の作成
//     make_gpque({...}) / make_lpque({...})
//    ・長さ(llで出力)
//     len(container)
//    ・総和、最大、最小
//     sum/max/min(container)
//    ・全てtrue, 少なくとも一つtrue
//     all_true(vector<bool>), any_true(vector<bool>)
//    ・一定値ベクトルの生成
//     make_vector<T>(size, T initial) 一次元
//     make_vector<T>(row, col, T initial) 二次元
//     make_vector<T>(depth, row, col, T initial) 三次元
//    ・pair, triplet, tupleの展開
//     unfold(f, s, (t, q), pair/triplet/tuple) 

int main(){
    cout << setprecision(18);
    
    // ***

    return 0;
}

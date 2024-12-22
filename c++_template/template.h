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

// 定数とマクロ
const ll MOD = 998244353;
#define elif else if
#define rep(i, n) for(ll i = 0; i < n; i++)
#define rep_in(a, A) for(auto a: A)
#define rep_range(i, s, t) for(ll i = s; i < t; i++)
#define rep_step(i, s, t, b) for(ll i = s; (i - t) * b < 0; i += b)

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
template <typename T>
void print_value(const T& value) {
    cout << value;
}
template <typename T1, typename T2>
void print_value(const pair<T1, T2>& pa) {
    cout << "(";
    print_value(pa.first);
    cout << ", ";
    print_value(pa.second);
    cout << ")";
}
template <typename... Args>
void print(Args&&... args) {
    (print_value(forward<Args>(args)), ...);
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

// vectorのソート
// sort_vector 関数：単純ソート
template <typename T>
void sort_vector(vector<T>& vec, bool reverse = false) {
    if (reverse) {
      sort(vec.begin(), vec.end(), greater<T>());
    } else {
      sort(vec.begin(), vec.end());
    }
}
// sort_by_key 関数：key関数に基づいてソート
template <typename T>
void sort_by_key(vector<T>& vec, bool reverse = false, ll (*key)(const T&) = nullptr) {
    if (key) {
        if (reverse) {
            // 降順ソート
            sort(vec.begin(), vec.end(), [key](const T& a, const T& b) {
                return key(a) > key(b);  // key関数の結果で降順
            });
        } else {
            // 昇順ソート
            sort(vec.begin(), vec.end(), [key](const T& a, const T& b) {
                return key(a) < key(b);  // key関数の結果で昇順
            });
        }
    } else {
        // keyがnullptrの場合（通常の昇順ソート）
        if (reverse) {
            sort(vec.begin(), vec.end(), greater<T>());
        } else {
            sort(vec.begin(), vec.end());
        }
    }
}
// sort_by_cmp 関数：cmp関数に基づいてソート
template <typename T>
void sort_by_cmp(vector<T>& vec, bool reverse = false, bool (*cmp)(const T&, const T&) = nullptr) {
    if (cmp) {
        if (reverse) {
            // 降順ソート
            sort(vec.begin(), vec.end(), [cmp](const T& a, const T& b) {
                return cmp(b, a);  // cmp関数を逆にして降順
            });
        } else {
            // 昇順ソート
            sort(vec.begin(), vec.end(), cmp);
        }
    } else {
        // cmpがnullptrの場合（通常の昇順ソート）
        if (reverse) {
            sort(vec.begin(), vec.end(), greater<T>());
        } else {
            sort(vec.begin(), vec.end());
        }
    }
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

// llについて、商、余り、除算、べき
// 整数の商
long long idiv(long long a, long long b) {
    return (a >= 0) ? a / b : ((a + 1) / b) - 1;
}
// 最小非負の余り
long long mod(long long a, long long b = MOD) {
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
//    umap: unordered_map;
//    uset: unordered_set;
//    mset: multiset;
//    umset: unordered_multiset;
//    gpque: max-priority_queue;
//    lpque: min-priority_queue;

//　定数：
//   MOD = 998244353

//  マクロ：
//   rep(i, n): for(ll i = 0; i < n; i++)   変数iをとる
//   rep_range(i, s, t): for(ll i = s; i < t; i++)   sからt-1まで
//   rep_step(i, s, t, b) for(ll i = s; (i - t) * b < 0; i += b) sから、tの直前まで。stepはb
//   rep_in(a, A): for(auto a: A)   変数aがコンテナAを走る
//   elif: else if

//  よく使う関数：
//   [標準出力]
//    print(可変長): 標準出力
//    print_elements(コンテナ, 区切り文字): コンテナ要素の出力 
//   [算術演算]
//    idiv, mod, fdiv: 商, 余り, 小数の除算
//    pow: べき（オプションで剰余）
//   [二分探索]
//    biect_left(コンテナ, 文字): 指定値未満の個数
//    biect_right(コンテナ, 文字): 指定値以下の個数
//   [コンテナ関係]
//    ・ソート
//     sort_vector(vector, reverse)
//     sort_by_key(vector, reverse, key)  ** ll key(T a)「aの大きさ」
//     sort_by_cmp(vector, reverse, cmp)  ** bool cmp(T a, T b)「aがbより大きい」
//    ・コンテナ変換
//     to_{vector/set/mset/uset/umset/deque/gpque/lpqueのいずれか}(container) 
//    ・lpque, gpque の作成
//     make_gpque({...}) / make_lpque({...})
//    ・長さ(llで出力)
//     len(container)

// pair のハッシュ関数を定義
template <typename T1, typename T2>
struct hash<pair<T1, T2>> {
    size_t operator()(const pair<T1, T2>& p) const {
        // 各要素のハッシュを組み合わせる方法
        size_t h1 = hash<T1>()(p.first); // first のハッシュ
        size_t h2 = hash<T2>()(p.second); // second のハッシュ
        return h1 ^ (h2 << 1);  // ハッシュ値を組み合わせる
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

int main(){
  cout << setprecision(18);
  //*****
}

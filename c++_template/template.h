#include <bits/stdc++.h>
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
using pque = priority_queue<T>;

// pairの三つ組版
template <typename T1, typename T2, typename T3>
struct triplet {
    T1 first;    // 第一の要素
    T2 second;   // 第二の要素
    T3 third;    // 第三の要素

    // コンストラクタ
    triplet(T1 f, T2 s, T3 t) : first(f), second(s), third(t) {}

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
#define MOD 998244353;
#define elif else if
#define rep(i, n) for(ll i = 0; i < n; i++)
#define rep_in(a, A) for(auto a: A)

// コンテナの標準出力をオーバーロード
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
ostream& operator<<(ostream& os, const priority_queue<T>& pq) {
    priority_queue<T> temp = pq;
    os << "[(priority_queue)";
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
//    pque: priority_queue;

//　定数：
//   MOD = 998244353

//  マクロ：
//   rep(i, n): for(ll i = 0; i < n; i++)   変数iをとる
//   rep(a, A): for(auto a: A)   変数aがコンテナAを走る
//   elif: else if

//  よく使う関数：
//   [標準出力]
//    print(可変長): 標準出力
//    print_elements(コンテナ, 区切り文字): コンテナ要素の出力 

class bigint {
public:
    bool is_negative;
    vector<unsigned long long> digits;
    
    bigint() {
      is_negative = false;
      digits = {0};
    }
    
    // 整数型からのコンストラクタ（任意の整数型）
    template <typename T>
    bigint(T val) {
        is_negative = (val < 0);
        if (val < 0) val = -val;
        while (val > 0) {
            digits.push_back(val & 0xFFFFFFFF);  // 32bitずつ格納
            val >>= 32;
        }
        if (digits.empty()) digits.push_back(0);
    }

    // 文字列からのコンストラクタ
    bigint(const string &s) {
        is_negative = (s[0] == '-');
        string num_str = is_negative ? s.substr(1) : s;

        unsigned long long num = 0;
        for (char c : num_str) {
            num = num * 10 + (c - '0');
            if (num >= 0x100000000) {  // 2^32を超える
                digits.push_back(num & 0xFFFFFFFF);
                num >>= 32;
            }
        }
        if (num > 0) digits.push_back(num);
        if (digits.empty()) digits.push_back(0);
    }

    // 位取りの整理
    void normalize() {
        while (digits.size() > 1 && digits.back() == 0) {
            digits.pop_back();
        }
        if (digits.size() == 1 && digits[0] == 0) {
            is_negative = false;
        }
    }

    // 結果表示
    void print() const {
        if (is_negative && !(digits.size() == 1 && digits[0] == 0)) cout << "-";
        if (digits.size() == 2) {
          cout << ((digits[1] << 32) | digits[0]);
        }
        else {
            for (int i = 0; i < digits.size(); ++i) {
                cout << digits[i];
                if (i > 0) cout << "* 2^" <<  (32 * i);
                if (i < digits.size() - 1) cout << (is_negative ? " - " : " + "); // 区切り
            }
        }
    }

    // 加算
    bigint operator+(const bigint &other) const {
        bigint result;
        if (is_negative == other.is_negative) {
            result = add_abs(*this, other);
            result.is_negative = is_negative;
        } else {
            if (abs_compare(*this, other) >= 0) {
                result = subtract_abs(*this, other);
                result.is_negative = is_negative;
            } else {
                result = subtract_abs(other, *this);
                result.is_negative = !is_negative;
            }
        }
        return result;
    }

    // 減算
    bigint operator-(const bigint &other) const {
        bigint result;
        if (is_negative != other.is_negative) {
            result = add_abs(*this, other);
            result.is_negative = is_negative;
        } else {
            if (abs_compare(*this, other) >= 0) {
                result = subtract_abs(*this, other);
                result.is_negative = is_negative;
            } else {
                result = subtract_abs(other, *this);
                result.is_negative = !is_negative;
            }
        }
        return result;
    }

    // 乗算
    bigint operator*(const bigint &other) const {
        bigint result;
        result.digits.resize(digits.size() + other.digits.size(), 0);

        for (size_t i = 0; i < digits.size(); ++i) {
            unsigned long long carry = 0;
            for (size_t j = 0; j < other.digits.size(); ++j) {
                unsigned long long prod = digits[i] * other.digits[j] + result.digits[i + j] + carry;
                result.digits[i + j] = prod & 0xFFFFFFFF;
                carry = prod >> 32;
            }
            result.digits[i + other.digits.size()] = carry;
        }
        
        result.is_negative = (is_negative != other.is_negative);
        result.normalize();
        return result;
    }

    // 比較演算（絶対値で比較）
    int abs_compare(const bigint &a, const bigint &b) const {
        if (a.digits.size() != b.digits.size()) {
            return a.digits.size() < b.digits.size() ? -1 : 1;
        }
        for (int i = a.digits.size() - 1; i >= 0; --i) {
            if (a.digits[i] != b.digits[i]) {
                return a.digits[i] < b.digits[i] ? -1 : 1;
            }
        }
        return 0;
    }

    // 絶対値での加算
    bigint add_abs(const bigint &a, const bigint &b) const {
        bigint res;
        unsigned long long carry = 0;
        size_t n = max(a.digits.size(), b.digits.size());

        res.digits.resize(n, 0);
        for (size_t i = 0; i < n; ++i) {
            unsigned long long a_digit = (i < a.digits.size()) ? a.digits[i] : 0;
            unsigned long long b_digit = (i < b.digits.size()) ? b.digits[i] : 0;
            unsigned long long sum = a_digit + b_digit + carry;
            res.digits[i] = sum & 0xFFFFFFFF;
            carry = sum >> 32;
        }
        if (carry > 0) res.digits.push_back(carry);
        res.normalize();
        return res;
    }

    // 絶対値での減算
    bigint subtract_abs(const bigint &a, const bigint &b) const {
        bigint res;
        unsigned long long borrow = 0;
        size_t n = a.digits.size();

        res.digits.resize(n, 0);
        for (size_t i = 0; i < n; ++i) {
            unsigned long long a_digit = a.digits[i];
            unsigned long long b_digit = (i < b.digits.size()) ? b.digits[i] : 0;
            unsigned long long diff = a_digit - b_digit - borrow;
            if (diff > a_digit) borrow = 1;
            else borrow = 0;
            res.digits[i] = diff;
        }

        res.normalize();
        return res;
    }

    // 等しいか比較
    bool operator==(const bigint &other) const {
        return is_negative == other.is_negative && digits == other.digits;
    }

    // 異なるか比較
    bool operator!=(const bigint &other) const {
        return !(*this == other);
    }

    // 小なり
    bool operator<(const bigint &other) const {
        if (is_negative != other.is_negative) return is_negative;
        return is_negative ? abs_compare(*this, other) > 0 : abs_compare(*this, other) < 0;
    }

    // 小なりイコール
    bool operator<=(const bigint &other) const {
        return *this < other || *this == other;
    }

    // 大なり
    bool operator>(const bigint &other) const {
        return !(*this <= other);
    }

    // 大なりイコール
    bool operator>=(const bigint &other) const {
        return !(*this < other);
    }

    // AND 演算子
    bigint operator&(const bigint &other) const {
        bigint result;
        size_t size = max(digits.size(), other.digits.size());
        result.digits.resize(size, 0);

        for (size_t i = 0; i < size; ++i) {
            unsigned long long a_digit = (i < digits.size()) ? digits[i] : 0;
            unsigned long long b_digit = (i < other.digits.size()) ? other.digits[i] : 0;
            result.digits[i] = a_digit & b_digit;
        }

        result.is_negative = false;  // 負数のビット演算は扱わない
        result.normalize();
        return result;
    }

    // OR 演算子
    bigint operator|(const bigint &other) const {
        bigint result;
        size_t size = max(digits.size(), other.digits.size());
        result.digits.resize(size, 0);

        for (size_t i = 0; i < size; ++i) {
            unsigned long long a_digit = (i < digits.size()) ? digits[i] : 0;
            unsigned long long b_digit = (i < other.digits.size()) ? other.digits[i] : 0;
            result.digits[i] = a_digit | b_digit;
        }

        result.is_negative = false;  // 負数のビット演算は扱わない
        result.normalize();
        return result;
    }
    
    // XOR 演算子
    bigint operator^(const bigint &other) const {
        bigint result;
        size_t size = max(digits.size(), other.digits.size());
        result.digits.resize(size, 0);

        for (size_t i = 0; i < size; ++i) {
            unsigned long long a_digit = (i < digits.size()) ? digits[i] : 0;
            unsigned long long b_digit = (i < other.digits.size()) ? other.digits[i] : 0;
            result.digits[i] = a_digit ^ b_digit;
        }

        result.is_negative = false;  // 負数のビット演算は扱わない
        result.normalize();
        return result;
    }
};

// 標準入力からの読み取り
istream& operator>>(istream& in, bigint& b) {
    long long s;
    in >> s;
    b = bigint(s);
    return in;
}

// 標準出力への書き込み
ostream& operator<<(ostream& out, const bigint& b) {
    b.print();
    return out;
}

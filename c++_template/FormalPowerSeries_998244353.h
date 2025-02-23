// total_length <= 2^23
const unsigned long long mod = 998244353ULL;
const unsigned long long mod2 = (mod * mod) << 2;

const vector<unsigned long long> root = {1, 998244352, 911660635, 372528824, 929031873, 452798380, 922799308, 781712469, 476477967, 166035806, 258648936, 584193783, 63912897, 350007156, 666702199, 968855178, 629671588, 24514907, 996173970, 363395222, 565042129, 733596141, 267099868, 15311432};
const vector<unsigned long long> root_inv = {1, 998244352, 86583718, 509520358, 337190230, 87557064, 609441965, 135236158, 304459705, 685443576, 381598368, 335559352, 129292727, 358024708, 814576206, 708402881, 283043518, 3707709, 121392023, 704923114, 950391366, 428961804, 382752275, 469870224};
const vector<unsigned long long> rate2 = {372528824, 337190230, 454590761, 816400692, 578227951, 180142363, 83780245, 6597683, 70046822, 623238099, 183021267, 402682409, 631680428, 344509872, 689220186, 365017329, 774342554, 729444058, 102986190, 128751033, 395565204};
const vector<unsigned long long> rate2_inv = {509520358, 929031873, 170256584, 839780419, 282974284, 395914482, 444904435, 72135471, 638914820, 66769500, 771127074, 985925487, 262319669, 262341272, 625870173, 768022760, 859816005, 914661783, 430819711, 272774365, 530924681};

/* 
// total_length <= 2^26
const unsigned long long mod = 469762049ULL;
const unsigned long long mod2 = (mod * mod) << 2;

const vector<unsigned long long> root = {1, 469762048, 450151958, 129701348, 426037461, 244709223, 210853138, 189158148, 338628632, 25153357, 110059487, 165447688, 244412522, 62025685, 19512135, 372627191, 386080322, 321129726, 422997289, 49553715, 197868229, 297449090, 391371999, 385303873, 320192759, 4782969, 2187};
const vector<unsigned long long> root_inv = {1, 469762048, 19610091, 26623616, 358191614, 278703339, 58439238, 230980285, 215855482, 436579181, 458753944, 63413564, 309717554, 318475127, 317243944, 271119509, 380600599, 417932558, 44275780, 96523612, 256026808, 131257384, 426545640, 300035530, 49490419, 392193156, 410692747};
const vector<unsigned long long> rate2 = {129701348, 358191614, 402152097, 345038213, 211638587, 4122572, 386688150, 144456548, 449668585, 142445815, 210245808, 60798333, 117629089, 394258599, 161246834, 392043613, 213529764, 192527415, 113333535, 462069946, 155386099, 333453653, 5562051, 311675917};
const vector<unsigned long long> rate2_inv = {26623616, 426037461, 269604844, 184209115, 123638379, 137578908, 217296754, 450792571, 303798807, 187328293, 237091113, 365548979, 340531665, 22112954, 343119676, 386493255, 429873751, 192036429, 206122223, 224823445, 147517911, 461548140, 398137, 276589614};
*/

// other mods:  https://www.mathenachia.blog/ntt-mod-list-01/

void fft(vector<unsigned long long> &a) {
    size_t N = a.size();
    size_t log_len = 63 - countl_zero(N); // log2 of block size
    if (log_len % 2) { 
        for (size_t i = 0; i < (N >> 1); i++) {
            unsigned long long p0 = a[i];
            unsigned long long p1 = a[i + (N >> 1)];
            a[i] = (p0 + p1) % mod;
            a[i + (N >> 1)] = (p0 + mod - p1) % mod;
        }
        log_len -= 1;
    }
    
    log_len -= 2; // log2 of quarter size
    while (log_len <= 63 && 0 <= log_len) {
        unsigned long long rot = 1;
        size_t L = 1 << log_len;
        for (size_t j = 0; j < (N >> (2 + log_len)); j++) {
            size_t offset = j << (2 + log_len);
            unsigned long long rot2 = (rot * rot) % mod;
            unsigned long long rot3 = (rot * rot2) % mod;
            for (size_t i = 0; i < L; i++) {
                unsigned long long p0 = a[offset + i];
                unsigned long long p1 = a[offset + i + L] * rot;
                unsigned long long p2 = a[offset + i + L * 2] * rot2;
                unsigned long long p3 = a[offset + i + L * 3] * rot3;
                  
                unsigned long long t0 = p0 + p2;
                unsigned long long t1 = p1 + p3;
                unsigned long long t2 = p0 + (mod2 - p2);
                unsigned long long t3 = root[2] * ((p1 + (mod2 - p3)) % mod);
                  
                a[offset + i] = (t0 + t1) % mod;
                a[offset + i + L] = (t0 + (mod2 - t1)) % mod;
                a[offset + i + 2 * L] = (t2 + t3) % mod;
                a[offset + i + 3 * L] = (t2 + (mod2 - t3)) % mod;
            }
            rot *= rate2[countr_zero(j + 1)];
            rot %= mod;
        }
        log_len -= 2;
    }
}
void ifft(vector<unsigned long long> &a) {
    size_t N = a.size();
    
    size_t log_len = 0; // log2 of current size of quarter
    while (log_len + 2 <= 63 - countl_zero(N)) {
        unsigned long long irot = 1;
        size_t L = 1 << log_len;
        for (size_t j = 0; j < (N >> (2 + log_len)); j++) {
            size_t offset = j << (2 + log_len);
            unsigned long long irot2 = irot * irot % mod;
            unsigned long long irot3 = irot * irot2 % mod;
            for (size_t i = 0; i < L; i++) {
              unsigned long long s0 = a[offset + i];
              unsigned long long s1 = a[offset + i + L];
              unsigned long long s2 = a[offset + i + L * 2];
              unsigned long long s3 = a[offset + i + L * 3];
              
              unsigned long long t0 = s0 + s1;
              unsigned long long t2 = s2 + s3;
              unsigned long long t1 = s0 + (mod - s1);
              unsigned long long t3 = (root_inv[2] * (s2 + (mod - s3))) % mod;
              
              a[offset + i] = (t0 + t2) % mod;
              a[offset + i + L] = (t1 + t3) * irot % mod;
              a[offset + i + 2 * L] = (t0 + (2 * mod - t2)) * irot2 % mod;
              a[offset + i + 3 * L] = (t1 + mod - t3) * irot3 % mod;
            }
            irot *= rate2_inv[countr_zero(j + 1)];
            irot %= mod;
        }
        log_len += 2;
    }
    
    if (log_len + 1 == 63 - countl_zero(N)) {
        for (size_t i = 0; i < (N >> 1); i++) {
            unsigned long long p0 = a[i];
            unsigned long long p1 = a[i + (N >> 1)];
            a[i] = (p0 + p1) % mod;
            a[i + (N >> 1)] = (p0 + mod - p1) % mod;
        }
        log_len += 1;
    }
}

template <typename T>
vector<unsigned long long> _conv_to_ull(vector<T>& a) {
    vector<unsigned long long> a_ull(a.begin(), a.end());
    return a_ull;
}
size_t _next_pow2(size_t s) {
    size_t ns = 1;
    while (ns < s) {
        ns *= 2;
    }
    return ns;
}

template <typename T>
vector<T> FPS_multiply(vector<T>& a, vector<T>& b) {
    if (a.size() == 0 || b.size() == 0) return {};
    
    auto a_ull = _conv_to_ull(a);
    auto b_ull = _conv_to_ull(b);
    
    size_t sz = _next_pow2(a_ull.size() + b_ull.size() - 1);
    a_ull.resize(sz, 0);
    b_ull.resize(sz, 0);
    
    fft(a_ull);
    fft(b_ull);
    
    rep(i, a_ull.size()) {
        a_ull[i] *= b_ull[i];
        a_ull[i] %= mod;
    }
    ifft(a_ull);
    
    long long sz_inv = mod_inv(static_cast<long long>(sz), static_cast<long long>(mod));
    
    vector<T> ans(a_ull.begin(), a_ull.begin() + (a.size() + b.size() - 1));
    rep_in(&v, ans) {
        v *= sz_inv;
        v %= mod;
    }
    return ans;
}

template <typename T>
vector<T> FPS_inv(vector<T>& a) {
    auto a_ull = _conv_to_ull(a);
    a_ull.resize(_next_pow2(a.size()), 0);
    
    vector<unsigned long long> ans = {mod_inv(static_cast<long long>(a[0]), static_cast<long long>(mod))};
    while (ans.size() < a_ull.size()) {
        
        vector<unsigned long long> ans_copy(ans.begin(), ans.end());
        ans_copy.resize(ans.size() * 2, 0);
        
        vector<unsigned long long> a_now(a_ull.begin(), a_ull.begin() + ans_copy.size());
        fft(a_now);
        fft(ans_copy);
        auto mod2 = mod * mod;
        rep(i, ans_copy.size()) {
            a_now[i] *= ans_copy[i];
            a_now[i] = mod2 - a_now[i];
            a_now[i] %= mod;
        }
        ifft(a_now);
        
        vector<unsigned long long> e_now(a_now.begin() + (ans_copy.size() / 2), a_now.end());
        e_now.resize(ans_copy.size(), 0);
        
        fft(e_now);
        rep(i, ans_copy.size()) {
            e_now[i] *= ans_copy[i];
            e_now[i] %= mod;
        }
        ifft(e_now);
        
        e_now.resize(ans_copy.size() / 2);
        long long sz2_inv = mod_inv(static_cast<long long>(ans_copy.size() * ans_copy.size() % mod), static_cast<long long>(mod));
        rep_in(&v, e_now) {
            v *= sz2_inv;
            v %= mod;
        }
        ans.insert(ans.end(), e_now.begin(), e_now.end());
    }
    vector<T> ret(ans.begin(), ans.begin() + a.size());
    return ret;
}

template <typename T>
vector<T> FPS_diff(vector<T>& a) { 
    // deg N -> deg N-1
    vector<T> ans(a.begin() + 1, a.end());
    for (int i = 0; i < a.size() - 1; i++) {
        ans[i] *= i + 1;
        ans[i] %= mod;
    }
    return ans;
}

template <typename T>
vector<T> FPS_integral(vector<T>& a, T c = T(0)) { 
    // deg N -> deg N+1
    vector<T> ans(a.size() + 1, c);
    copy(a.begin(), a.end(), ans.begin() + 1);
    
    long long mod_ll = static_cast<ll>(mod);
    for (long long i = 0; i < a.size() + 1; i++) {
        ans[i] *= static_cast<T>(mod_inv(i, mod_ll));
        ans[i] %= mod_ll;
    }
    return ans;
}

template <typename T>
vector<T> FPS_log(vector<T>& a) {
    assert(a[0] == 1);
    vector<T> a_inv = FPS_inv(a);
    vector<T> a_diff = FPS_diff(a);
    
    vector<T> ans_diff = FPS_multiply(a_diff, a_inv);
    
    ans_diff.resize(a.size() - 1);
    return FPS_integral(ans_diff);
}

template <typename T>
vector<T> FPS_exp(vector<T>& a) {
    assert(a[0] == 0);
    if (a.size() == 1) return {1};
    
    vector<unsigned long long> a_ull = _conv_to_ull(a);
    a_ull.resize(_next_pow2(a.size()), 0);
    
    vector<unsigned long long> ans = {1, a[1] % mod};
    vector<unsigned long long> ans_inv = {1};
    
    vector<unsigned long long> ans_inv_fft = {1, 1, 1, 1};
    
    while (ans.size() < a.size()) {
        vector<unsigned long long> ans_copy(ans.begin(), ans.end());
        ans_copy.resize(ans.size() * 2, 0);
        
        vector<unsigned long long> ans_fft(ans_copy.begin(), ans_copy.end());
        fft(ans_fft);
        
        for (size_t i = 0; i < ans_copy.size(); i++) {
            unsigned long long tmp = 2 + mod * mod - ans_fft[i] * ans_inv_fft[i];
            ans_inv_fft[i] *= (tmp % mod);
            ans_inv_fft[i] %= mod;
        }
        ans_inv = ans_inv_fft;
        ifft(ans_inv);
        ans_inv.resize(ans.size());
        long long mod_ll = static_cast<long long>(mod);
        long long sz_inv = mod_inv(static_cast<long long>(ans_copy.size()), mod_ll);
        for (auto& v: ans_inv) {
            v *= sz_inv;
            v %= mod;
        }
        
        vector<unsigned long long> aug1(a_ull.begin(), a_ull.begin() + ans.size());
        for (int i = 0; i < aug1.size(); i++) {
            aug1[i] *= i;
            aug1[i] %= mod;
        }
        // aug1 = q = h'
        
        fft(aug1);
        for (size_t i = 0; i < aug1.size(); i++) {
            aug1[i] *= ans_fft[i];
            aug1[i] %= mod;
        }
        ifft(aug1);
        for (auto& v: aug1) {
            v *= sz_inv * 2;
            v %= mod;
        }
        // aug1 = xr
        
        for (int i = 0; i < aug1.size(); i++) {
            aug1[i] = i * ans[i] + mod - aug1[i];
            aug1[i] %= mod;
        }
        // aug1 = s = xf' - xr
        
        aug1.resize(aug1.size() * 2, 0);
        ans_inv_fft = ans_inv;
        ans_inv_fft.resize(aug1.size() * 2, 0);
        
        fft(aug1);
        fft(ans_inv_fft);
        for (size_t i = 0; i < aug1.size(); i++) {
            aug1[i] *= ans_inv_fft[i];
            aug1[i] %= mod;
        }
        ifft(aug1);
        for (auto& v: aug1) {
            v *= sz_inv;
            v %= mod;
        }
        aug1.resize(ans.size());
        // aug1 = t = gs
        
        for (long long i = 0; i < ans.size(); i++) {
            aug1[i] = a_ull[i + ans.size()] + mod * mod - mod_inv(static_cast<long long>(i + ans.size()), mod_ll) * aug1[i];
            aug1[i] %= mod;
        }
        // aug1 = u = (h - \int tx^(m-1) dx) / x^m
        
        aug1.resize(ans.size() * 2, 0);
        fft(aug1);
        for (size_t i = 0; i < aug1.size(); i++) {
            aug1[i] *= ans_fft[i];
            aug1[i] %= mod;
        }
        ifft(aug1);
        for (auto& v: aug1) {
            v *= sz_inv;
            v %= mod;
        }
        aug1.resize(ans.size());
        // aug1 = v = fu
        
        ans.insert(ans.end(), aug1.begin(), aug1.end());
        // ans <- ans + aug1 * x^m
    }
    vector<T> ans_T(ans.begin(), ans.begin() + a.size()); 
    return ans_T;
}

template <typename T>
vector<T> FPS_sqrt(vector<T>& a) {
    assert(a[0] == 1);
    vector<unsigned long long> a_ull = _conv_to_ull(a);
    a_ull.resize(_next_pow2(a.size()), 0);
    
    long long mod_ll = static_cast<long long>(mod);
    long long inv_2 = mod_inv(2LL, mod_ll);
    
    vector<unsigned long long> ans = {1ULL};
    while (ans.size() < a.size()) {
        vector<unsigned long long> ans_copy(ans.begin(), ans.end());
        ans_copy.resize(ans.size() * 2, 0);
        
        vector<unsigned long long> ans_inv = FPS_inv(ans_copy);
        vector<unsigned long long> a_now(a_ull.begin(),a_ull.begin() + ans_copy.size());
        
        vector<unsigned long long> ans_pre = FPS_multiply(ans_inv, a_now);
        vector<unsigned long long> ans_ext(ans_pre.begin() + ans.size(), ans_pre.begin() + ans.size() * 2);
        for (auto& v: ans_ext) {
            v *= inv_2;
            v %= mod;
        }
        ans.insert(ans.end(), ans_ext.begin(), ans_ext.end());
    }
    vector<T> ans_T(ans.begin(), ans.begin() + a.size()); 
    return ans_T;
}

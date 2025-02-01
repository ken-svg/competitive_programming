const unsigned long long mod = 998244353;
const vector<unsigned long long> root = {1, 998244352, 911660635, 372528824, 929031873, 452798380, 922799308, 781712469, 476477967, 166035806, 258648936, 584193783, 63912897, 350007156, 666702199, 968855178, 629671588, 24514907, 996173970, 363395222, 565042129, 733596141, 267099868, 15311432};
const vector<unsigned long long> root_inv = {1, 998244352, 86583718, 509520358, 337190230, 87557064, 609441965, 135236158, 304459705, 685443576, 381598368, 335559352, 129292727, 358024708, 814576206, 708402881, 283043518, 3707709, 121392023, 704923114, 950391366, 428961804, 382752275, 469870224};
const vector<unsigned long long> rate2 = {372528824, 337190230, 454590761, 816400692, 578227951, 180142363, 83780245, 6597683, 70046822, 623238099, 183021267, 402682409, 631680428, 344509872, 689220186, 365017329, 774342554, 729444058, 102986190, 128751033};
const vector<unsigned long long> rate2_inv = {509520358, 929031873, 170256584, 839780419, 282974284, 395914482, 444904435, 72135471, 638914820, 66769500, 771127074, 985925487, 262319669, 262341272, 625870173, 768022760, 859816005, 914661783, 430819711, 272774365};

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
                unsigned long long p1 = (a[offset + i + L] * rot) % mod;
                unsigned long long p2 = (a[offset + i + L * 2] * rot2) % mod;
                unsigned long long p3 = (a[offset + i + L * 3] * rot3) % mod;
                  
                unsigned long long t0 = p0 + p2;
                unsigned long long t1 = p1 + p3;
                unsigned long long t2 = p0 + (mod - p2);
                unsigned long long t3 = (root[2] * (p1 + (mod - p3))) % mod;
                  
                a[offset + i] = (t0 + t1) % mod;
                a[offset + i + L] = (t0 + (2 * mod - t1)) % mod;
                a[offset + i + 2 * L] = (t2 + t3) % mod;
                a[offset + i + 3 * L] = (t2 + (mod - t3)) % mod;
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
              unsigned long long t3 = root_inv[2] * (s2 + (mod - s3)) % mod;
              
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
vector<T> convolution(vector<vector<T>>& convoluted_lists) {
    size_t res_size = 1;
    for (auto& a: convoluted_lists) {
        if (a.size() == 0) return {};
        res_size += a.size() - 1;
    }
    size_t total_size = 1 << (64 - countl_zero(res_size - 1));
    // print(total_size, countl_zero(res_size - 1), res_size);
    
    vector<T>& first = convoluted_lists[0];
    vector<unsigned long long> fft_res(total_size, 0);
    for (size_t i = 0; i < first.size(); i++) {
        fft_res[i] = (first[i] + mod) % mod;
    }
    fft(fft_res);
    
    for (size_t j = 1; j < convoluted_lists.size(); j++) {
        vector<T>& target = convoluted_lists[j];
        vector<unsigned long long> fft_target(total_size, 0);
        for (size_t i = 0; i < target.size(); i++) {
            fft_target[i] = (target[i] + mod) % mod;
        }
        fft(fft_target);
        for (size_t i = 0; i < total_size; i++) {
            fft_res[i] *= fft_target[i];
            fft_res[i] %= mod;
        }
    } 
    
    ifft(fft_res);
    for (auto& a : fft_res) {
        a *= mod_inv(total_size, mod);
        a %= mod;
    }
    
    return vector<T>(fft_res.begin(), fft_res.begin() + res_size);
}

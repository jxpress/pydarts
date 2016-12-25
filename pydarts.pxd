cdef extern from "darts.h" namespace "Darts":
    struct result_pair_type:
        int value
        size_t length

    cdef cppclass DoubleArray:
        int build(size_t size, const char**)
        int save(const char*)
        int open(const char*)
        int size()
        void clear()
        size_t commonPrefixSearch(char *key, result_pair_type*, size_t)
        void exactMatchSearch(const char*, int, size_t, size_t) const

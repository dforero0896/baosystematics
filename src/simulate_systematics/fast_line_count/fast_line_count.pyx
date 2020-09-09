from libc.stdio cimport *

cdef extern from "stdio.h":
    #FILE * fopen ( const char * filename, const char * mode )
    FILE *fopen(const char *, const char *)
    #int fclose ( FILE * stream )
    int fclose(FILE *)
    #ssize_t getline(char **lineptr, size_t *n, FILE *stream);
    ssize_t getline(char **, size_t *, FILE *)


def count_lines(str filename):
    filename_byte_string = filename.encode("UTF-8")
    cdef char* fname = filename_byte_string
    cdef int num_lines=0;
    cdef FILE* cfile
    cfile = fopen(fname, "rb")
    if cfile == NULL:
        raise FileNotFoundError(2, "ERROR: No such file or directory: '%s'" % filename)

    cdef char * line = NULL
    cdef size_t l = 0
    cdef ssize_t read

    while True:
        read = getline(&line, &l, cfile)
        if read == -1: break
        num_lines+=1;
    fclose(cfile)

    return num_lines

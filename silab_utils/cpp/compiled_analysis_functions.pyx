# distutils: language = c++
# cython: boundscheck=False
# cython: wraparound=False

import numpy as np
cimport numpy as cnp
from numpy cimport ndarray

from tables import dtype_from_descr
from libc.stdint cimport uint8_t, uint16_t, uint32_t, uint64_t, int64_t

cnp.import_array()  # if array is used it has to be imported, otherwise possible runtime error

cdef extern from "CompiledAnalysisFunctions.h":
    void histogram_1d(int*& x, const unsigned int& rSize, const unsigned int& rNbinsX, uint32_t*& rResult) except +
    void histogram_2d(int*& x, int*& y, const unsigned int& rSize, const unsigned int& rNbinsX, const unsigned int& rNbinsY, uint32_t*& rResult) except +
    void histogram_3d(int*& x, int*& y, int*& z, const unsigned int& rSize, const unsigned int& rNbinsX, const unsigned int& rNbinsY, const unsigned int& rNbinsZ, uint32_t*& rResult) except +

def hist_1d(cnp.ndarray[cnp.int32_t, ndim=1] x, const unsigned int& n_x, cnp.ndarray[cnp.uint32_t, ndim=1] array_result):
    histogram_1d(<int*&> x.data, <const unsigned int&> x.shape[0], <const unsigned int&> n_x, <uint32_t*&> array_result.data) 

def hist_2d(cnp.ndarray[cnp.int32_t, ndim=1] x, cnp.ndarray[cnp.int32_t, ndim=1] y, const unsigned int& n_x, const unsigned int& n_y, cnp.ndarray[cnp.uint32_t, ndim=1] array_result):
    histogram_2d(<int*&> x.data, <int*&> y.data, <const unsigned int&> x.shape[0], <const unsigned int&> n_x, <const unsigned int&> n_y, <uint32_t*&> array_result.data)
    
def hist_3d(cnp.ndarray[cnp.int32_t, ndim=1] x, cnp.ndarray[cnp.int32_t, ndim=1] y, cnp.ndarray[cnp.int32_t, ndim=1] z, const unsigned int& n_x, const unsigned int& n_y, const unsigned int& n_z, cnp.ndarray[cnp.uint32_t, ndim=1] array_result, throw_exception = True):
    histogram_3d(<int*&> x.data, <int*&> y.data, <int*&> z.data, <const unsigned int&> x.shape[0], <const unsigned int&> n_x, <const unsigned int&> n_y, <const unsigned int&> n_z, <uint32_t*&> array_result.data)

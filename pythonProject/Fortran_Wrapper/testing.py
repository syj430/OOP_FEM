import numpy as np
import time
import matmul1


M1 = 80
N1M2 = 300
N2 = 80

a = np.empty((M1,N1M2), dtype=np.float64)
b = np.empty((N1M2,N1M2), dtype=np.float64)
c = np.empty((M1,M1), dtype=np.float64)
print(a.shape)
print(b.shape)
a[:] = np.random.rand(M1, N1M2)
b[:] = np.random.rand(N1M2, N1M2)


# Numpy
start = time.time()
# c = np.dot(a,b)
c = a @ b @ np.transpose(a)
stop = time.time()
print(c)
print('Numpy: ', (stop - start)*1000, 'msec')


# # Fortran call
start = time.time()
c = matmul1.matmul1(a,b,M1,N1M2)
stop = time.time()
print(c)
print('Fortran: ', (stop - start)*1000, 'msec')


# import numpy as np
# import time
#
# #import os
# #os.system('f2py -c matmul1 -m operator.f90')
# import operator
#
#
# NI = 8
# NJ = 3
#
# a = np.empty((NI, NJ), dtype=np.float64)    # 8x3
# b = np.empty((NJ, NJ), dtype=np.float64)    # 3x3
# c = np.empty((NI, NI), dtype=np.float64)    # 8x8
# print(a.shape)
# print(b.shape)
# a[:] = np.random.rand(NI, NJ)
# b[:] = np.random.rand(NJ, NJ)
# # print(a)
# # print(a[:])
# #
# # NI = 8
# # NJ = 3
# # Fortran call
# start = time.time()
# c = operator.matmul(a, b, NI, NJ)
# stop = time.time()
# # print(c)
# print('Fortran took ', (stop - start), 'sec')
#
#
# # Numpy
# start = time.time()
# c = a @ b @ np.transpose(a)
# stop = time.time()
# # print(c)
# print('Numpy took ', (stop - start), 'sec')






import numpy as np
import time
import matmul1


M1 = 8
N1M2 = 3
N2 = 8

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





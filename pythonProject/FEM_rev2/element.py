from node import *
from material import *
import numpy as np

class ELEMENT:
    def __init__(self, data):
        self.elem_type = data['Element']['elem_type']
        self.element = data['Element']['element']
        [self.E, self.nu] = ELASTIC(data).getElastic()
        self.node = NODE(data).getNodeData()

    def getElementData(self):
        return self.element

    def DMAT(self):
        # 평면응력
        if self.elem_type == 'CPS4':        # 평면응력
            D = np.zeros((3,3))
            D[0,0] = 1
            D[1,1] = 1
            D[2,2] = 0.5 * (1 - self.nu)
            D[0,1] = self.nu
            D[1,0] = D[0,1]
            D = self.E / (1 - self.nu**2) * D
        return D

    def Bmat(self, e, s ,t):
        nod = self.node
        elem = self.element
        J = self.JACOBIAN(e, s, t)

        # 1-D
        if self.dim == 1:
            n1  = lambda xi : -(xi-1)/2
            n2  = lambda xi : (xi+1)/2
            dn1 = lambda xi : -1/2
            dn2 = lambda xi : 1/2

            N = [n1, n2]
            B = [dn1, dn2]

        if self.dim == 2:
            x1 = nod[int(elem[e][1]) - 1][1]
            y1 = nod[int(elem[e][1]) - 1][2]
            x2 = nod[int(elem[e][2]) - 1][1]
            y2 = nod[int(elem[e][2]) - 1][2]
            x3 = nod[int(elem[e][3]) - 1][1]
            y3 = nod[int(elem[e][3]) - 1][2]
            x4 = nod[int(elem[e][4]) - 1][1]
            y4 = nod[int(elem[e][4]) - 1][2]

            a = 0.25 * (y1 * (s - 1) + y2 * (-1 - s) + y3 * (1 + s) + y4 * (1 - s))
            b = 0.25 * (y1 * (t - 1) + y2 * (1 - t) + y3 * (1 + t) + y4 * (-1 - t))
            c = 0.25 * (x1 * (t - 1) + x2 * (1 - t) + x3 * (1 + t) + x4 * (-1 - t))
            d = 0.25 * (x1 * (s - 1) + x2 * (-1 - s) + x3 * (1 + s) + x4 * (1 - s))

            N1_s = 0.25 * (t - 1)
            N2_s = 0.25 * (1 - t)
            N3_s = 0.25 * (1 + t)
            N4_s = 0.25 * (-t - 1)
            N1_t = 0.25 * (s - 1)
            N2_t = 0.25 * (-1 - s)
            N3_t = 0.25 * (1 + s)
            N4_t = 0.25 * (1 - s)

            B1 = np.array(
                [[a * N1_s - b * N1_t, 0], [0, c * N1_t - d * N1_s], [c * N1_t - d * N1_s, a * N1_s - b * N1_t]])
            B2 = np.array(
                [[a * N2_s - b * N2_t, 0], [0, c * N2_t - d * N2_s], [c * N2_t - d * N2_s, a * N2_s - b * N2_t]])
            B3 = np.array(
                [[a * N3_s - b * N3_t, 0], [0, c * N3_t - d * N3_s], [c * N3_t - d * N3_s, a * N3_s - b * N3_t]])
            B4 = np.array(
                [[a * N4_s - b * N4_t, 0], [0, c * N4_t - d * N4_s], [c * N4_t - d * N4_s, a * N4_s - b * N4_t]])

            B = np.concatenate([B1, B2, B3, B4], axis=1) / J
        return B


    def JACOBIAN(self, e, s, t):
        nod = self.node
        elem = self.element

        if self.dim == 2:
            x1 = nod[int(elem[e][1]) - 1][1]
            y1 = nod[int(elem[e][1]) - 1][2]
            x2 = nod[int(elem[e][2]) - 1][1]
            y2 = nod[int(elem[e][2]) - 1][2]
            x3 = nod[int(elem[e][3]) - 1][1]
            y3 = nod[int(elem[e][3]) - 1][2]
            x4 = nod[int(elem[e][4]) - 1][1]
            y4 = nod[int(elem[e][4]) - 1][2]

            Xc = np.array([[x1], [x2], [x3], [x4]])
            Yc = np.array([[y1], [y2], [y3], [y4]])

            Jmat = np.array([[0, 1-t, t-s, s-1],[t-1, 0, s+1, -s-t],[s-t,-s-1,0,t+1],[1-s,s+t,-t-1,0]])
            J = 1/8 * np.transpose(Xc) @ Jmat @ Yc
        return J

    def computeke(self, e):
        ke = np.zeros((8, 8))
        Dmat = self.DMAT()

        # FIXME e 바꿔
        h=0.12
        ke = np.zeros((8, 8))
        i = int(self.element[e][1])
        j = int(self.element[e][2])
        k = int(self.element[e][3])
        l = int(self.element[e][4])

        gdof = [2 * i - 2, 2 * i - 1, 2 * j - 2, 2 * j - 1, 2 * k - 2, 2 * k - 1, 2 * l - 2, 2 * l - 1]

        for ss in range(len(self.xg)):
            for tt in range(len(self.xg)):
                s = self.xg[ss]
                t = self.xg[tt]
                W1 = self.wt[ss]
                W2 = self.wt[tt]

                Bmat = self.Bmat(e, s, t)
                J = self.JACOBIAN(e, s, t)
                ke = ke + h * np.transpose(Bmat) @ Dmat @ Bmat * W1 * W2 * J
        # print(type(ke))
        return ke, gdof

class ELEMENT_2D(ELEMENT):
    def __init__(self, data):
        # Gauss Quadrature class
        self.xg = np.array([-np.sqrt(1 / 3), np.sqrt(1 / 3)])
        self.wt = np.array([1, 1])

        ELEMENT.__init__(self, data)
        self.dim = 2


class CPS4(ELEMENT_2D):
    def __init__(self, data):
        ELEMENT_2D.__init__(self, data)

    def ke_mat(self, e):
        ke, gdof = self.computeke(e)
        return ke, gdof

class CPE4(ELEMENT_2D):
    pass

class ELEMENT_3D(ELEMENT):
    def __init__(self, data):
        ELEMENT.__init__(self, data)
        self.dim = 3


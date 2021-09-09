from element import *
from boundary import *
from load import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import matplotlib.cm
import matplotlib.cm as cm
from celluloid import Camera
from matplotlib import animation

class ASSEMBLY:
    def __init__(self):
        self.node = None
        self.element = None

    def getNode(self, enriched_data):
        self.node = NODE(enriched_data).getNodeData()
        return self.node

    def getElement(self, enriched_data):
        self.element = ELEMENT(enriched_data).getElementData()
        self.numel = len(self.element)
        return self.numel

    def numberofNode(self):
        return len(self.node)

    def numberofDOF(self):
        self.dof = 2 * self.numberofNode()
        return self.dof

    def assembleGlobalStiff(self, enriched_data):
        dof = self.numberofDOF()
        K = np.zeros((dof, dof))

        for e in range(self.numel):
            # 요소 강성행렬
            ke, gdof = CPS4(enriched_data).computeke(e)               # Elem_type : CPS4

            # Global stiffness matrix 조립
            for i in range(len(ke)):
                for j in range(len(ke)):
                    K[gdof[i], gdof[j]] = K[gdof[i], gdof[j]] + ke[i, j]

        # plt.spy(K)
        # plt.show()
        return K

    def getBoundary(self, enriched_data):
        K = self.assembleGlobalStiff(enriched_data)
        BC = BOUNDARY(enriched_data)
        self.boundary = BC.getBoundaryData()
        self.nset = BC.getNsetData()

        for bctype in self.boundary.keys():
            if bctype == 'ENCASTRE':
                setname = self.boundary[bctype]
                n = self.nset[setname]
                if len(n) == 2:
                    nodes = n

                else:
                    nodes = np.linspace(n[0], n[1], int(1 + (n[1] - n[0]) / n[2]))
                    # print(nodes)
            else:
                pass


                # for gdof in [1, 12]:
                # for gdof in [1, 22, 43]:
                # for gdof in [1, 52, 103, 154, 205, 256]:
            for gdof in nodes:
                gdof = int(gdof)

                K[2 * gdof - 2, :] = 0
                K[2 * gdof - 1, :] = 0
                K[:, 2 * gdof - 2] = 0
                K[:, 2 * gdof - 1] = 0
                K[2 * gdof - 2, 2 * gdof - 2] = 1
                K[2 * gdof - 1, 2 * gdof - 1] = 1

        return K

    def showSparseMatrix(self,enriched_data):
        K = self.getBoundary(enriched_data)
        plt.spy(K)
        plt.show()


    def getLoad(self, enriched_data):
        self.load = CLOAD(enriched_data).getCloadData()
        BC = BOUNDARY(enriched_data)
        self.nset = BC.getNsetData()

        GF = np.zeros((self.numberofDOF(), 1))

        for bctype in list(self.load.keys()):
            for bc in self.nset[bctype]:
                load = self.load[bctype][1]
                GF[bc-1] = load
            # print(bc, load)
        return GF

class SOLVE(ASSEMBLY):
    def __init__(self):
        ASSEMBLY.__init__(self)

    def displacement(self, data):
        self.getNode(data)
        self.getElement(data)
        K = self.getBoundary(data)
        F = self.getLoad(data)
        u = np.linalg.solve(K, F)
        U = np.reshape(u, (self.numberofNode(), 2))
        # print(u)
        # plt.spy(K)
        # plt.show()
        return u

    def stress(self, data):
        U = self.displacement(data)

        Dmat = CPS4(data).Dmat()

        s = 0
        t = 0
        sigma = np.zeros((3, 1))
        u = np.zeros((8, 1))
        S11 = np.zeros((self.numel, 1))
        S22 = np.zeros((self.numel, 1))
        S12 = np.zeros((self.numel, 1))

        for e in range(self.numel):
            i = int(self.element[e][1])
            j = int(self.element[e][2])
            m = int(self.element[e][3])
            n = int(self.element[e][4])
            # print(i,j,m,n)
            u[0] = U[2 * i - 2]
            u[1] = U[2 * i - 1]
            u[2] = U[2 * j - 2]
            u[3] = U[2 * j - 1]
            u[4] = U[2 * m - 2]
            u[5] = U[2 * m - 1]
            u[6] = U[2 * n - 2]
            u[7] = U[2 * n - 1]

            Bmat = CPS4(data).Bmat(e, s, t)
            sigma = Dmat @ Bmat @ u

            S11[e-1] = sigma[0]
            S22[e-1] = sigma[1]
            S12[e-1] = sigma[2]

        # print(S22)
        # print(S12)

class OUTPUT(SOLVE):
    def __init__(self):
        SOLVE.__init__(self)

    def visual(self, data):

        # converts quad elements into tri elements
        def quads_to_tris(quads):
            tris = [[None for j in range(3)] for i in range(2 * len(quads))]
            for i in range(len(quads)):
                j = 2 * i
                n0 = quads[i][0]
                n1 = quads[i][1]
                n2 = quads[i][2]
                n3 = quads[i][3]
                tris[j][0] = int(n0)
                tris[j][1] = int(n1)
                tris[j][2] = int(n2)
                tris[j + 1][0] = int(n2)
                tris[j + 1][1] = int(n3)
                tris[j + 1][2] = int(n0)
            return tris

        # plots a finite element mesh
        def plot_fem_mesh(nodes_x, nodes_y, elements):
            for element in elements:
                x = [nodes_x[int(element[i])] for i in range(len(element))]
                y = [nodes_y[int(element[i])] for i in range(len(element))]
                plt.fill(x, y, edgecolor='black', fill=False, linewidth=0.25 )

        # FEM data
        u = self.displacement(data)
        disp_data = np.reshape(u, (self.numberofNode(), 2))
        U1 = disp_data[:, 0]
        U2 = disp_data[:, 1]
        U = np.sqrt(U1 ** 2 + U2 ** 2)
        # print(U1)
        print(U2)

        i=0
        for nodal_values in [U1, U2, U]:
            # print(str(nodal_values))
            i+=1
            # nodes_x, nodes_y = self.node[:, 1], self.node[:, 2]
            nodes_x, nodes_y = self.node[:, 1] + U1 * 100, self.node[:, 2] + U2 * 100
            # nodal_values = U1
            elements_quads = self.element[:, 1:5] - 1
            elements = elements_quads

            # convert all elements into triangles
            elements_all_tris = quads_to_tris(elements_quads)

            # create an unstructured triangular grid instance
            triangulation = tri.Triangulation(nodes_x, nodes_y, elements_all_tris)

            # plot the finite element mesh
            plot_fem_mesh(nodes_x, nodes_y, elements)

            # plot the contours
            plt.tricontourf(triangulation, nodal_values, levels=11, cmap="jet", alpha=0.70)

            # show
            plt.colorbar(extendrect='True',extendfrac='auto',spacing='proportional')
            # plt.axis('equal')
            plt.axis('scaled')
            plt.title("U2")
            plt.xlabel("m")
            plt.ylabel("m")
            plt.savefig("Q4_250.png", dpi=300)
            plt.show()










    # def displacement(self, data):
    #     U = self.linalg(data)
    #     print(U)
    #     # U1 = self.linalg(data)[:, 0]
    #     # print(U1)
    #     # x, y = self.node[:, 1], self.node[:, 2]
    #     # print(x, y)
    #     # x_new, y_new = self.node[:, 1] + U[:, 0] * 100, self.node[:, 2] + U[:, 1] * 100
    #
    #     # x = np.array(x_plot)
    #     # y = np.array(y_plot)
    #     # a = np.array(a_plot)
    #     fig = plt.figure()
    #     ax = plt.gca()
    #     # x = self.node[:, 1] + U[:, 0] * 0
    #     # y = self.node[:, 2] + U[:, 1] * 0
    #     # a = self.linalg(data)[:, 1] * 0.0000001
    #     x = self.node[:, 1] + U[:, 0] * 1
    #     y = self.node[:, 2] + U[:, 1] * 1
    #     a = self.linalg(data)[:, 0] * 1
    #
    #     triang = mtri.Triangulation(x, y)
    #     refiner = mtri.UniformTriRefiner(triang)
    #     tri_refi, z_test_refi = refiner.refine_field(a, subdiv=4)
    #
    #     levels = np.linspace(z_test_refi.min(), z_test_refi.max(), num=100)
    #     cmap = cm.get_cmap(name='jet')
    #
    #     tric = ax.tricontourf(tri_refi, z_test_refi, levels=levels, cmap=cmap)
    #     ax.scatter(x, y, c=a, cmap=cmap, vmin=z_test_refi.min(), vmax=z_test_refi.max())
    #     fig.colorbar(tric, ax=ax)
    #
    #     ax.set_title('U1 plot')
    #     plt.axis('equal')
    #     plt.show()
    #
    # # fig, (ax, ax2) = plt.subplots(nrows=2, sharey=True, sharex=True, subplot_kw={"aspect": "equal"})
    # #     return x, y, x_new, y_new
    #
    # def plot(self, xcoord, ycoord, connectivity, time):
    #     for connect in connectivity:
    #         x = [xcoord[int(connect[i] - 1)] for i in range(len(connect))]
    #         y = [ycoord[int(connect[i] - 1)] for i in range(len(connect))]
    #         if time == 0:
    #             plt.fill(x, y, edgecolor='black', fill=False)
    #         elif time == 1:
    #             plt.fill(x, y, edgecolor='red', fill=False)





    # # # TODO 작동OK
    # def displacement(self, data):
    #     U = self.linalg(data)
    #     # print(U)
    #     x, y = self.node[:, 1], self.node[:, 2]
    #     x_new, y_new = self.node[:, 1] + U[:, 0] * 100, self.node[:, 2] + U[:, 1] * 100
    #
    #     self.plot(x, y, self.element[:, 1:5], 0)
    #     # self.plot(x+0.1, y+0.1, self.element[:, 1:5], 1)
    #     self.plot(x_new, y_new, self.element[:, 1:5], 1)
    #     plt.axis('equal')
    #     plt.show()
    #
    #     return x, y, x_new, y_new
    #
    # def plot(self, xcoord, ycoord, connectivity, time):
    #     for connect in connectivity:
    #         x = [xcoord[int(connect[i] - 1)] for i in range(len(connect))]
    #         y = [ycoord[int(connect[i] - 1)] for i in range(len(connect))]
    #         if time == 0:
    #             plt.fill(x, y, edgecolor='black', fill=False)
    #         elif time == 1:
    #             plt.fill(x, y, edgecolor='red', fill=False)




# class staticimplicit(SOLVE):
#     pass
#
# class dynamicexplicit(SOLVE):
#     pass



        # fig = plt.figure()
        # ax = plt.axes(xlim=(0, 2.2), ylim=(-0.2, 0.2))
        # line, = ax.plot([], [], lw=2)
        #
        # def init():
        #     line.set_data([], [])
        #     return line,
        #
        # def animate(i):
        #     x = np.linspace(0, 2, 1000)
        #     y = np.sin(2 * np.pi * (x - 0.01 * i))
        #     line.set_data(x, y)
        #     return line,
        #
        # anim = animation.FuncAnimation(fig, animate, init_func=init, frames=200, interval=20, blit=True)
        #
        # anim.save('exAnimation.gif', writer='Pillow', fps=30, dpi=100)
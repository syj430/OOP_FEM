import numpy as np
import re
from SET import SET
from SECTION import SECTION
from MATERIAL import MATERIAL

'''
파트 클래스 - name, node, element, Nset, Elset data for each part
'''


class PARTS:
    # 생성자

    def __init__(self, name, node, element, eltype, Nset, Elset, section):  # , section):
        self.name = name
        self.node = node
        self.element = element
        self.eltype = eltype
        self.Nset = Nset
        self.Elset = Elset
        self.section = section

        # print('**')
        # print('*Part, name=', self.name)
        # print('*Node')

    def part_info(self):
        # 파트별 name, node, element, Nset, Elset 데이터
        print(" ")
        print("<Part> ")
        print("----------------------------------------------------------------------------")
        print("name         =", self.name)
        print("node         =", self.node)
        print("element      =", self.element)
        print("element type =", self.eltype)
        print("Nset         =", self.Nset)
        print("Elset        =", self.Elset)
        print("section      =", self.section)
        print("----------------------------------------------------------------------------")

    def mnode(self):
        # TODO : node 데이터 처리 (pandas, numpy)
        # 리스트타입 -> 숫자형타입 데이터클리닝
        if not self.node == []:
            node_data = self.node
            del node_data[0]
            print(len(node_data))
            d = []
            for i in range(0, len(node_data)):
                s = [float(s) for s in re.findall(r"[-+]?\d*\.\d+|\d+", node_data[i])]
                d.append(s)
            d = np.array(d)

            nodenum = d[:, 0]  # Node number
            x = d[:, 1]  # First coordinate of the node
            y = d[:, 2]  # Second coordinate of the node

        else:
            d = []
            print(d)
            nodenum = []
            x = []
            y = []

        # return node0
        return nodenum, x, y

        #     np.array([[0,0], [0,0.5],[0,1],[0.5,0], [0.5,0.5], [0.5,1], [1,0],
        #           [1,0.5],[1,1]])

    # def melement(self):
    # TODO : element 데이터 처리
    # 리스트타입 -> 숫자형타입
    # return
    #
    def mNset(self):
        # TODO : element 데이터 처리
        # 리스트타입 -> 숫자형타입
        Nset = self.Nset

        # print(Nset)

        # sep1 = Nset[0].split(',')
        sep1 = Nset[1].split(',')
        # print(sep1)
        #
        return sep1
        # return Nset

    # def mElset(self):
    # TODO : element 데이터 처리
    # 리스트타입 -> 숫자형타입
    # return

    def msection(self):
        # TODO : element 데이터 처리
        # 리스트타입 -> 숫자형타입
        section = self.section
        sep1 = section[0].split(',')  # ','기준으로 리스트 분리
        sect_name = sep1[0]  # Section name

        sep2 = sep1[1].split('=')[1]
        sep3 = sep1[2].split('=')[1]

        return sect_name, sep2, sep3

    # ...

#
# # Sub class
# class WORKPIECE(PARTS):
#
#
#     print('*Node')
#     # data line
#
#     print('*Element'+'\n')
#     # data line
#
#     Set = SET('test')
#     Set.Nset()
#     Set.Elset()
#
#     # Section data line
#
#
#     def Section(self):
#         print('*Section')
#         Section = SECTION('PICKEDSET2')
#
#         Section.SOLID()
#
#         print('재료 이름은 : ', self.name)


# class TOOLS(PARTS):
#     # Sub class
#     print('Tools')
#
#
#     def node(self):
#         print('재료 이름은 : ', self.name)


# class PART:
#     # Super class
#     name = '이름'
#
#     def show(self):
#         print('파트 클래스의 메소드입니다.')
#
# class WORKPIECE(PART):
#     # Sub class
#     #     print('Workpiece')
#
#     def __init__(self, name):
#         self.name = name
#
#     def show_name(self):
#         print('재료 이름은 : ', self.name)
#
# class TOOLS(PART):
#     # Sub class
#     #     print('Tools')
#
#     def __init__(self, name):
#         self.name = name
#
#     def show_name(self):
#         print('재료 이름은 : ', self.name)
#
#
#
# a = WORKPIECE('material-1')
# a.show()
# a.show_name()

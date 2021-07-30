import numpy as np
import pandas as pd
import re
from PART import PARTS
from MATERIAL import MATERIAL
from INTERPROP import INTERPROP
from INTERACTION import INTERACTION
from BC import BC
from matplotlib import pyplot as plt


# main code
# if __name__ == "__main__":

'''
Extract data from an ABAQUS INP file.

'''

# Read inp file
file = open('job.inp', 'r')
line = file.read()
# print(line) # line = file.readline()
# print(line) # line = line.lower() # print(lower)


# Split string data into a list of strings
split = line.split("*")                         # Split data by '*'
list = list(map(lambda x: x.strip(), split))

for item in list:
    if not item:
        list.remove('')

# Initialize an array of each class instance
for i in range(10):     # FIXME : 10? or..
    globals()['part{}'.format(i)] = PARTS("", [], [], [], [], [], [])       # Parts
    globals()['BC{}'.format(i)] = BC("", "", [])                            # Boundary condition
    globals()['MAT{}'.format(i)] = MATERIAL("", [], [])                     # Material
    globals()['IP{}'.format(i)] = INTERPROP([], [], [])                     # Interaction properties

z = 1; z2 = z; z3 = z   # FIXME : 다른 구문 있다면..

# Read the file line by line
for i in range(0, len(list)):
    x = list[i]
    x = x.split("\n")        # show list
    print(x)
    # print(x[0])


    sep1 = x[0].split(',')   #TODO    ','기준으로 리스트 분리
    sep2 = x[0].split(' ')   #TODO    ' '기준으로 리스트 분리 (BOUNDARY CONDITION)
    # print('sep1 =', sep1)
    keyword = sep1[0]        # extract the keyword from the string with ','
    # print(keyword)


# Keywords              # FIXME      if문 or 딕셔너리 이용 switch-case문
    if keyword == 'Heading':
        # TODO      *Heading
        print('Heading...TBC!!')

    elif keyword == 'Part':
        partname = sep1[1]
        partname = partname.split('=')[1]   # PARTS 클래스 name
        # print(partname)

    elif keyword == 'Node':
        node = x            # node 데이터
        # print(node)

    elif keyword == 'Element':
        eltype = sep1[1]
        elname = eltype.split('=')[1]   # element 타입
        element = x                     # element 데이터

        # print(elname)
        # print(element)

    elif keyword == 'Nset':
        Nsetname = sep1[1]
        unknown1 = sep1[2]
        Nset = x

        name = Nsetname.split('=')[1]   # PARTS 클래스 name
        # print('Nset_name =', name,', UK1 =', unknown1)
        # print(Nset)

    elif keyword == 'Elset':
        Elsetname = sep1[1]
        unknown1 = sep1[2]
        Elset = x
        # print([l.strip() for l in Elset])

        name = Elsetname.split('=')[1]  # PARTS 클래스 name
        # print('Elset_name =', name,', UK1 =', unknown1)
        # print(Elset)

    elif 'Section' in keyword:
        sectionname = keyword
        section = x
        # print(x)

    elif keyword == 'End Part':
        globals()['part{}'.format(z)] = PARTS(partname,node,element,elname,Nset,Elset,section)

        z+=1

        # Initialize the
        name = []
        node = []
        element = []
        elname = []
        Nset = []
        Elset = []
        section = []

    else:
        pass


# Material loop
    if keyword == 'Material':
        matname = sep1[1]
        matname = matname.split('=')[1]   # MATERIAL 클래스 name
        # print(matname)

    elif keyword == 'Elastic':
        elastic = x
        # partname = partname.split('=')[1]   # PARTS 클래스 name


    elif keyword == 'Plastic':
        plastic = x
        # partname = partname.split('=')[1]   # PARTS 클래스 name

        # mat 클래스
        globals()['MAT{}'.format(z2)] = MATERIAL(matname, elastic, plastic)

    else:
        pass

# INTERACTION PROPERTIES
    if keyword == 'Surface Interaction':
        surf_int = x

    elif keyword == 'Friction':
        friction = x

    elif keyword == 'Surface Behavior':
        surf_beh = x

        globals()['IP{}'.format(z2)] = INTERPROP(surf_int, friction, surf_beh)   # IP 클래스
    else:
        pass

# INTERATIONS
    if 'Interaction:' in keyword:
        interaction = sep2[1]

    elif keyword == 'Contact Pair':
        CP = x


        # INTERACTION(interaction, CP).inter_info()   # 클래스
    else:
        pass


# BOUNDARY CONDTION
    if 'Type:' in keyword:
        BCname = sep2[1]
        BCtype = sep2[3]
        # print(sep2)
        # print(BCname)
        # print(BCtype)

    elif keyword == 'Boundary':
        pickedset = x

        # print(pickedset)
        globals()['BC{}'.format(z3)] = BC(BCname, BCtype, pickedset)

        z3+=1
        # Initialize the
        BCname = []
        BCtype = []
        pickedset = []

    else:
        pass

#TODO : Assembly, HISTORY DATA(STEP)

# Instance test             # FIXME Unresolved reference
# part1.part_info()           # part1 = 인스턴스 (클래스PART의 객체)
# part2.part_info()
# part3.part_info()

# part1.part_info()
########### aaa = part1.mnode()
# print(list(aaa))
# print(aaa)

# print(type(aaa))






# # EX.)

info = part1.part_info()
node = part1.mnode()         # part1의 노드데이터 (숫자형)

section = part1.msection()

print(section[0],section[1],section[2])
# node2 = part2.mnode()         # part1의 노드데이터 (숫자형)
#
# plt.figure()
# plt.plot(node[1], node[2])
# plt.show()
#
# print(node[23])
print(node[0])
print(node[1])
# print(node[2])

sss = part1.mNset()
print(sss)

# print(node1)
# print(node1)
# print(len(node))
# print(len(node1))

#class Gausspt:
#    # dim = 2
#    def mat_info(self):
#
#
#    # dim = 3
#    def mat_info(self):




#
# BC1.BC_info()
# BC2.BC_info()
# BC4.BC_info()
#
# print(MAT1.ELAS())
# MAT1.PLAS()
# print(MAT1.PLAS())


# IP1.IP_info()

print('--------end--------')



    
    # keyword 분류
    # if ',' in x[0]:
    #
    #     sep1 = x[0].split(',')
    #     print(sep1)
    #     keyword = sep1[0]  # extract the keyword from the string with ','
    #     print(keyword)
    #     # # x = x.split(",")
    #     # print('Yes ,', keyword)
    #
    # else:
    #     # print('No', keyword)
    #     # print('No ,',x[0])
    #     a=1


    # if sep1[0] == 'Heading':
    #     print('Heading...TBC!!')
    # elif sep1[0] == 'Part':
    #     name = sep1[1]
    #     # name = x[0].split('=')[1]
    #     # xxx = x
    #     print(name)
    #     # print('NODENODENODENODE')
    #
    #
    # else:
    #     # print('None')
    #     a=1

    #
    # if
    # else:
    #     print('Empty')



#
# # llll = print(list)
# x = list[6]
# # print(x)
# # print(x)
# #
# x = x.split("\n")
# #
# x.remove('Node')  # keyword 삭제
#
# print(x)






# # stringnode = np.array(x, dtype=float)
# # stringnode.remove(stringnode[0])
#
#
# print(x)
# # print(matnode)
# # print(stringnode[1])
# # print(type(stringnode[1]))






# stringnode = stringnode.split("\n")

# float_node = stringnode.astype(float)
# print(stringnode)
# print(type(stringnode))
# print(float_node)

# print(node.shape)



# print(node[1])
# print(type(node))


# print(list)
# print(list[5])
# print(list[6])
# print(list[7])

# print(list)

# split = split.strip('\n')
# print([l.strip() for l in split])

# for i in split[0:30]:
#     print(i)
    # split2 = i.split(",")
    # print(split2)
#
#     keyword = split2[0].split(",")
#     keyword = str(keyword)
#     print(keyword)
#
#
#     if not keyword:
#         # print('empty')
#         pass
#
#     elif keyword == 'Heading\n':
#         print('begins')
#         pass
#
#     elif keyword == 'Part':
#         print(split2)
#
#     else:
#         pass
#         # print('else')



# for i, x in enumerate(split):
#     print(x)


# 210718
    # for i in range(0,len(line)):
    #     # print(lines[i])
    #
    #     skip = '**, *Heading, *Preprint'
    #
    #     if skip in line[i]:
    #         pass
    #
    #     if '*Part, name=' in line[i]:
    #         print('줄번호: ', i+1)
    #         for i, x in enumerate(line[i+1:i+10]):
    #             print(x)
    #
    #     #
    #     else:
    #         a=1





        #
        # print('---------End_of_line-----------'+'\n')
        #
        #
        #
        #
        #
        #
        #
        #
        #
        # if '**' in lines[i]:
        #     pass            # comment
        #
        # elif '*' in lines[i]:
        #
        #     skip = '**, *Heading,*Preprint'
        #
        #     if skip in lines[i]:
        #         pass
        #     if '*Part, name=' in lines[i]:
        #         item = lines[i].split(" ")
        #         print(item)
        #
        #
        #         print(lines[i][4:10])
        # else:
        #     a=1
        #     # print(lines[i])
        #
        #
        #




'''
Load the input data
'''

# PART
'''
Initialize arrays
'''

'''
Apply B.C
'''

'''
Stiffness matrix, load vector
'''

'''
Solve the governing equations
'''

'''
Outputs
'''



# import numpy as np

from MATERIAL import MATERIAL

# class material:
#     def youngs(self):
#         print('youngs modulus')
# def test(*args):
#     for i in args:
#         print(i, end=',')
    # print()

# main code
# if __name__ == "__main__":



# a = MATERIAL()
# a.ELAS()

# test(1, 0.0, 0.0, 2, 0.0, 0.0)  # 튜플


# with open('job.inp') as file:
#     for line in file:
#         # print(line)
#         line = line.rstrip('\n')
#         # print(line)
#
#         split2 = line.split("**")
#         print(split2)
#
#         # split2 = split2.split(",")
#         # print(split2)


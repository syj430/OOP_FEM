from keywords import *
import numpy as np
import re

class INPUT:
    def __init__(self):
        # KEY : VALUE (Method)
        self.dict_func = {
            'Part'              : self.part,
            'Node'              : self.node,
            'Element'           : self.element,
            'Nset'              : self.nset,
            'Elset'             : self.elset,
            'Solid Section'     : self.Solid_Section,
            'Assembly'          : self.assembly,
            'Material'          : self.material,
            'Elastic'           : self.elastic,
            'Plastic'           : self.plastic,
            'Boundary'          : self.boundary,
            'Step'              : self.step,
            'Static'            : self.static,
            'Cload'             : self.cload,
            'Output, field'     : self.foutput,
            'Output, history'   : self.houtput
        }

        # List
        self._node = []
        self._element = []
        self._nset = []
        self._elset = []
        self._Solid_Section = []
        self._assembly = []
        self._material = []
        self._elastic = []
        self._plastic = []
        self._boundary = []
        self._step = []
        self._static = []
        self._cload = []
        self._foutput = []
        self._houtput = []

        # Dictionary
        self.DATA = {}

    def read_file(self, file_name):
        with open(file_name, 'r') as file:
            content = file.readlines()
            for line in content:
                line = line.rstrip('\n')

                if "*" in line:
                    key = self.KeyfromLine(line)

                if key in KEYWORDS:
                    ans = self.dict_func[str(key)](line)
                    self.DATA[str(key)] = ans
        print(self.DATA)
        return self.DATA


    def part(self, line):
        self._name = self.getName(line)
        return self._name

    def node(self, line):
        self._node.append(line)
        return self._node

    def element(self, line):
        self._element.append(line)
        return self._element

    def nset(self, line):
        self._nset.append(line)
        return self._nset

    def elset(self, line):
        self._elset.append(line)
        return self._elset

    def Solid_Section(self, line):
        self._Solid_Section.append(line)
        return self._Solid_Section

    def assembly(self, line):
        self._assembly.append(line)
        return self._assembly

    def material(self, line):
        self._material.append(line)
        return self._material

    def elastic(self, line):
        self._elastic.append(line)
        return self._elastic

    def plastic(self, line):
        self._plastic.append(line)
        return self._plastic

    def boundary(self, line):
        self._boundary.append(line)
        return self._boundary

    def step(self, line):
        self._step.append(line)
        return self._step

    def static(self, line):
        self._static.append(line)
        return self._static

    def cload(self, line):
        self._cload.append(line)
        return self._cload

    def foutput (self, line):
        self._foutput .append(line)
        return self._foutput

    def houtput (self, line):
        self._houtput .append(line)
        return self._houtput

    def getName(self, line):
        name = line.split('=')[1]
        return name

    def KeyfromLine(self, line):
        line = line.strip()
        key = line.split(",")[0]
        key = key.replace("*", "")
        return key



class PRE(INPUT):
    def __init__(self):
        INPUT.__init__(self)

        self.rrr={}
        self.nset_dict = {}
        self.essbc = {}
        self.cload = {}

    def categorize(self, data):
        # print(data)
        KeyUsed = list(data.keys())
        # print(KeyUsed)
        for key in KeyUsed:
            value = data[str(key)]

            ans = self.dict_func[str(key)](value)
            # print(key)
            # print(value)
            # print(ans)
            self.rrr[str(key)] = ans

        return self.rrr


    def part(self, value):
        # print(value)
        # value = value['Part']
        return value

    def node(self, value):
        del value[0]
        d = []
        for i in range(0, len(value)):
            s = [float(s) for s in re.findall(r"[-+]?\d*\.\d+|\d+", value[i])]
            d.append(s)
        d = np.array(d)
        return d


    def element(self, value):
        elemdict = {}
        firstline = value[0]
        elem_type = self.getName(firstline)

        del value[0]
        d = []
        for i in range(0, len(value)):
            s = [float(s) for s in re.findall(r"[-+]?\d*\.\d+|\d+", value[i])]
            d.append(s)
        d = np.array(d)
        elemdict['elem_type'] = elem_type
        elemdict['element'] = d
        # print(d)
        return elemdict


    def nset(self, value):
        # self.nset_list = []
        nsetname = None
        for line in value:
            if 'instance' in line:
                nsetname = line.split(',')[1].split('=')[1]
                # print(nsetname)
                self.nset_list = []


            if nsetname:
                if not 'instance' in line:
                    line = line.strip()
                    line = line.strip(',')
                    line = line.split(',')
                    # print(line)
                    for item in line:
                        item = int(item)
                        self.nset_list.append(item)
                        # print(self.nset_list)
                    self.nset_dict[str(nsetname)] = self.nset_list
        # print(self.nset_dict)
        return self.nset_dict

    # nodes = np.linspace(n[0], n[1], int(1 + (n[1] - n[0]) / n[2]))

    def elset(self, value):
        pass
        # for line in value:
        #     print(line)

    def Solid_Section(self, value):
        del value[0]
        for line in value:
            if ','==line:
                thickness = None

            else:
                thickness = float(line.strip(','))
            # line = line.replace(',','')
            # line = line.split(',')
        return thickness # can be thickness or none

    def assembly(self, value):
        pass

    def material(self, value):
        name = self.getName(value[0])
        return name

    def elastic(self, value):
        del value[0]
        for line in value:
            elas = line.split(",")
            E = float(elas[0])
            nu = float(elas[1])
        elasdata = {'E':E,'nu':nu}
        return elasdata

    def plastic(self, value):
        del value[0]
        for line in value:
            elas = line.split(",")
            E = float(elas[0])
            nu = float(elas[1])
        elasdata = {'E': E, 'nu': nu}
        return elasdata

    def boundary(self, value):
        del value[0]
        value = value[0]
        name, type = value.split(", ")
        self.essbc[type] = name
        # print(self.essbc)
        return self.essbc

    def step(self, value):
        a = 1
        # print(value)

    def static(self, value):
        pass

    def cload(self, value):
        del value[0]
        value = value[0]
        name, direction, load = value.split(",")
        self.cload[name] = [int(direction), float(load)]
        # print(self.cload)
        return self.cload

    def getName(self, line):
        name = line.split('=')[1]
        return name


    # def foutput (self, value):
    #     a = 1
    #     # print(value)
    #
    # def houtput (self, value):
    #     a = 1
    #     # print(value)



if __name__ == '__main__':
    preprocessor = PRE()
    a = preprocessor.read_file("Q4.inp")
    print(a)

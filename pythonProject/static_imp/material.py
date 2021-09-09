class MATERIAL:
    def __init__(self, data):
        self.data = data

    def getMaterialData(self):
        return self.data['Material']


class ELASTIC(MATERIAL):
    def __init__(self, data):
        MATERIAL.__init__(self, data)
        self.E  = self.data['Elastic']['E']
        self.nu = self.data['Elastic']['nu']
        # print('sss')

    def getElastic(self):
        return self.E, self.nu


class ELASTOPLASTIC(MATERIAL):
    pass











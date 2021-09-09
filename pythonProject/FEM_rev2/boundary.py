class BOUNDARY:
    def __init__(self, data):
        self.data = data

    def getBoundaryData(self):
        self.boundary = self.data['Boundary']
        return self.boundary

    def getNsetData(self):
        self.nset = self.data['Nset']
        print(self.nset)
        return self.nset
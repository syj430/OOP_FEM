class CLOAD:
    def __init__(self, data):
        self.data = data

    def getCloadData(self):
        self.cload = self.data['Cload']

        print('CCC', self.cload)
        return self.cload


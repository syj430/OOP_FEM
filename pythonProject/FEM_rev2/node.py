class NODE:
    def __init__(self, data):
        self.data = data

    def getNodeData(self):
        self.node = self.data['Node']
        return self.node




# class NODE:
#     def __init__(self):
#         self.__node = None
#
#     @property           # get method
#     def getNode(self):
#         return self.__node
#
#     @getNode.setter        # set method
#     def getNode(self, array):
#         self.__node = array
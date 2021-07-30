class BC:
    def __init__(self, BCname, BCtype, pickedset):

        self.BCname = BCname
        self.BCtype = BCtype
        self.pickedset = pickedset


    def BC_info(self):
        print(" ")
        print("<BOUNDARY CONDITION> ")
        print("----------------------------------------------------------------------------")
        print("name        =", self.BCname)
        print("type        =", self.BCtype)
        print("pickedset   =", self.pickedset)
        print("----------------------------------------------------------------------------")


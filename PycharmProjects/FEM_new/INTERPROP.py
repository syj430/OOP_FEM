class INTERPROP:
    def __init__(self, surf_int, friction, surf_beh):

        self.surf_int = surf_int
        self.friction = friction
        self.surf_beh = surf_beh


    def IP_info(self):
        print(" ")
        print("<INTERACTION PROPERTIES> ")
        print("----------------------------------------------------------------------------")
        print("surface interaction =", self.surf_int)
        print("friction            =", self.friction)
        print("surface behavior    =", self.surf_beh)
        print("----------------------------------------------------------------------------")


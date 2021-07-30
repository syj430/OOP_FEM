class INTERACTION:
    def __init__(self, interaction, CP):

        self.interaction = interaction
        self.CP = CP

    def inter_info(self):
        print(" ")
        print("<INTERACTION> ")
        print("----------------------------------------------------------------------------")
        print("interaction  =", self.interaction)
        print("contact pair =", self.CP)
        print("----------------------------------------------------------------------------")

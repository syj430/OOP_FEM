class SECTION:
    # 생성자
    def __init__(self, name):
        self.name = name
    
    def SOLID(self):
        print('*Solid Section, ', self.name)


    def SHELL(self):
        print('*Shell Section, ', self.name)
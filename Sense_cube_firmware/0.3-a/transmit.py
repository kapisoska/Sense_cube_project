class globl:
    def __init__(self):
        self.__msg = ["text", 0]
        self.__charging = bool

    @property
    def msg(self):
        return list(self.__msg)

    @msg.setter
    def msg(self, new):
        self.__msg = new


    @property
    def charging(self):
        return self.__charging
    
    @charging.setter
    def charging(self, new):
        self.__charging = new
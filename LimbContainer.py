class LimbContainer:

    name = ''
    array = []

    def __init__(self, name, array):
        self.name = name
        self.array = array

    def getName(self):
        return self.name

    def getArray(self):
        return self.array

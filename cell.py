class Cell():
    def __init__(self, value = 0):
        self.value = value
        self.possibles = [1,2,3,4,5,6,7,8,9]
        self.lock = False
        if self.value != 0:
            self.possibles = []
            self.lock = True
    
    def __str__(self):
        return str(self.value)
import builtins
z1 = 0
class MapManager():
    def __init__(self) -> None:
        self.model = 'block.egg'
        self.texture = "block.png"
        self.color = (0.2, 0.2, 0.35, 1)
        self.startNew()
        self.addBlock((0, 10, 0))
    def startNew(self):
        self.land = builtins.render.attachNewNode("Land")
    def addBlock(self, position: tuple[int, int, int]):
        self.block = builtins.loader.loadModel(self.model)
        texture = builtins.loader.loadTexture(self.texture)
        self.block.setTexture(texture)
        self.block.setPos(position)
        self.block.reparentTo(self.land)
    def clear(self):
        self.land.removeNode()
        self.startNew()
    def loadland(self, filename):
        self.clear()
        a = 0
        b = 0
        c = 0
        with open(filename, 'r') as file:
            y = 0
            for line in file:
                x = 0
                line = line.split(" ")
                for z in line:
                    for z0 in range(int(z)+1):
                        c += z0
                        self.addBlock((x, y, z0))
                        if z == "1":
                            a += z0
                    x += 1
                y += 1
        print("Кількість одиниць: " + str(a))
        print("14 елемент 8 рядка: " + str(b))
        print("" + str(c))
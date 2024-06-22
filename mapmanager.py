import builtins
import pickle
z1 = 0
class MapManager():
    def __init__(self) -> None:
        self.model = 'block.egg'
        self.textures = ["block.png",
                         "stone.png",
                         "wood.png"
        ]
        self.color = (0.2, 0.2, 0.35, 1)
        self.colors = [(0.5, 0.5, 0.6, 1), 
                       (1, 0.4, 0, 1), 
                       (0.2, 0.7, 0.3, 1), 
                       (0.4, 0.1, 0.9, 1)]
        self.startNew()
        self.addBlock((0, 10, 0))
    def startNew(self):
        self.land = builtins.render.attachNewNode("Land")
    def getColor(self, z):
        if z >= len(self.colors) - 1:
            return self.colors[-1]
        return self.colors[z]
    def getTexture(self, z):
        if z >= len(self.textures) - 1:
            return self.textures[-1]
        return self.textures[z]


    def addBlock(self, position:  tuple[int,int,int]):
        self.block = builtins.loader.loadModel(self.model)
        texture = builtins.loader.loadTexture(self.getTexture(position[2]))
        #self.block.setTexture(texture)
        self.block.setTexture(texture)
        self.block.setTag("at", str(position))
        new_color = self.getColor(position[2])
        self.block.setColor(new_color)
        self.block.setPos(position)
        self.block.reparentTo(self.land)
    def deleteBlock(self, pos):
        blocks = self.findBlock(pos)
        for b in blocks:
            b.removeNode()
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
    def isEmpty(self, pos):
        blocks = self.findBlock(pos)
        return not bool(blocks)
    def findBlock(self, pos):
        return self.land.findAllMatches("=at="+str(pos))
    def findhighestEmpty(self, pos):
        x,y,z = pos
        z = 1
        while not self.isEmpty((x,y,z)):
            z += 1
        return (x,y,z)
    def saveToBin(self):
        blocks = self.land.getChildren()
        with open("landbin.dat", "wb") as file:
            pickle.dump(len(blocks), file)
            for b in blocks:
                #x, y, z = b.getPos()
                #pos = int(x), int(y), int(z)
                pos = b.getPos()
                pos = tuple(map(int, pos))
                pickle.dump(pos, file)
    def loadBin(self):
        self.clear()
        with open("landbin.dat", "rb") as file:
            lenght = pickle.load(file)
            for _ in range(lenght):
                pos = pickle.load(file)
                self.addBlock(pos)
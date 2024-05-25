import builtins
class Hero:
    def __init__(self, pos:tuple, land):
        self.land = land
        self.hero = builtins.loader.loadModel("jack")
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(builtins.render)
        self.cameraBind()
        self.cameraUnBind()
        self.acceptEvents()
    def cameraBind(self):
        builtins.base.disableMouse()
        builtins.base.camera.reparentTo(self.hero)
        builtins.base.camera.setPos(0, 0, 1.5)
        self.cameraOn = True
    def cameraUnBind(self):
        pos = self.hero.getPos()
        builtins.base.mouseInterfaceNode.setPos(-pos[0], -pos[1], pos[2]-4)
        builtins.base.camera.reparentTo(builtins.render)
        builtins.base.enableMouse()
        self.cameraOn = False
    def changeCamera(self):
        if self.cameraOn:
            self.cameraUnBind()
        else:
            self.cameraBind()
    def turnLeft(self):
        a = self.hero.getH()
        self.hero.setH(a+5)
    def turnRight(self):
        a = self.hero.getH()
        self.hero.setH(a-5)
    def justMove(self, angle):
        ...
    def tryMove(self, angle):
        ...
    def moveTo(self, angle):
        ...
    def acceptEvents(self):
        builtins.base.accept("c", self.changeCamera)
        builtins.base.accept("arrow_left", self.turnLeft)
        builtins.base.accept("arrow_right", self.turnRight)
        builtins.base.accept("arrow_left"+"-repeat", self.turnLeft)
        builtins.base.accept("arrow_right"+"-repeat", self.turnRight)
change_camera_key = "c"
turn_left_key = "arrow_left"
turn_right_key = "arrow_right"

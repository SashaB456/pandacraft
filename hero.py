import builtins
from direct.task.Task import Task
from panda3d.core import WindowProperties
class Hero:
    def __init__(self, pos:tuple, land):
        self.land = land
        self.spectatorMode = True
        self.hero = builtins.loader.loadModel("smiley")
        self.hero.setH(180)
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(builtins.render)
        self.cameraBind()
        self.acceptEvents()
    def cameraBind(self):
        builtins.base.disableMouse()
        builtins.base.camera.reparentTo(self.hero)
        builtins.base.camera.setPos(0, 0, 1.5)
        self.cameraOn = True
        builtins.base.camera.setH(180)
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
        h = self.hero.getH() % 360
        self.hero.setH(h+5)
    def turnRight(self):
        h = self.hero.getH() % 360
        self.hero.setH(h-5)
    def turnUp(self):
        p = self.hero.getP() % 360
        self.hero.setP(p-5)
    def turnDown(self):
        p = self.hero.getP() % 360
        self.hero.setP(p+5)
    def justMove(self, angle):
        new_pos = self.lookAt(angle)
        self.hero.setPos(new_pos)
    def tryMove(self, angle):
        new_pos = self.lookAt(angle)
        if self.land.isEmpty(new_pos):
            new_pos = self.land.findhighestEmpty(new_pos)
            self.hero.setPos(new_pos)
        else:
            new_pos = new_pos[0], new_pos[1], new_pos[2]+1
            if self.land.isEmpty(new_pos):
                self.hero.setPos(new_pos)
    def moveTo(self, angle):
        if self.spectatorMode:
            self.justMove(angle)
        else:
            self.tryMove(angle)
    def lookAt(self, angle):
        from_x = round(self.hero.getX())
        from_y = round(self.hero.getY())
        from_z = round(self.hero.getZ())
        dx, dy = self.checkDir(angle)
        return from_x+dx, from_y+dy, from_z
    def checkDir(self, angle):
        if angle >= 0 and angle <= 20:
            return 0, -1
        elif angle <= 65:
            return +1, -1
        elif angle <= 110:
            return +1, 0
        elif angle <= 155:
            return +1, +1
        elif angle <= 200:
            return 0, +1
        elif angle <= 245:
            return -1, +1
        elif angle <= 290:
            return -1, 0
        elif angle <= 335:
            return -1, -1
        else:
            return 0, -1
    def forward(self):
        h = self.hero.getH() % 360
        self.moveTo(h)
    def back(self):
        h = (self.hero.getH() + 180) % 360
        self.moveTo(h)
    def left(self):
        h = (self.hero.getH() + 90) % 360
        self.moveTo(h)
    def right(self):
        h = (self.hero.getH() + 270) % 360
        self.moveTo(h)
    def up(self):
        if self.spectatorMode:
            z = self.hero.getZ()
            self.hero.setZ(z+1)
    def down(self):
        if self.spectatorMode:
            z = self.hero.getZ()
            self.hero.setZ(z-1)
    def changeMode(self):
        self.spectatorMode = not self.spectatorMode
    def build(self):
        pos = self.lookAt(self.hero.getH() % 360)
        self.land.addBlock(pos)
    def destroy(self):
        pos = self.lookAt(self.hero.getH() % 360)
        self.land.deleteBlock(pos)
    def save(self):
        self.land.saveToBin()
    def load(self):
        self.land.loadBin()
    def followMouse(self, task):
        if builtins.base.mouseWatcherNode.hasMouse():
            mouse_pos = builtins.base.mouseWatcherNode.getMouse()
            h = trim(mouse_pos.getX())*-180
            p = trim(mouse_pos.getY(), mn = -0.5, mx = 0.5)*-180
            self.hero.setH(h)
            self.hero.setP(p)
            props = builtins.base.win.getProperties()
            mouse_properties = builtins.base.win.getPointer(0)
            new_properties = WindowProperties()
            new_properties.setCursorHidden(True)
            builtins.base.win.requestProperties(new_properties)
            if mouse_pos.getX() >= 0.99:
                builtins.base.win.movePointer(0, 5, int(mouse_properties.getY()))
            if mouse_pos.getX() <= -0.99:
                builtins.base.win.movePointer(0, props.getXSize()-5, int(mouse_properties.getY()))
        return Task.cont
    def acceptEvents(self):
        builtins.base.accept("c", self.changeCamera)
        builtins.base.accept("arrow_left", self.turnLeft)
        builtins.base.accept("arrow_right", self.turnRight)
        builtins.base.accept("arrow_left"+"-repeat", self.turnLeft)
        builtins.base.accept("arrow_right"+"-repeat", self.turnRight)
        builtins.base.accept("arrow_up", self.turnUp)
        builtins.base.accept("arrow_down", self.turnDown)
        builtins.base.accept("arrow_up"+"-repeat", self.turnUp)
        builtins.base.accept("arrow_down"+"-repeat", self.turnDown)
        builtins.base.accept(move_forward_key, self.forward)
        builtins.base.accept(move_back_key, self.back)
        builtins.base.accept(move_forward_key+"-repeat", self.forward)
        builtins.base.accept(move_back_key+"-repeat", self.back)
        builtins.base.accept(move_left_key, self.left)
        builtins.base.accept(move_right_key, self.right)
        builtins.base.accept(move_left_key+"-repeat", self.left)
        builtins.base.accept(move_right_key+"-repeat", self.right)
        builtins.base.accept(move_up_key, self.up)
        builtins.base.accept(move_down_key, self.down)
        builtins.base.accept(move_up_key+"-repeat", self.up)
        builtins.base.accept(move_down_key+"-repeat", self.down)
        builtins.base.accept(change_mode, self.changeMode)
        builtins.base.accept(build, self.build)
        builtins.base.accept(destroy, self.destroy)
        builtins.base.accept(s, self.save)
        builtins.base.accept(l, self.load)
def trim(i, mn=-1, mx=1):
    if i < mn:
        i = mn
    if i > mx:
        i = mx
    return i





change_camera_key = "c"
turn_left_key = "arrow_left"
turn_right_key = "arrow_right"
turn_up_key = "arrow_up"
turn_down_key = "arrow_down"
move_forward_key = "w"
move_back_key = "s"
move_left_key = "a"
move_right_key = "d"
move_up_key = "shift"
move_down_key = "control"
change_mode = "q"
build = "mouse3"
destroy = "mouse1"
s = "r"
l = "l"
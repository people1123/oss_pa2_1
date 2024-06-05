import pygame

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((448,546),0,32)

font_name = pygame.font.get_default_font()
game_font = pygame.font.SysFont(font_name, 72)
info_font = pygame.font.SysFont(font_name, 24)
menu_font = pygame.font.SysFont(font_name, 36)

pygame.display.set_caption('Frogger')
clock = pygame.time.Clock()

background_filename = './images/background.png'
frog_filename = './images/sprite_sheets_up.png'
arrived_filename = './images/frog_arrived.png'
car1_filename = './images/car1.png'
car2_filename = './images/car2.png'
car3_filename = './images/car3.png'
car4_filename = './images/car4.png'
car5_filename = './images/car5.png'
tree_filename = './images/tree.png'

background = pygame.image.load(background_filename).convert()
sprite_frog = pygame.image.load(frog_filename).convert_alpha()
sprite_arrived = pygame.image.load(arrived_filename).convert_alpha()
sprite_car1 = pygame.image.load(car1_filename).convert_alpha()
sprite_car2 = pygame.image.load(car2_filename).convert_alpha()
sprite_car3 = pygame.image.load(car3_filename).convert_alpha()
sprite_car4 = pygame.image.load(car4_filename).convert_alpha()
sprite_car5 = pygame.image.load(car5_filename).convert_alpha()
sprite_tree = pygame.image.load(tree_filename).convert_alpha()

class Object():
    def __init__(self, position, sprite):
        self.sprite = sprite
        self.position = position

    def draw(self):
        screen.blit(self.sprite, (self.position))

    def rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.sprite.get_width(), self.sprite.get_height())

class Frog(Object):
    def __init__(self, position, sprite_frog):
        self.sprite = sprite_frog
        self.position = position
        self.animation_counter = 0
        self.animation_tick = 1
        self.way = "UP"
        self.can_move = 1
        self.life = 3

    def updateSprite(self, key_pressed):
        if self.way != key_pressed:
            self.way = key_pressed
            if self.way == "up":
                frog_filename = './images/sprite_sheets_up.png'
                self.sprite = pygame.image.load(frog_filename).convert_alpha()
            elif self.way == "down":
                frog_filename = './images/sprite_sheets_down.png'
                self.sprite = pygame.image.load(frog_filename).convert_alpha()
            elif self.way == "left":
                frog_filename = './images/sprite_sheets_left.png'
                self.sprite = pygame.image.load(frog_filename).convert_alpha()
            elif self.way == "right":
                frog_filename = './images/sprite_sheets_right.png'
                self.sprite = pygame.image.load(frog_filename).convert_alpha()


    def moveFrog(self,key_pressed, key_up):
        print(self.animation_counter)
        if self.animation_counter == 0 :
            self.updateSprite(key_pressed)
        self.incAnimationCounter()
        print("key up", key_up)
        if key_up == 1:
            print(self.position[0], self.position[1])
            if key_pressed == "up":
                if self.position[1] > 39:
                    self.position[1] = self.position[1]-13
            elif key_pressed == "down":
                if self.position[1] < 473:
                        self.position[1] = self.position[1]+13
            if key_pressed == "left":
                if self.position[0] > 2:
                    if self.animation_counter == 2 :
                        self.position[0] = self.position[0]-13
                    else:
                        self.position[0] = self.position[0]-14
            elif key_pressed == "right":
                if self.position[0] < 401:
                    if self.animation_counter == 2 :
                        self.position[0] = self.position[0]+13
                    else:
                        self.position[0] = self.position[0]+14

    def cannotMove(self):
        self.can_move = 0

    def animateFrog(self, key_pressed, key_up):
        if self.animation_counter != 0:
            if self.animation_tick <= 0:
                self.moveFrog(key_pressed, key_up)
                print("key: ",key_pressed)
                self.animaiton_tick = 1
            else:
                self.animation_tick = self.animation_tick -1

    def draw(self):
        current_sprite = self.animation_counter * 30
        screen.blit(self.sprite, (self.position), (0+current_sprite, 0, 30, 30 + current_sprite))

    def incAnimationCounter(self):
        self.animation_counter = self.animation_counter +1
        if self.animation_counter == 3:
            self.animation_counter = 0
            self.can_move = 1

    def setInitPosition(self):
        self.position = [207,475]

    def frogDead(self, game):
        self.setInitPosition()
        self.decLife()
        self.animation_counter = 0
        self.animation_tick = 1
        self.way = "UP"
        self.can_move = 1
        game.resetTime()
    
    def rect(self):
        return pygame.Rect(self.position[0],self.position[1],30,30)

    def decLife(self):
        self.life = self.life -1

def crashedFrog(frog, cars, game):
    for i in cars:
        carRec = i.rect()
        frogRec = frog.rect()
        if frogRec.colliderect(carRec):
            print(carRec, frogRec)
            frog.frogDead(game)

def drownedFrog(frog, trees, speed, game):
    safe = 0
    wayTree = ""
    for i in trees:
        treeRec = i.rect()
        frogRec = frog.rect()
        if frogRec.colliderect(treeRec):
            safe = 1
            wayTree = i.way
    
    if safe == 0:
        frog.frogDead(game)
    elif safe == 1:
        if wayTree == "right":
            frog.position[0] = frog.position[0] + speed
        elif wayTree == "left":
            frog.position[0] = frog.position[0] - speed

def frogArrived(frog,arrived_frog, game):
    if frog.position[0] > 33 and frog.position[0] < 53:
        position_init = [43,7]
        createArrived(frog,arrived_frog,position_init,game)

    elif frog.position[0] > 115 and frog.position[0] < 135:
        position_init = [125,7]
        createArrived(frog,arrived_frog,position_init,game)

    elif frog.position[0] > 197 and frog.position[0] < 217:
        position_init = [207,7]
        createArrived(frog,arrived_frog,position_init,game)

    elif frog.position[0] > 279 and frog.position[0] < 299:
        position_init = [289,7]
        createArrived(frog,arrived_frog,position_init,game)

    elif frog.position[0] > 361 and frog.position[0] < 381:
        position_init = [371,7]
        createArrived(frog,arrived_frog,position_init,game)
    



class Car(Object):
    def __init__(self,position,sprite_enemy,way,factor):
        self.sprite = sprite_enemy
        self.position = position
        self.way = way
        self.factor = factor

    def move(self,speed):
        if self.way == "right":
            self.position[0] = self.position[0] + speed * self.factor
        elif self.way == "left":
            self.position[0] = self.position[0] - speed * self.factor


class Tree(Object):
    def __init__(self,position,sprite_tree,way):
        self.sprite = sprite_tree
        self.position = position
        self.way = way

    def move(self,speed):
        if self.way == "right":
            self.position[0] = self.position[0] + speed
        elif self.way == "left":
            self.position[0] = self.position[0] - speed

def createArrived(frog,arrived_frog,position_init, game):
    frog_arrived = Object(position_init,sprite_arrived)
    arrived_frog.append(frog_arrived)
    game.incPoints(10 + game.time)
    game.resetTime()
    frog.position = [207, 475]
    frog.animation_counter = 0
    frog.animation_tick = 1
    frog.can_move = 1

def drawList(list):
    for i in list:
        i.draw()

def createCars(list,cars, speed):
    for i, tick in enumerate(list):
        list[i] = list[i] - 1
        if tick <= 0:
            if i == 0:
                list[0] = (40*speed)
                position_init = [-55,436]
                car = Car(position_init,sprite_car1,"right",1)
                cars.append(car)
            elif i == 1:
                list[1] = (30*speed)
                position_init = [506, 397]
                car = Car(position_init,sprite_car2,"left",2)
                cars.append(car)
            elif i == 2:
                list[2] = (40*speed)
                position_init = [-80, 357]
                car = Car(position_init,sprite_car3,"right",2)
                cars.append(car)
            elif i == 3:
                list[3] = (30*speed)
                position_init = [516, 318]
                car = Car(position_init,sprite_car4,"left",1)
                cars.append(car)
            elif i == 4:
                list[4] = (50*speed)
                position_init = [-56, 280]
                car = Car(position_init,sprite_car5,"right",1)
                cars.append(car)


def createTrees(list,trees,speed):
    for i, tick in enumerate(list):
        list[i] = list[i] - 1
        if tick <= 0:
            if i == 0:
                list[0] = (30*speed)
                position_init = [-100,200]
                tree = Tree(position_init,sprite_tree,"right")
                trees.append(tree)
            elif i == 1:
                list[1] = (30*speed)
                position_init = [448, 161]
                tree = Tree(position_init,sprite_tree,"left")
                trees.append(tree)
            elif i == 2:
                list[2] = (30*speed)
                position_init = [-100, 122]
                tree = Tree(position_init,sprite_tree,"right")
                trees.append(tree)
            elif i == 3:
                list[3] = (30*speed)
                position_init = [448, 83]
                tree = Tree(position_init,sprite_tree,"left")
                trees.append(tree)
            elif i == 4:
                list[4] = (30*speed)
                position_init = [-100, 44]
                tree = Tree(position_init,sprite_tree,"right")
                trees.append(tree)

class Game():
    def __init__(self,level, speed):
        self.level = level
        self.speed = speed
        self.points = 0
        self.time = 30
        
        self.gameInit = 0

    def incLevel(self):
        self.level = self.level + 1

    def incSpeed(self):
        self.speed = self.speed + 1

    def incPoints(self,points):
        self.points = self.points + points

    def decTime(self):
        self.time = self.time -1
    
    def resetTime(self):
        self.time = 30

def levelUp(arrived_frog, cars, trees, frog, game):
    if len(arrived_frog) == 1:
        arrived_frog[:] = []
        frog.position=[207,475]
        game.incLevel()
        game.incSpeed()
        game.incPoints(100)

def moveList(list,speed):
    for i in list:
        i.move(speed)



gameInit = 0

while True:
    screen.blit(background, (0,0))
    frog = Frog([207,475], sprite_frog)
    cars =[]
    trees =[]
    key_up = 1
    key_pressed=0
    arrived_frog = []
    ticks_cars = [30, 0, 30, 0, 60]
    ticks_trees = [0, 0, 30, 30, 30]
    speed = 3
    game = Game(1, 3)
    time = 30

    while frog.life > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    exit()
            if event.type == pygame.KEYUP:
                key_up = 1
            if event.type == pygame.KEYDOWN:
                if key_up == 1 and frog.can_move == 1:
                    key_pressed = pygame.key.name(event.key)
                    frog.moveFrog(key_pressed, key_up)
                    frog.cannotMove()
        if not time:
            time = 30
            game.decTime()
        else:
            time -=1
        
        if game.time == 0:
            frog.frogDead(game)

        if frog.position[1] <40 :
            frogArrived(frog,arrived_frog, game)

        createCars(ticks_cars, cars, game.speed)
        createTrees(ticks_trees, trees, game.speed)
        moveList(cars,game.speed)
        moveList(trees, game.speed)

        if frog.position[1] > 240 :
            crashedFrog(frog, cars,game)
        elif frog.position[1] < 240 and frog.position[1] > 40:
            drownedFrog(frog, trees, game.speed, game)

        levelUp(arrived_frog, cars, trees, frog, game)

        text_info1 = info_font.render(('Level: {0}               Points: {1}'.format(game.level,game.points)),1,(255,255,255))
        text_info2 = info_font.render(('Time: {0}'.format(game.time)),1,(255,255,255))
        text_info3 = info_font.render(('Life: {0}'.format(frog.life)),1,(255,255,255))
        screen.blit(background, (0,0))
        screen.blit(text_info1, (10, 520))
        screen.blit(text_info2, (250, 520))
        screen.blit(text_info3, (350, 520))
        drawList(arrived_frog)
        drawList(cars)
        drawList(trees)
        frog.animateFrog(key_pressed, key_up)
        frog.draw()

        pygame.display.update()
        time_passed = clock.tick(30)

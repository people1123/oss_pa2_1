import pygame

pygame.init()

screen = pygame.display.set_mode((448,546),0,32)

pygame.display.set_caption('Frogger')
clock = pygame.time.Clock()
background_filename = './images/background.png'
frog_filename = './images/sprite_sheets_up.png'

background = pygame.image.load(background_filename).convert()
sprite_frog = pygame.image.load(frog_filename).convert_alpha()
class Object():
    def __init__(self, position, sprite):
        self.sprite = sprite
        self.position = position

    def draw(self):
        screen.blit(self.sprite, (self.position))

    def rect(self):
        return Rect(self.postion[0], self.position[1], self.sprite.get_width(), self.sprite.get_height())

class Frog(Object):
    def __init__(self, position, sprite_frog):
        self.sprite = sprite_frog
        self.position = position
        self.animation_counter = 0
        self.animation_tick = 1
        self.way = "UP"
        self.can_move = 1

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


screen.blit(background, (0,0))
frog = Frog([207,475], sprite_frog)
key_up = 1
key_pressed=0
while True:
    
    
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
        
    screen.blit(background, (0,0))
    frog.animateFrog(key_pressed, key_up)
    frog.draw()

    pygame.display.update()
    time_passed = clock.tick(30)

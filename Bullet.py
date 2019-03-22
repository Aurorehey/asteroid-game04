from Asteroid import *
from game_engine import *
from random import randint

class Bullet (Sprite):
    def __init__(self, position, speed=(0,0)):  #speed (0,0) c'est par défaut si on donne pas de valeur
        image_path= "assets/bullet.png"
        super().__init__(image_path,position)
        self.speed = speed

    def update(self, dt):
        mov_h= dt * self.speed[0]
        mov_v= dt * self.speed[1]
        self.position = (self.position[0]+mov_h, self.position[1]+mov_v)
        super().update(dt)
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

        if (self.position[0]>=800 or self.position[0]<=0):
            self.speed=(self.speed[0]*(-1),self.speed[1])

        if (self.position[1]>=600 or self.position[1]<=0):
            self.speed = (self.speed[0], self.speed[1]*(-1))

        super().update(dt) 

    def on_collision(self, other):
        other.destroy()


resolution = (800,600)
init(resolution, "Asteroid by Sheraaa")

game = Game()


layer= Layer()

#créer un nouveau Sprite
#sprite= Sprite("assets/bullet.png",(400,300))
#l'ajouter le sprite au layer
#layer.add(sprite)

for i in range(10):
    sprite=Bullet((randint(0,800),randint(0,600)), speed= (randint(-100,100),randint(-100,100)))

#Sprite("assets/bullet.png",(randint(0,800),randint(0,600)),1, (50,0))
    layer.add(sprite)



game.add(layer)


game.run()
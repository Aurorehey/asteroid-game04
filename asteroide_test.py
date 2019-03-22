from game_engine import init, Game,Sprite,Layer,Text
from random import randint
from math import cos,sin,radians,sqrt
from pyglet.window.key import symbol_string
import pyglet

class AsteroidGame(Game):
    def __init__(self):
        super().__init__()
        self.started = False        
        
    def add(self,layer):
        super().add(layer)
        layer.game = self
        
    def update(self,dt):
        if self.started:
            super().update(dt)
class Title(Layer):
    def __init__(self):
        super().__init__()
        self.text=Sprite("assets/debut.png")
        self.add(self.text)
        
        
    def on_key_press(self,key,modifiers):
        super().on_key_press(key,modifiers)
        self.game.started=True
        self.text.destroy() 
        
class GameLayer(Layer):
    def __init__(self):
        super().__init__()
        self.game = None
        
        self.score_points = 0
        self.score = Text("",(100,100),font_size=24,italic=True,color=(255,0,0,128))
        self.add(self.score)
        
    def update(self,dt):
        super().update(dt)
        self.score.element.text = "Score:"+ str(self.score_points)
        
    def change_score(self,amount):
        self.score_points= max(0,self.score_points + amount)
        
class GUI(Layer):

    def __init__(self,spaceship):
        super().__init__()
        self.spaceship = spaceship
        self.lives=[]
        position_initial= 795,595
        
        for n in range(spaceship.lives):
            image_path=r'assets/coeur.png'
            position = position_initial[0]-n*(32+5),position_initial[1]
            life=Sprite(image_path,position,anchor=(32,32))
            self.lives.append(life)
            self.add(life)
    def update(self,dt):
        super().update(dt)
        
        if len(self.lives)> self.spaceship.lives:
            life = self.lives.pop()
            life.destroy()
        
class SpaceObject(Sprite):
    def __init__(self,image_path,position,speed=(0,0),anchor=(0,0),rotation_speed=0):
        super().__init__(image_path,position,anchor=anchor)
        self.speed = speed
        self.rotation_speed = rotation_speed

    def update(self, dt): 
        mouvement_h= dt * self.speed[0]
        mouvement_v= dt * self.speed[1] 
        self.position = (self.position[0]+ mouvement_h, self.position[1]+mouvement_v)
        
        if self.position[0]<0:
            self.position=(800,self.position[1])
            
        elif self.position[0]>800:
            self.position=(0,self.position[1])
        
        if self.position[1]<0:
            self.position=(self.position[0], 600)
            
        elif self.position[1]>600:
            self.position=(self.position[0], 0) 
            
        self.rotation += self.rotation_speed * dt
            
        super().update(dt)
        
        
class Bullet(SpaceObject):
    def __init__(self, position,speed=(0,0)):
        image_path ="assets/salade.png"
        self.lifetime = 3
        super().__init__(image_path,position,speed,anchor=(32,22))
        self.speed = speed
    def update(self,dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.destroy()
        super().update(dt)   
    def on_collision(self,other):
        if isinstance(other,Asteroid):
            other.destroy() 
            self.destroy()
            
            
        
        
class Asteroid(SpaceObject):
    def __init__(self,position,speed=(0,0),category=3):
        if category == 3:
            image_path="assets/renard 128.png"
            anchor= (64,90)
        elif category == 2:
            image_path="assets/renard  64.png"
            anchor=(32,45)
        else:
            image_path="assets/renard 32.png"
            anchor=(16,22)
            
       
        super().__init__(image_path,position,speed,anchor=anchor,rotation_speed=randint(-50,50))
        self.speed = speed
        self.category = category
        self.explosion_sound= pyglet.media.load('assets/Explosion41.wav', streaming=False)
        
    def on_collision(self,other):
        if isinstance(other,Vaisseau):
            other.destroy()
            
            
    def destroy(self):
        super().destroy()
        self.layer.change_score(200*self.category)
        self.explosion_sound.play()
        
        
        if self.category> 1:
            for n in range(3):
                speed=(randint(-100,100),randint(-100,100))
                new_asteroid = Asteroid(self.position,speed,category = self.category-1) 
                self.layer.add(new_asteroid)
                
        
class Vaisseau(SpaceObject):
    def __init__(self, position,speed=(0,0)):
        image_path ="assets/tortue.png"
        self.velocity = 0
        self.engine_on = False
        self.lives = 3
        self.max_invincibility_time = 3
        self.invincible = 0
        self.speed = speed
        self.shoot_sound = pyglet.media.load("assets/Laser_Shoot.wav", streaming=False)
        self.hit_sound= pyglet.media.load("assets/evite.wav",streaming=False)
        super().__init__(image_path,position,speed,anchor=(64,90))
        
        
    def on_key_press(self, key, modifiers):
        if symbol_string(key)=='UP':
            self.engine_on = True
        elif symbol_string(key)=='LEFT':
            self.rotation_speed= -180
        elif symbol_string(key)=='RIGHT':
            self.rotation_speed= 180
        elif symbol_string(key)=='SPACE':
            self.shoot()
            
    def on_key_release(self, key, modifiers):
        if symbol_string(key)=='UP':
            self.engine_on = False
        elif symbol_string(key)=='LEFT':
            self.rotation_speed=0
        elif symbol_string(key)=='RIGHT':
            self.rotation_speed=0
            
    def update(self,dt):
        if self.invincible>0:
            self.invincible -= dt
            self.opacity = 50
        else :
            self.opacity = 255
    
        angle = -radians(self.rotation-90)
        dspeed_h = 0
        dspeed_v = 0
        
        
        if self.engine_on:
        
        
            dspeed_h = cos(angle)* dt * 100
            dspeed_v = sin(angle)* dt * 100
            
            #dif_vel = 100 * dt 
            #self.velocity += dif_vel
            
        #else: 
            #dif_vel = -300 * dt 
            #self.velocity=max(self.velocity+dif_vel,0)
    
        
        self.speed=(self.speed[0]+dspeed_h,self.speed[1]+dspeed_v)
        
        lenght = sqrt(self.speed[0]**2 + self.speed[1]** 2)
        
        if lenght> 100: 
            self.speed=(self.speed[0]/lenght*100,self.speed[1]/lenght*100)
            
        
        #self.speed=(cos(angle)* self.velocity,sin(angle)* self.velocity)
        
    
        super().update(dt)
        
    def shoot(self):
        angle = -radians(self.rotation-90)
        self.layer.change_score(-50)
        
        self.shoot_sound.play()
        bullet=Bullet(position=self.position,
                      speed=(cos(angle)* 200,sin(angle)*200 ))
        
        self.layer.add(bullet)
        
    def destroy(self): 
        if self.invincible <=0:
            self.hit_sound.play()
            self.lives-=1
            self.layer.change_score(-200)
      
            if self.lives >0: 
                for n in range(10):
                    speed=randint(-100,100),randint(-100,100)
                    bullet= Bullet(self.position,speed)
                    self.layer.add(bullet)
                self.invincible = self.max_invincibility_time 
                
            else: 
                super().destroy()
                
                
                gameover = Layer()
                bg=Sprite("assets/game over 1.png")
                gameover.add(bg)
                self.layer.game.add(gameover)

resolution = (800,600)
init(resolution, "asteroid by Aurore") 


game = AsteroidGame()
background_layer=Layer()
game_layer = GameLayer() 

position=randint(0,800),randint(0,600)
speed=randint(-100,100),randint(-100,100)
asteroid= Asteroid(position,speed,category=3)
game_layer.add(asteroid)

#for i in range(100):
    
    #sprite = Bullet((randint(0,800),randint(0,600)),speed=(randint(-100,100),randint(-100,100)))
    #layer.add(sprite)
    
    
    
vaisseau=Vaisseau((400,300))
game_layer.add(vaisseau)

score = Text("",(100,100),font_size=24,italic=True,color=(255,0,0,128))
game_layer.add(score)
 
gui=GUI(vaisseau)
title = Title()


background= Sprite("assets/328933-svetik.jpg")
background_layer.add(background)


game.add(background_layer)                     
game.add(game_layer)
game.add(gui)
game.add(title)
#game.debug = True

music = pyglet.media.load("assets/BeepBox-Song2.wav",streaming=False)
music_player=pyglet.media.Player()
music_player.queue(music)
music_player.eos_action= pyglet.media.SourceGroup.loop
music_player.play()
#bgm

game.run() 
from game_engine import Sprite, Layer, Game, Text
from random import randint
from math import sin, cos, radians, sqrt
from pyglet.window.key import symbol_string
from cocos.audio.pygame.mixer import Sound

class AsteroidGame(Game):

    def __init__(self):
        super().__init__()
        self.started = False

    def add(self, layer):
        super().add(layer)
        layer.game = self

    def update(self, dt):
        if self.started:
            super().update(dt)

class Title(Layer):
    def __init__(self):
        super().__init__()
        self.text = Sprite("assets/title.png")
        self.add(self.text)

    def on_key_press(self, key, modifiers):
        super().on_key_press(key, modifiers)
        self.game.started = True
        self.text.destroy()


class GameLayer(Layer):

    def __init__(self):
        super().__init__()
        self.game = None

        self.score_points = 0
        self.score = Text("", (100, 100), size=48, italic=True, color=(255, 0, 0, 128))
        self.add(self.score)

    def update(self, dt):
        super().update(dt)
        self.score.element.text = "Score : " + str(self.score_points)

    def change_score(self, amount):
        self.score_points = max(0, self.score_points + amount)

class GUI(Layer):

    def __init__(self, spaceship):
        super().__init__()
        self.spaceship = spaceship
        self.lives = []
        position_initial = 795, 595

        for n in range(spaceship.lives):
            image_path = 'assets/life.png'
            position = position_initial[0] - n * (16 + 5), position_initial[1]
            life = Sprite(image_path, position, anchor=(16,16))
            self.lives.append(life)
            self.add(life)

    def update(self, dt):
        super().update(dt)

        if len(self.lives) > self.spaceship.lives:
            life = self.lives.pop()
            life.destroy()    


class SpaceObject(Sprite):

    def __init__(self, image_path, position, speed=(0,0),
                 anchor=(0,0), rotation_speed=0):
        super().__init__(image_path, position, anchor=anchor)
        self.speed = speed
        self.rotation_speed = rotation_speed

    def update(self, dt):
        mov_h= dt * self.speed[0]
        mov_v= dt * self.speed[1]
        self.position = (self.position[0]+mov_h, self.position[1]+mov_v)

        if self.position[0] < 0:
            self.position = (800, self.position[1])
        elif self.position[0] > 800:
            self.position = (0, self.position[1])

        if self.position[1] < 0:
            self.position = (self.position[0], 600)
        elif self.position[1] > 600:
            self.position = (self.position[0], 0)

        self.rotation += self.rotation_speed * dt

        super().update(dt) 


class Bullet (SpaceObject):
    def __init__(self, position, speed=(0,0)):
        image_path= "assets/bullet.png"
        self.lifetime = 3
        super().__init__(image_path, position, speed, anchor=(8,8))

    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.destroy()
        super().update(dt)

    def on_collision(self, other):
        if isinstance(other, Asteroid):
            other.destroy()
            self.destroy()

class Asteroid(SpaceObject):
    def __init__(self, position, speed=(0,0), category=3):
        
        if category  == 3:
            image_path = "assets/asteroid128.png"
            anchor = (64, 64)
        elif category == 2:
            image_path = "assets/asteroid64.png"
            anchor = (32, 32)
        else:
            image_path = "assets/asteroid32.png"
            anchor = (16, 16)

        super().__init__(image_path, position, speed, anchor=anchor,
            rotation_speed=randint(-50,50))
        self.category = category
        self.explosion_sound = Sound("assets/explosion.wav")

    def on_collision(self, other):
        if isinstance(other, Spaceship):
            other.destroy()

    def destroy(self):
        super().destroy()

        self.layer.change_score(200 * self.category)

        self.explosion_sound.play()

        if self.category > 1:
            for n in range(3):
                speed = (randint(-100,100) , randint(-100,100))
                new_asteroid = Asteroid(self.position, speed, category = self.category-1)
                self.layer.add(new_asteroid)

class Spaceship(SpaceObject):

    def __init__(self, position):
        image_path= "assets/source.gif"
        self.velocity = 0
        self.engine_on = False
        self.lives = 3
        self.max_invincibility_time = 3
        self.invincible = 0
        self.shoot_sound = Sound("assets/shoot.wav")
        self.hit_sound = Sound("assets/hit.wav")

        super().__init__(image_path, position, anchor=(32,64))

    def on_key_press(self, key, modifiers):
        if symbol_string(key) == 'UP':
            self.engine_on = True
        elif symbol_string(key) == 'LEFT':
            self.rotation_speed = -180
        elif symbol_string(key) == 'RIGHT':
            self.rotation_speed = 180
        elif symbol_string(key) == 'SPACE':
            self.shoot()

    def on_key_release(self, key, modifiers):
        if symbol_string(key) == 'UP':
            self.engine_on = False
        elif symbol_string(key) == 'LEFT':
            self.rotation_speed = 0
        elif symbol_string(key) == 'RIGHT':
            self.rotation_speed = 0

    def update(self, dt):

        if self.invincible > 0:
            self.invincible -= dt
            self.opacity = 50
        else:
            self.opacity = 255

        angle = -radians(self.rotation - 90)
        
        dspeed_h = 0
        dspeed_v = 0

        if self.engine_on:
            dspeed_h = cos(angle) * dt * 1000
            dspeed_v = sin(angle) * dt * 1000

        self.speed = (self.speed[0] + dspeed_h, self.speed[1] + dspeed_v)
        
        length = sqrt(self.speed[0] ** 2 + self.speed[1] ** 2 )

        if length > 1000:
            self.speed = (self.speed[0] / length * 1000, self.speed[1] / length * 1000)

        #self.speed = ( cos(angle) * self.velocity , sin(angle) * self.velocity )

        super().update(dt)

    def shoot(self):
        angle = -radians(self.rotation - 90)

        self.layer.change_score(-50)

        self.shoot_sound.play()

        bullet = Bullet(position=self.position,
                        speed=(cos(angle) * 200, sin(angle) * 200))
        self.layer.add(bullet)

    def destroy(self):
        if self.invincible <= 0:
            self.hit_sound.play()
            self.lives -= 1
            
            self.layer.change_score(-200)

            if self.lives > 0:
                for n in range(10):
                    speed = randint(-100, 100), randint(-100, 100)
                    bullet = Bullet(self.position, speed)
                    self.layer.add(bullet)

                self.invincible = self.max_invincibility_time
            else:
                super().destroy()

                gameover =  Layer()
                bg = Sprite("assets/game over 1.png")
                gameover.add(bg)
                self.layer.game.add(gameover) 

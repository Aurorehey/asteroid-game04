from game_engine import init, Layer, Sprite, Text
from asteroid import (
    Bullet, Spaceship, Asteroid, GUI, AsteroidGame, GameLayer, Title)
from random import randint
from cocos.audio.pygame import mixer
from cocos.audio.pygame.mixer import Sound

resolution = (800,600)
init(resolution, "Asteroid by Game 04")
mixer.init()


game = AsteroidGame()
background_layer = Layer()
game_layer = GameLayer()
title = Title()

position = randint(0,800),randint(0,600)
speed= randint(-100,100), randint(-100,100)

asteroid = Asteroid(position, speed)
spaceship = Spaceship((400,300))
game_layer.add(asteroid)
game_layer.add(spaceship)

gui = GUI(spaceship)

background = Sprite("assets/background.jpg")
background_layer.add(background)

game.add(background_layer)
game.add(game_layer)
game.add(gui)
game.add(title)
# game.debug = True

music = Sound("assets/music.wav")
music.play(-1)

game.run()

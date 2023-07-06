import pygame
import random
from laser import Laser
from pygame.sprite import Group


class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('asteroide.png')
        self.image = pygame.transform.scale(self.image,(40,40))
        self.rect = self.image.get_rect()

    def movimiento(self):
        """
        el enemigo se va a mover de a 1 pixel
        """
        self.rect.y += 1
    
    def bordes(self):
        """
        en esta funcion se limitan los bordes del rect del enemigo, 
        pero en el caso de que llegue hasta abajo de todo, va a
        aparecer en una posicion random de 0 a 600 en el eje x
        """

        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= 600:
            self.rect.right = 600
        if self.rect.top <= 0:
            self.rect.y = 0
        if self.rect.bottom >= 650:
            self.rect.y = 0
            self.rect.x = random.randint(0,600)
    
    def update(self):
        """
        La función update se encarga de aplicar los límites de los bordes 
        y el movimiento al enemigo en cada iteración del bucle principal del juego.
        """
        self.bordes()
        self.movimiento()        
       
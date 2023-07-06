import pygame
from pygame.sprite import Group

class Laser(pygame.sprite.Sprite):
    def __init__(self,pos,velocidad,alto_pantalla):
        super().__init__()
        self.image = pygame.Surface((4,20))
        self.image = pygame.image.load('laser.png')
        self.image = pygame.transform.scale(self.image,(35,50))
        self.rect = self.image.get_rect(center = pos)
        self.velocidad = velocidad
        self.altura_borde = alto_pantalla

    def destruir(self):
        """
        Desaparece el laser de la pantalla
        """
        if self.rect.y <= -50 or self.rect.y >= self.altura_borde + 50:
            self.kill()

    def update(self):
        """
        Actualiza la velocidad para el bucle principal
        """
        self.rect.y += self.velocidad


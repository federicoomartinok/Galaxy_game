import pygame, sys
from pygame.locals import *
from personaje import Jugador 
from laser import Laser
from asteroide import Enemigo
import colores
import random
import sqlite3
from data_base import * 


class Juego:
    def __init__(self):
        sprite_jugador = Jugador((ANCHO / 2,ALTO - 10), 600 ,5)
        self.jugador = pygame.sprite.GroupSingle(sprite_jugador)

        self.vidas = 3
        self.superficie_vidas = pygame.image.load('nave2.png').convert_alpha()
        self.posicion_x_vidas = ANCHO - (self.superficie_vidas.get_size()[0] * 2 + 20)
        self.score = 0
        self.fuente = pygame.font.Font(r'E:\LABORATORIO_1_PYTHON\Laboratorio_1_Pyhton\Laboratorio_1_Pyhton\Ejercicios_Python\Parcial2\fuenteretro.ttf',20)
        self.segaFont = pygame.font.Font(r'E:\LABORATORIO_1_PYTHON\Laboratorio_1_Pyhton\Laboratorio_1_Pyhton\Ejercicios_Python\Parcial2\SEGA.ttf',20)
        self.game_over = False
        self.flag_input = False
        self.texto_usuario = ''

        """self.ruta = 'E:\LABORATORIO_1_PYTHON\Laboratorio_1_Pyhton\Laboratorio_1_Pyhton\Ejercicios_Python\Parcial2'"""
        self.ruta = r'E:\LABORATORIO_1_PYTHON\Laboratorio_1_Pyhton\Laboratorio_1_Pyhton\Ejercicios_Python\Parcial2\tabla.db'

    def display_vidas(self):
        for vida in range(self.vidas - 1):
            #calcula la posición horizontal en la que se dibujarán las vidas del jugador
            x = self.posicion_x_vidas + (vida * (self.superficie_vidas.get_size()[0] + 10))
            pantalla.blit(self.superficie_vidas,(x,8))

    def display_score(self):
        """
        Muestra el score arriba a la izquierda
        """
        superficie_score = self.fuente.render('Score:{0}'.format(self.score),False,colores.RED2)
        rect_score = superficie_score.get_rect(topleft =(10,10))
        pantalla.blit(superficie_score,rect_score)
        
    def start(self):
        """
        Ejecuta el funcionamiento del juego
        """
        self.jugador.update()
        self.jugador.sprite.lasers.draw(pantalla)
        self.jugador.draw(pantalla)
        self.colisiones()
        self.display_vidas()
        self.display_score()

    def colisiones(self):
        """
        Si hay colision con el asteroide se borra el laser y el asteroide.
        Depende de la colision se suma puntos o se baja la vida.
        Actualiza los puntajes.
        """
        
        if self.game_over == False:
            if self.jugador.sprite.lasers:
                for laser in self.jugador.sprite.lasers:
                    if pygame.sprite.spritecollide(laser ,lista_asteroide, True):
                        laser.kill()
                        self.score += 100
        
            if lista_asteroide:
                for asteroide in lista_asteroide:
                    if pygame.sprite.spritecollide(asteroide,juego.jugador,False):
                        asteroide.kill()
                        self.vidas -= 1
                        if self.vidas <= 0:
                            self.game_over = True
                            self.flag_input = True
                            if juego.score > 0:
                                guardar_score(juego.ruta,juego.texto_usuario,juego.score)
                                juego.texto_usuario = ''

if __name__ == '__main__':
    """
    Esto se asegura que el código dentro de él solo se ejecute cuando 
    el archivo se ejecuta directamente como programa principal, 
    y no cuando se importa como un módulo en otro archivo.
    """
    pygame.init()
    pygame.mixer.init()
    ANCHO = 600
    ALTO = 600
    pantalla = pygame.display.set_mode((ANCHO,ALTO))
    pygame.display.set_caption('Galaxia')
    imagen_space = pygame.image.load('fondoespacio.jpg')
    imagen_space = pygame.transform.scale(imagen_space,(ANCHO,ALTO))

    reloj = pygame.time.Clock()
    juego = Juego()

    creacion_tabla_scores(juego.ruta)

    titulo = juego.segaFont.render('~~~GALAXY GAME~~~', True, colores.WHITE)
    titulo_x = (ANCHO // 2) - (titulo.get_width() // 2)
    titulo_y = 20
    titulo_rect = titulo.get_rect(topleft=(titulo_x, titulo_y))
    
    txt = juego.segaFont.render('Click para empezar el JUEGO', True,colores.WHITE)
    txt_ingreso_nombre = juego.fuente.render('Ingrese un nombre:',True,colores.WHITE)
    txt_x = (ANCHO // 2) - (txt.get_width() // 2)
    txt_y = 50

    input_usuario = pygame.Rect((ANCHO/2 - 100),110,200,40)

    background = pygame.image.load('menu3.jpg').convert_alpha()
    background = pygame.transform.scale(background,(ANCHO,ALTO))

    lista_asteroide = pygame.sprite.Group()

    musica = pygame.mixer.Sound('theme-mp3.mp3')
    musica.set_volume(0.5)
    pygame.mixer.Sound.play(musica, -1)    

    flag_correr_juego = True
    while flag_correr_juego:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()#system quit
            if evento.type == pygame.KEYDOWN:
                if juego.flag_input == True:
                    if evento.key == K_BACKSPACE:
                        juego.texto_usuario = juego.texto_usuario[:-1]
                    else:
                        juego.texto_usuario += evento.unicode
        """
        Se vuelve al menu de inicio luego de perder
        """
        if juego.game_over == True:
            juego.flag_input = True
            juego.jugador.remove()#se borra el pj
            pantalla.blit(background,background.get_rect())
            pantalla.blit(txt,(txt_x,txt_y))
            pantalla.blit(titulo, titulo_rect) 

            pantalla.blit(txt_ingreso_nombre,(input_usuario.x - 5,input_usuario.y - 25))
            pygame.draw.rect(pantalla,colores.BLACK,input_usuario,2)
            superficie_txt_usuario = juego.fuente.render(juego.texto_usuario,True,colores.WHITE)
            pantalla.blit(superficie_txt_usuario,(input_usuario.x + 5, input_usuario.y + 5))
            #se blitea todo lo de la pantalla

            if evento.type == pygame.MOUSEBUTTONDOWN:
                juego.score = 0
                juego.vidas = 3
                for i in range(25):#asteroides
                    asteroide = Enemigo()#asigno enemigo
                    asteroide.rect.x = random.randrange(ANCHO)
                    asteroide.rect.y = random.randint(0,400)
                    lista_asteroide.add(asteroide)
                juego.game_over = False #cambio flags
                juego.flag_input = False #cambio flags

            lista_ranking = devolver_lista_scores(juego.ruta)
            for i in range(len(lista_ranking)):
            # se imprimen los rankings ya ordenados.
                texto = "{0}º {1}".format(i, lista_ranking[i]["nombre"])
                if i == 0:
                    color = colores.BLACK
                    tamaño = 30
                    texto = lista_ranking[i]["nombre"]
                else:
                    color = colores.WHITE
                    tamaño = 24 - i

                texto_nombre = juego.fuente.render(texto, True, color)
                pantalla.blit(texto_nombre,(150, 230+(i*30)))

                texto_tiempo = juego.fuente.render(str(lista_ranking[i]["score"]), True, color)
                pantalla.blit(texto_tiempo,(400, 230+(i*30)))
        else:
            pantalla.blit(imagen_space, imagen_space.get_rect())
            lista_asteroide.draw(pantalla)    
            lista_asteroide.update()
            juego.start()
            
            if len(lista_asteroide) == 0:
                juego.game_over = True
                for i in range(20):
                    asteroide = Enemigo()
                    asteroide.rect.x = random.randrange(ANCHO)
                    asteroide.rect.y = random.randint(0,400)
                    lista_asteroide.add(asteroide)
                if juego.score > 0:
                    guardar_score(juego.ruta,juego.texto_usuario,juego.score)
                    juego.texto_usuario = ''
        pygame.display.flip()
        reloj.tick(60)

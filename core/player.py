import pygame
from core.utils import cargar_frames_jugador
class Jugador:
    def __init__(self, x, y, imagen):
        self.x = x  
        self.y = y
        self.max_bombas = 1
        self.rango_explosion = 1
        self.velocidad = 1 
        self.color = (0, 255, 0)  
        self.vivo = True
        self.dx = 0  
        self.dy = 0 
        self.imagen = pygame.transform.scale(imagen, (40, 40))
        self.frames_por_direccion = {
            "up": cargar_frames_jugador("up", 3),
            "down": cargar_frames_jugador("down", 3),
            "left": cargar_frames_jugador("left", 3),
            "right": cargar_frames_jugador("right", 3),
            "dead": cargar_frames_jugador("dead", 3)
        }
        self.direccion_actual = "down"
        self.frame_actual = 0
        self.tiempo_ultimo_frame = pygame.time.get_ticks()
        self.frame_intervalo = 200 

        
    def mover(self, dx, dy, mapa):
        nueva_x = self.x + dx
        nueva_y = self.y + dy

        if dx == 1:
            self.direccion_actual = "right"
        elif dx == -1:
            self.direccion_actual = "left"
        elif dy == 1:
            self.direccion_actual = "down"
        elif dy == -1:
            self.direccion_actual = "up"


        if mapa[nueva_y][nueva_x] in (" ", "+B", "+R", "+V"):  
            celda = mapa[nueva_y][nueva_x]

            if celda == "+B":
                self.max_bombas += 1
            elif celda == "+R":
                self.rango_explosion += 1
            elif celda == "+V":
                self.velocidad += 1  

            mapa[nueva_y][nueva_x] = " " 

            self.x = nueva_x
            self.y = nueva_y
            self.dx = dx
            self.dy = dy

    def dibujar(self, pantalla, tamaño_celda):
        ahora = pygame.time.get_ticks()
        
        if self.vivo:
            if ahora - self.tiempo_ultimo_frame > self.frame_intervalo:
                self.frame_actual = (self.frame_actual + 1) % len(self.frames_por_direccion[self.direccion_actual])
                self.tiempo_ultimo_frame = ahora

            frame = self.frames_por_direccion[self.direccion_actual][self.frame_actual]
        else:
            if self.frame_actual < len(self.frames_por_direccion["dead"]) - 1:
                if ahora - self.tiempo_ultimo_frame > self.frame_intervalo:
                    self.frame_actual += 1
                    self.tiempo_ultimo_frame = ahora
            frame = self.frames_por_direccion["dead"][self.frame_actual]

        pos = (self.x * tamaño_celda, self.y * tamaño_celda)
        pantalla.blit(frame, pos)

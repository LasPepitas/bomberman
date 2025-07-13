import pygame

class Jugador:
    def __init__(self, x, y):
        self.x = x  
        self.y = y
        self.color = (0, 255, 0)  
        self.vivo = True
        self.dx = 0  
        self.dy = 0 

    def mover(self, dx, dy, mapa):
        nueva_x = self.x + dx
        nueva_y = self.y + dy

        if mapa[nueva_y][nueva_x] == " ":
            self.x = nueva_x
            self.y = nueva_y
            self.dx = dx
            self.dy = dy

    def dibujar(self, pantalla, tamaño_celda):
        if self.vivo:
            rect = pygame.Rect(self.x * tamaño_celda, self.y * tamaño_celda, tamaño_celda, tamaño_celda)
            pygame.draw.rect(pantalla, self.color, rect)

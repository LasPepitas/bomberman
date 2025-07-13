import pygame

def salir(evento):
    if evento.type == pygame.QUIT:
        pygame.quit()
        return

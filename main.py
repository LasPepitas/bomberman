from ui.menu import iniciar_juego
import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    
    pantalla = pygame.display.set_mode((800, 600))    
    
    iniciar_juego(pantalla)
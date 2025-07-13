import pygame
import sys
from ui.audio_manager import reproducir_audio, detener_audios
from core.game import ejecutar_juego

def menu_iniciar_juego(pantalla):
    pygame.display.set_caption("Bomberman - Iniciar Juego")

def menu_principal(pantalla):
    pygame.display.set_caption("Bomberman - Menú Principal")
    fuente_titulo = pygame.font.Font("ui/assets/fonts/Pixeboy.ttf", 80)
    fuente_opciones = pygame.font.Font("ui/assets/fonts/Pixeboy.ttf", 48)

    opciones = ["Nuevo juego", "Salir"]
    opcion_activa = 0
    reloj = pygame.time.Clock()
    musica_menu_reproducida = False

    while True:
        if not musica_menu_reproducida:
            reproducir_audio("ui/assets/audio/menu_music.mp3", loop=True)
            musica_menu_reproducida = True
        
        pantalla.fill((0, 0, 0))  
        
        titulo = fuente_titulo.render("Bomberman", True, (255, 255, 255))
        pantalla.blit(titulo, (280, 150))
        
        for i, texto in enumerate(opciones):
            color = (255, 255, 0) if i == opcion_activa else (200, 200, 200)
            render = fuente_opciones.render(texto, True, color)
            pantalla.blit(render, (150, 250 + i * 80))
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    opcion_activa = (opcion_activa - 1) % len(opciones)
                    reproducir_audio("ui/assets/audio/option.mp3", duracion=0.25)
                
                elif evento.key == pygame.K_DOWN:
                    opcion_activa = (opcion_activa + 1) % len(opciones)
                    reproducir_audio("ui/assets/audio/option.mp3", duracion=0.25)
                    
                elif evento.key == pygame.K_RETURN:
                    if opcion_activa == 0:
                        detener_audios()
                        ejecutar_juego(pantalla)
                        return
                    elif opcion_activa == 1:
                        pygame.quit()
                        sys.exit()
        
        pygame.display.flip()
        reloj.tick(30)

def iniciar_juego(pantalla):
    pygame.display.set_caption("Bomberman")

    intro_image = pygame.image.load("ui/assets/images/intro.png").convert_alpha()
    logo_image = pygame.image.load("ui/assets/images/logo2.png").convert_alpha()
    
    image = pygame.transform.scale(intro_image, (600, 500))
    logo = pygame.transform.scale(logo_image, (200, 200))
    
    fuente_logo = pygame.font.Font("ui/assets/fonts/Pixeboy.ttf", 74)
    
    reloj = pygame.time.Clock()

    tiempo_inicio_logo = pygame.time.get_ticks()
    tiempo_inicio_intro = tiempo_inicio_logo + 4000
    duracion_logo = 3000
    duracion_intro = 12000
    audio_intro_logo = False
    audio_intro_image = False
    
    while True:
        pantalla.fill((0, 0, 0))

        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual < tiempo_inicio_intro:
            if not audio_intro_logo:
                reproducir_audio("ui/assets/audio/intro_voice.mp3", duracion=4)
                audio_intro_logo = True
                
            transcurrido_logo = tiempo_actual - tiempo_inicio_logo
            progreso_logo = transcurrido_logo / duracion_logo
            alpha_logo = max(0, 255 - int(progreso_logo * 255))
            titulo = fuente_logo.render("Pepa Ping", True, (255, 255, 255))
            titulo2 = fuente_logo.render("Producciones", True, (255, 255, 255))
            
            titulo.set_alpha(alpha_logo)
            titulo2.set_alpha(alpha_logo)    
            logo.set_alpha(alpha_logo)
            
            pantalla.blit(logo, (100, 240))
            pantalla.blit(titulo, (300, 300))
            pantalla.blit(titulo2, (300, 340))    
            
        
        elif tiempo_actual >= tiempo_inicio_intro:
            if not audio_intro_image:
                reproducir_audio("ui/assets/audio/intro_music.mp3", duracion=12)
                audio_intro_image = True
                
            transcurrido_intro = tiempo_actual - tiempo_inicio_intro
            progreso_intro = transcurrido_intro / duracion_intro
            alpha_intro = max(0, 255 - int(progreso_intro * 255))
            image.set_alpha(alpha_intro)
            pantalla.blit(image, (100, 50))
        
            if transcurrido_intro >= duracion_intro:
                menu_principal(pantalla)
                return

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return
                elif evento.key == pygame.K_RETURN:
                    detener_audios() 
                    menu_principal(pantalla)
                    return

        pygame.display.flip()
        reloj.tick(30)

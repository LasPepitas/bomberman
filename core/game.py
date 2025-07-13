import pygame
from ui.audio_manager import reproducir_audio, detener_audios
# from core.map import MAPA
from core.player import Jugador
from core.bomb import Bomba
from core.enemy import EnemigoBasico, EnemigoInteligente, EnemigoAvanzado
from core.levels import cargar_nivel


def ejecutar_juego(pantalla):
    
    def plantar_bomba(x, y):
        bombas.append(Bomba(x, y))
    
    bombas = []
    jugador1 = Jugador(1, 1)
    nivel_actual = 1
    
    resultado = cargar_nivel(nivel_actual, jugador1, lambda: {(b.x, b.y) for b in bombas}, bombas, plantar_bomba)
    MAPA, enemigos = resultado[0], resultado[1]
    
    TAM_CELDA = 40
    
    pygame.display.set_caption("Bomberman - Juego")

    
    # enemigos = [
    #     EnemigoBasico(5, 5, MAPA),
    #     EnemigoInteligente(1, 5, MAPA, jugador1, obtener_bombas=lambda: {(b.x, b.y) for b in bombas}),
    #     EnemigoAvanzado(7, 3, MAPA, jugador1, obtener_bombas=bombas, plantar_bomba_cb=plantar_bomba)
    # ]
    reproducir_audio("ui/assets/audio/in_game.mp3", loop=True)
    
    reloj = pygame.time.Clock()
    corriendo = True

    while corriendo:
        pantalla.fill((0, 0, 0))  

        for y, fila in enumerate(MAPA):
            for x, celda in enumerate(fila):
                rect = pygame.Rect(x * TAM_CELDA, y * TAM_CELDA, TAM_CELDA, TAM_CELDA)
                if celda == "#":
                    pygame.draw.rect(pantalla, (100, 100, 100), rect)
                elif celda == "*":
                    pygame.draw.rect(pantalla, (160, 110, 50), rect)
                else:
                    pygame.draw.rect(pantalla, (0, 0, 0), rect)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    jugador1.mover(0, 1, MAPA)
                elif evento.key == pygame.K_UP:
                    jugador1.mover(0, -1, MAPA)
                elif evento.key == pygame.K_RIGHT:
                    jugador1.mover(1, 0, MAPA)
                elif evento.key == pygame.K_LEFT:
                    jugador1.mover(-1, 0, MAPA)
                if evento.key == pygame.K_SPACE:
                    bombas.append(Bomba(jugador1.x, jugador1.y))

        if not jugador1.vivo:
            fuente_game_over = pygame.font.Font("ui/assets/fonts/Pixeboy.ttf", 64)
            texto_game_over = fuente_game_over.render("GAME OVER", True, (255, 0, 0))
            pantalla.blit(texto_game_over, (pantalla.get_width() // 2 - texto_game_over.get_width() // 2,
                                            pantalla.get_height() // 2 - texto_game_over.get_height() // 2))
            detener_audios()
            reproducir_audio("ui/assets/audio/game_over.mp3", duracion=6)
            pygame.display.flip()
            pygame.time.delay(6000)
            from ui.menu import menu_principal 
            menu_principal(pantalla)
            return

        bombas_nuevas = []
        for bomba in bombas:
            if bomba.ha_explotado():
                casillas = bomba.explotar(MAPA)
                for (bx, by) in casillas:
                    if jugador1.vivo and jugador1.x == bx and jugador1.y == by:
                        jugador1.vivo = False
                    
                    for enemigo in enemigos:
                        if enemigo.vivo and enemigo.x == bx and enemigo.y == by:
                            enemigo.vivo = False
                        
                    rect = pygame.Rect(bx * TAM_CELDA, by * TAM_CELDA, TAM_CELDA, TAM_CELDA)
                    pygame.draw.rect(pantalla, (255, 100, 0), rect) 
            else:
                rect = pygame.Rect(bomba.x * TAM_CELDA, bomba.y * TAM_CELDA, TAM_CELDA, TAM_CELDA)
                pygame.draw.rect(pantalla, (0, 0, 255), rect)
                bombas_nuevas.append(bomba)
                    
        bombas = bombas_nuevas 
        jugador1.dibujar(pantalla, TAM_CELDA)
        
        for enemigo in enemigos:
            enemigo.dibujar(pantalla, TAM_CELDA)
            if enemigo.vivo and jugador1.vivo and jugador1.x == enemigo.x and jugador1.y == enemigo.y:
                jugador1.vivo = False

        if all(not e.vivo for e in enemigos):
            fuente_nivel = pygame.font.Font("ui/assets/fonts/Pixeboy.ttf", 48)
            texto = fuente_nivel.render("¡Nivel superado!", True, (0, 255, 0))
            pantalla.blit(texto, (pantalla.get_width() // 2 - texto.get_width() // 2,
                                pantalla.get_height() // 2 - texto.get_height() // 2))

            detener_audios()
            reproducir_audio("ui/assets/audio/victory.mp3", duracion=5)
            pygame.display.flip()
            pygame.time.delay(5000)

            nivel_actual += 1
            bombas.clear()
            resultado = cargar_nivel(nivel_actual, jugador1, lambda: {(b.x, b.y) for b in bombas}, bombas,plantar_bomba)
            if resultado:
                MAPA, enemigos = resultado[0], resultado[1]
                bombas.clear()
                reproducir_audio("ui/assets/audio/in_game.mp3", loop=True)

            else:
                from ui.menu import menu_principal
                menu_principal(pantalla)
                return
            

        pygame.display.flip()
        reloj.tick(30)

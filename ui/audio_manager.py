# ui/audio_manager.py
import pygame
import threading
import time

canales_activos = []

def reproducir_audio(path, duracion=None, loop=False):
    def _play():
        sound = pygame.mixer.Sound(path)
        canal = sound.play(loops=-1 if loop else 0)
        canales_activos.append(canal)

        if duracion:
            time.sleep(duracion)
            canal.stop()
            if canal in canales_activos:
                canales_activos.remove(canal)

    hilo = threading.Thread(target=_play, daemon=True)
    hilo.start()


def detener_audios():
    for canal in canales_activos:
        canal.stop()
    canales_activos.clear()

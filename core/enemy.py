import pygame
import random
import threading
import time
from core.utils import a_estrella, obtener_zona_explosion

class EnemigoBase:
    def __init__(self, x, y, mapa):
        self.x = x
        self.y = y
        self.mapa = mapa
        self.vivo = True

    def dibujar(self, pantalla, tam_celda):
        if self.vivo:
            rect = pygame.Rect(self.x * tam_celda, self.y * tam_celda, tam_celda, tam_celda)
            pygame.draw.rect(pantalla, self.color(), rect)

    def color(self):
        return (255, 0, 0) 


class EnemigoBasico(EnemigoBase):
    def __init__(self, x, y, mapa, obtener_bombas=None):
        super().__init__(x, y, mapa)
        self.obtener_bombas = obtener_bombas or (lambda: set())
        self.thread = threading.Thread(target=self._mover_aleatorio, daemon=True)
        self.thread.start()

    def _mover_aleatorio(self):
        while self.vivo:
            self.mover()
            time.sleep(0.6)

    # def mover(self):
    #     direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    #     random.shuffle(direcciones)
    #     for dx, dy in direcciones:
    #         nx, ny = self.x + dx, self.y + dy
    #         if 0 <= ny < len(self.mapa) and 0 <= nx < len(self.mapa[0]) and self.mapa[ny][nx] == " ":
    #             self.x, self.y = nx, ny
    #             break
    def mover(self):
        direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(direcciones)

        for dx, dy in direcciones:
            nx, ny = self.x + dx, self.y + dy
            if self._es_celda_libre(nx, ny):
                self.x, self.y = nx, ny
                break

    def _es_celda_libre(self, x, y):
        if not (0 <= y < len(self.mapa) and 0 <= x < len(self.mapa[0])):
            return False
        return self.mapa[y][x] == " " and (x, y) not in self.obtener_bombas()


    def color(self):
        return (255, 100, 100) 


class EnemigoInteligente(EnemigoBase):
    def __init__(self, x, y, mapa, jugador, obtener_bombas=None):
        super().__init__(x, y, mapa)
        self.jugador = jugador
        self.obtener_bombas = obtener_bombas
        self.thread = threading.Thread(target=self._seguir_jugador, daemon=True)
        self.thread.start()

    def _seguir_jugador(self):
        while self.vivo:
            bombas = self.obtener_bombas() if self.obtener_bombas else set()
            camino = a_estrella((self.x, self.y), (self.jugador.x, self.jugador.y), self.mapa, bombas)
            if camino:
                self.x, self.y = camino[0]
            time.sleep(0.4)

    def color(self):
        return (255, 0, 255) 
    
class EnemigoAvanzado(EnemigoBase):
    def __init__(self, x, y, mapa, jugador, obtener_bombas=None, plantar_bomba_cb=None):
        super().__init__(x, y, mapa)
        self.jugador = jugador
        self.obtener_bombas = obtener_bombas
        self.plantar_bomba_cb = plantar_bomba_cb
        self.thread = threading.Thread(target=self._inteligencia, daemon=True)
        self.thread.start()

    def _inteligencia(self):
        while self.vivo:
            bombas = self.obtener_bombas() if self.obtener_bombas else set()
            zona_peligrosa = set()
            bloqueos = set()

            for b in bombas:
                zona_peligrosa |= obtener_zona_explosion(b)
                bloqueos.add((b.x, b.y)) 

            for y in range(len(self.mapa)):
                for x in range(len(self.mapa[0])):
                    if self.mapa[y][x] == "*":
                        bloqueos.add((x, y))

            if (self.x, self.y) in zona_peligrosa:
                safe_spot = self._buscar_refugio(zona_peligrosa)
                if safe_spot:
                    self.x, self.y = safe_spot
                    time.sleep(0.2)
                    continue

            px = self.jugador.x + self.jugador.dx
            py = self.jugador.y + self.jugador.dy
            objetivo = (px, py) if self._es_celda_valida(px, py) else (self.jugador.x, self.jugador.y)

            camino = a_estrella((self.x, self.y), objetivo, self.mapa, bloqueos | zona_peligrosa)

            if camino:
                self.x, self.y = camino[0]

            if abs(self.x - self.jugador.x) + abs(self.y - self.jugador.y) <= 1:
                if self.plantar_bomba_cb:
                    self.plantar_bomba_cb(self.x, self.y)

            time.sleep(0.3)

    def _buscar_refugio(self, zona_peligrosa):
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = self.x + dx, self.y + dy
            if self._es_celda_valida(nx, ny) and (nx, ny) not in zona_peligrosa:
                return (nx, ny)
        return None

    def _es_celda_valida(self, x, y):
        if not (0 <= y < len(self.mapa) and 0 <= x < len(self.mapa[0])):
            return False
        if self.mapa[y][x] != " ":
            return False
        bombas = self.obtener_bombas() if self.obtener_bombas else set()
        return (x, y) not in {(b.x, b.y) for b in bombas}

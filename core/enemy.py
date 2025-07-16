import pygame
import random
import threading
import time
from core.utils import a_estrella, obtener_zona_explosion, cargar_frames, cargar_frames_vampire, cargar_frames_calavera

class EnemigoBase:
    def __init__(self, x, y, mapa):
        self.x = x
        self.y = y
        self.mapa = mapa
        self.vivo = True
        self.direccion_actual = "down"
        self.frames_por_direccion = {}
        self.frame_actual = 0
        self.tiempo_ultimo_frame = time.time()
        self.intervalo_frame = 0.25
        self.muriendo = False  
        self.muerte_completada = False 

    def dibujar(self, pantalla, tam_celda):
        if self.direccion_actual in self.frames_por_direccion:
            frames = self.frames_por_direccion[self.direccion_actual]
            ahora = time.time()

            if ahora - self.tiempo_ultimo_frame >= self.intervalo_frame:
                if self.direccion_actual == "dead":
                    if self.frame_actual < len(frames) - 1:
                        self.frame_actual += 1 
                    else:
                        self.muerte_completada = True
                else:
                    self.frame_actual = (self.frame_actual + 1) % len(frames)
                self.tiempo_ultimo_frame = ahora

            imagen = frames[self.frame_actual]
            pantalla.blit(imagen, (self.x * tam_celda, self.y * tam_celda))
        else:
            rect = pygame.Rect(self.x * tam_celda, self.y * tam_celda, tam_celda, tam_celda)
            pygame.draw.rect(pantalla, self.color(), rect)

    def morir(self):
        if not self.muriendo:
            self.vivo = False
            self.muriendo = True
            self.direccion_actual = "dead"
            self.frame_actual = 0
            self.tiempo_ultimo_frame = time.time()

    def color(self):
        return (255, 0, 0) 


class EnemigoBasico(EnemigoBase):
    def __init__(self, x, y, mapa, obtener_bombas=None):
        super().__init__(x, y, mapa)
        self.obtener_bombas = obtener_bombas or (lambda: set())
        self.frames_por_direccion = {
            "up": cargar_frames_vampire("up", 3),
            "down": cargar_frames_vampire("down", 3),
            "left": cargar_frames_vampire("left", 3),
            "right": cargar_frames_vampire("right", 3),
            "dead": cargar_frames_vampire("dead", 3)
        }
        self.direccion_actual = "down"
        self.frame_actual = 0
        self.tiempo_ultimo_frame = time.time()
        self.frame_intervalo = 0.15 
        self.thread = threading.Thread(target=self._mover_aleatorio, daemon=True)
        self.thread.start()

    def _mover_aleatorio(self):
        while self.vivo:
            self.mover()
            time.sleep(0.6)
    
    def mover(self):
        if self.muriendo:
            self.direccion_actual = "dead"
            return

        direcciones = [((0, 1), "down"), ((0, -1), "up"), ((1, 0), "right"), ((-1, 0), "left")]
        random.shuffle(direcciones)

        for (dx, dy), direccion in direcciones:
            nx, ny = self.x + dx, self.y + dy
            if self._es_celda_libre(nx, ny):
                self.x, self.y = nx, ny
                self.direccion_actual = direccion
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
        self.frames_por_direccion = {
            "up": cargar_frames("up", 3),
            "down": cargar_frames("down", 3),
            "left": cargar_frames("left", 3),
            "right": cargar_frames("right", 3),
            "dead": cargar_frames("dead", 3)
        }
        self.direccion_actual = "down"
        self.frame_actual = 0
        self.tiempo_ultimo_frame = time.time()
        self.frame_intervalo = 0.15 
        self.thread = threading.Thread(target=self._seguir_jugador, daemon=True)
        self.thread.start()

    def _seguir_jugador(self):
        while self.vivo:
            if self.muriendo: 
                time.sleep(0.1)
                continue
                
            bombas = self.obtener_bombas() if self.obtener_bombas else set()
            camino = a_estrella((self.x, self.y), (self.jugador.x, self.jugador.y), self.mapa, bombas)
            if camino:
                nx, ny = camino[0]
                dx = nx - self.x
                dy = ny - self.y

                if dx == 1:
                    self.direccion_actual = "right"
                elif dx == -1:
                    self.direccion_actual = "left"
                elif dy == 1:
                    self.direccion_actual = "down"
                elif dy == -1:
                    self.direccion_actual = "up"

                self.x, self.y = nx, ny
            time.sleep(0.4)

    def color(self):
        return (255, 0, 255) 

    
class EnemigoAvanzado(EnemigoBase):
    def __init__(self, x, y, mapa, jugador, obtener_bombas=None, plantar_bomba_cb=None):
        super().__init__(x, y, mapa)
        self.jugador = jugador
        self.obtener_bombas = obtener_bombas
        self.plantar_bomba_cb = plantar_bomba_cb
        self.frames_por_direccion = {
            "up": cargar_frames_calavera("up", 3),
            "down": cargar_frames_calavera("down", 3),
            "left": cargar_frames_calavera("left", 3),
            "right": cargar_frames_calavera("right", 3),
            "dead": cargar_frames_calavera("dead", 3)
        }
        self.direccion_actual = "down"
        self.frame_actual = 0
        self.tiempo_ultimo_frame = time.time()
        self.frame_intervalo = 0.15 
        self.thread = threading.Thread(target=self._inteligencia, daemon=True)
        self.thread.start()

    def _inteligencia(self):
        while self.vivo:
            if self.muriendo:
                time.sleep(0.1)
                continue
                
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
                nx, ny = camino[0]
                dx = nx - self.x
                dy = ny - self.y

                if dx == 1:
                    self.direccion_actual = "right"
                elif dx == -1:
                    self.direccion_actual = "left"
                elif dy == 1:
                    self.direccion_actual = "down"
                elif dy == -1:
                    self.direccion_actual = "up"

                self.x, self.y = nx, ny


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
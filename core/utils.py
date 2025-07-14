import heapq
import pygame

def a_estrella(inicio, objetivo, mapa, obstaculos_extra=None):
    filas = len(mapa)
    columnas = len(mapa[0])
    
    if obstaculos_extra is None:
        obstaculos_extra = set()
    
    def heuristica(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    abiertos = []
    heapq.heappush(abiertos, (0, inicio))
    
    came_from = {inicio: None}
    g_score = {inicio: 0}
    
    while abiertos:
        _, actual = heapq.heappop(abiertos)

        if actual == objetivo:
            camino = []
            while actual:
                camino.append(actual)
                actual = came_from[actual]
            camino.reverse()
            return camino[1:]  
        
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            vecino = (actual[0] + dx, actual[1] + dy)
            x, y = vecino

            if (0 <= x < columnas and 0 <= y < filas and mapa[y][x] == " " and (x, y) not in obstaculos_extra):
                tentative_g = g_score[actual] + 1
                if vecino not in g_score or tentative_g < g_score[vecino]:
                    g_score[vecino] = tentative_g
                    f_score = tentative_g + heuristica(vecino, objetivo)
                    heapq.heappush(abiertos, (f_score, vecino))
                    came_from[vecino] = actual

    return [] 

def obtener_zona_explosion(bomba, alcance=3):
    x, y = bomba.x, bomba.y
    zona = {(x, y)}
    
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        for i in range(1, alcance + 1):
            nx, ny = x + dx*i, y + dy*i
            if 0 <= ny < len(bomba.mapa) and 0 <= nx < len(bomba.mapa[0]):
                if bomba.mapa[ny][nx] == "#":
                    break
                zona.add((nx, ny))
            else:
                break
    return zona

def cargar_frames(direccion, cantidad, carpeta="ui/assets/images/enemigos/dragon"):
    return [
        pygame.transform.scale(
            pygame.image.load(f"{carpeta}/dragon_{direccion}{i}.png").convert_alpha(),
            (40, 40)
        ) for i in range(1, cantidad + 1)
    ]

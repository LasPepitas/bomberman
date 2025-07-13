import time

class Bomba:
    def __init__(self, x, y, tiempo_creacion=None, duracion=2, radio=1):
        self.x = x
        self.y = y
        self.tiempo_creacion = tiempo_creacion or time.time()
        self.duracion = duracion
        self.radio = radio
        self.exploto = False

    def ha_explotado(self):
        return time.time() - self.tiempo_creacion >= self.duracion

    def explotar(self, mapa):
        self.exploto = True
        casillas_afectadas = [(self.x, self.y)]  

        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            for i in range(1, self.radio + 1):
                nx = self.x + dx * i
                ny = self.y + dy * i

                if 0 <= ny < len(mapa) and 0 <= nx < len(mapa[0]):
                    if mapa[ny][nx] == "#":
                        break
                    
                    elif mapa[ny][nx] == "*":
                        mapa[ny][nx] = " "  
                
                    casillas_afectadas.append((nx, ny))
                else:
                    break  

        return casillas_afectadas

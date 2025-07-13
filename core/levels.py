# core/levels.py
from core.enemy import EnemigoBasico, EnemigoInteligente, EnemigoAvanzado

def cargar_nivel(nivel, jugador, obtener_bombas, bombas, plantar_bomba_cb):
    niveles = {
        1: {
            "mapa": [
                "####################",
                "#      *     #     #",
                "# ** ##### ## ## # #",
                "# #        #     # #",
                "# # ########### #  #",
                "# # #         # #  #",
                "#   # ### ### #    #",
                "##### #     # ######",
                "#     ### ###     ##",
                "# # #         # # ##",
                "# # ########### # ##",
                "# #     #        # #",
                "# ## ## ##### ## ###",
                "#     #     #     ##",
                "####################"
            ],
            "enemigos": [
                ("avanzado",10, 3),
                # ("avanzado", 3, 3),
            ],
            "inicio_jugador": (1, 1)
        },
        2: {
            "mapa": [
                "##########",
                "#     #  #",
                "# ## ##  #",
                "#  #     #",
                "##########"
            ],
            "enemigos": [
                ("avanzado", 7, 3),
                ("basico", 3, 2)
            ],
            "inicio_jugador": (1, 1)
        }
    }

    datos = niveles.get(nivel)
    if not datos:
        return None

    mapa = [list(fila) for fila in datos["mapa"]]
    jugador.x, jugador.y = datos["inicio_jugador"]

    enemigos = []
    for tipo, x, y in datos["enemigos"]:
        if tipo == "basico":
            enemigos.append(EnemigoBasico(x, y, mapa, obtener_bombas=obtener_bombas))
        elif tipo == "inteligente":
            enemigos.append(EnemigoInteligente(x, y, mapa, jugador, obtener_bombas=obtener_bombas))
        elif tipo == "avanzado":
            print(obtener_bombas, "asdasd")
            enemigos.append(EnemigoAvanzado(x, y, mapa, jugador, obtener_bombas=bombas, plantar_bomba_cb=plantar_bomba_cb))

    return mapa, enemigos

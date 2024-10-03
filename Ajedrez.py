import pygame
import sys

pygame.init()

ANCHO, ALTO = 640, 680
TAMAÑO_CASILLA = 640 // 8
fuente = pygame.font.Font(None, 36)
fuente_titulo = pygame.font.Font(None, 72)
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ajedrez")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
AMARILLO = (255, 255, 0)
VERDE = (0, 255, 0)
AZUL_CLARO = (173, 216, 230)

PIEZAS = {
    "r": pygame.image.load("Imagenes/iconos/Torre_Negro.png"),
    "n": pygame.image.load("Imagenes/iconos/Caballo_Negro.png"),
    "b": pygame.image.load("Imagenes/iconos/Alfil_Negro.png"),
    "q": pygame.image.load("Imagenes/iconos/Reina_Negro.png"),
    "k": pygame.image.load("Imagenes/iconos/Rey_Negro.png"),
    "p": pygame.image.load("Imagenes/iconos/Peon_Negro.png"),
    "R": pygame.image.load("Imagenes/iconos/Torre_Blanco.png"),
    "N": pygame.image.load("Imagenes/iconos/Caballo_Blanco.png"),
    "B": pygame.image.load("Imagenes/iconos/Alfil_Blanco.png"),
    "Q": pygame.image.load("Imagenes/iconos/Reina_Blanco.png"),
    "K": pygame.image.load("Imagenes/iconos/Rey_Blanco.png"),
    "P": pygame.image.load("Imagenes/iconos/Peon_Blanco.png"),
}

TABLERO_INICIAL = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
]


def dibujar_texto(texto, x, y, color=BLANCO, fuente=fuente):
    superficie = fuente.render(texto, True, color)
    rectangulo = superficie.get_rect()
    rectangulo.center = (x, y)
    PANTALLA.blit(superficie, rectangulo)


def dibujar_tablero(tablero, seleccionado, movimientos_validos):
    for fila in range(8):
        for col in range(8):
            color = BLANCO if (fila + col) % 2 == 0 else AZUL_CLARO
            pygame.draw.rect(
                PANTALLA,
                color,
                (
                    col * TAMAÑO_CASILLA,
                    fila * TAMAÑO_CASILLA + 40,
                    TAMAÑO_CASILLA,
                    TAMAÑO_CASILLA,
                ),
            )
            if (fila, col) == seleccionado:
                pygame.draw.rect(
                    PANTALLA,
                    VERDE,
                    (
                        col * TAMAÑO_CASILLA,
                        fila * TAMAÑO_CASILLA + 40,
                        TAMAÑO_CASILLA,
                        TAMAÑO_CASILLA,
                    ),
                    4,
                )
            if (fila, col) in movimientos_validos:
                pygame.draw.circle(
                    PANTALLA,
                    AMARILLO,
                    (
                        col * TAMAÑO_CASILLA + TAMAÑO_CASILLA // 2,
                        fila * TAMAÑO_CASILLA + TAMAÑO_CASILLA // 2 + 40,
                    ),
                    10,
                )
            pieza = tablero[fila][col]
            if pieza != ".":
                PANTALLA.blit(
                    pygame.transform.scale(
                        PIEZAS[pieza], (TAMAÑO_CASILLA, TAMAÑO_CASILLA)
                    ),
                    (col * TAMAÑO_CASILLA, fila * TAMAÑO_CASILLA + 40),
                )


def es_movimiento_valido(tablero, origen, destino, turno):
    pieza = tablero[origen[0]][origen[1]]
    if pieza == ".":
        return False
    if pieza.isupper() != turno:
        return False
    dif_fila = destino[0] - origen[0]
    dif_col = destino[1] - origen[1]
    if pieza.lower() == "p":
        if turno:
            return (
                (
                    dif_fila == -1
                    and dif_col == 0
                    and tablero[destino[0]][destino[1]] == "."
                )
                or (
                    dif_fila == -2
                    and dif_col == 0
                    and origen[0] == 6
                    and tablero[destino[0]][destino[1]] == "."
                    and tablero[destino[0] + 1][destino[1]] == "."
                )
                or (
                    dif_fila == -1
                    and abs(dif_col) == 1
                    and tablero[destino[0]][destino[1]].islower()
                )
            )
        else:
            return (
                (
                    dif_fila == 1
                    and dif_col == 0
                    and tablero[destino[0]][destino[1]] == "."
                )
                or (
                    dif_fila == 2
                    and dif_col == 0
                    and origen[0] == 1
                    and tablero[destino[0]][destino[1]] == "."
                    and tablero[destino[0] - 1][destino[1]] == "."
                )
                or (
                    dif_fila == 1
                    and abs(dif_col) == 1
                    and tablero[destino[0]][destino[1]].isupper()
                )
            )
    elif pieza.lower() == "r":
        return (dif_fila == 0 or dif_col == 0) and not es_camino_bloqueado(
            tablero, origen, destino
        )
    elif pieza.lower() == "n":
        return (abs(dif_fila) == 2 and abs(dif_col) == 1) or (
            abs(dif_fila) == 1 and abs(dif_col) == 2
        )
    elif pieza.lower() == "b":
        return abs(dif_fila) == abs(dif_col) and not es_camino_bloqueado(
            tablero, origen, destino
        )
    elif pieza.lower() == "q":
        return (
            dif_fila == 0 or dif_col == 0 or abs(dif_fila) == abs(dif_col)
        ) and not es_camino_bloqueado(tablero, origen, destino)
    elif pieza.lower() == "k":
        return abs(dif_fila) <= 1 and abs(dif_col) <= 1
    return False


def es_camino_bloqueado(tablero, origen, destino):
    paso_fila = 1 if destino[0] > origen[0] else -1 if destino[0] < origen[0] else 0
    paso_col = 1 if destino[1] > origen[1] else -1 if destino[1] < origen[1] else 0
    fila, col = origen
    while (fila, col) != destino:
        fila += paso_fila
        col += paso_col
        if (fila, col) != destino and tablero[fila][col] != ".":
            return True
    return False


def obtener_movimientos_validos(tablero, origen, turno):
    movimientos_validos = []
    for fila in range(8):
        for col in range(8):
            if es_movimiento_valido(tablero, origen, (fila, col), turno):
                movimientos_validos.append((fila, col))
    return movimientos_validos


def menu_principal():
    fuente = pygame.font.Font(None, 48)
    seleccion = 0
    opciones = ["Jugar", "Salir"]
    while True:
        PANTALLA.fill(NEGRO)
        dibujar_texto("Ajedrez", ANCHO // 2, ALTO // 4, BLANCO, fuente_titulo)
        for i, opcion in enumerate(opciones):
            color = BLANCO if i == seleccion else GRIS
            texto = fuente.render(opcion, True, color)
            PANTALLA.blit(
                texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 + i * 50)
            )
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    if seleccion == 0:
                        return
                    elif seleccion == 1:
                        pygame.quit()
                        sys.exit()


def menu_pausa():
    fuente = pygame.font.Font(None, 48)
    seleccion = 0
    opciones = ["Reanudar", "Reiniciar", "Salir al menu principal"]
    while True:
        PANTALLA.fill(NEGRO)
        for i, opcion in enumerate(opciones):
            color = BLANCO if i == seleccion else GRIS
            texto = fuente.render(opcion, True, color)
            PANTALLA.blit(
                texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 + i * 50)
            )
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    return opciones[seleccion].lower()


def reiniciar_partida():
    global tablero, turno, contador_turnos
    tablero = [fila[:] for fila in TABLERO_INICIAL]
    turno = True
    contador_turnos = 0


def main():
    global tablero, turno, contador_turnos
    while True:
        menu_principal()
        tablero = [fila[:] for fila in TABLERO_INICIAL]
        turno = True
        contador_turnos = 0
        seleccionado = None
        movimientos_validos = []
        reloj = pygame.time.Clock()
        juego_activo = True
        while juego_activo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        opcion = menu_pausa()
                        if opcion == "reanudar":
                            continue
                        elif opcion == "reiniciar":
                            reiniciar_partida()
                            seleccionado = None
                            movimientos_validos = []
                        elif opcion == "salir al menu principal":
                            juego_activo = False
                            break
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // TAMAÑO_CASILLA
                    fila = (pos[1] - 40) // TAMAÑO_CASILLA
                    if 0 <= fila < 8 and 0 <= col < 8:
                        if seleccionado is None:
                            seleccionado = (fila, col)
                            movimientos_validos = obtener_movimientos_validos(
                                tablero, seleccionado, turno
                            )
                        else:
                            if (fila, col) in movimientos_validos:
                                tablero[fila][col] = tablero[seleccionado[0]][
                                    seleccionado[1]
                                ]
                                tablero[seleccionado[0]][seleccionado[1]] = "."
                                turno = not turno
                                contador_turnos += 1
                            seleccionado = None
                            movimientos_validos = []
            if juego_activo:
                PANTALLA.fill(NEGRO)
                pygame.draw.rect(PANTALLA, GRIS, (0, 0, ANCHO, 40))
                texto_turno = fuente.render(
                    f'Turno: {"Blanco" if turno else "Negro"}', True, BLANCO
                )
                texto_contador = fuente.render(
                    f"Movimientos: {contador_turnos}", True, BLANCO
                )
                PANTALLA.blit(texto_turno, (20, 10))
                PANTALLA.blit(texto_contador, (ANCHO - 200, 10))
                dibujar_tablero(tablero, seleccionado, movimientos_validos)
                pygame.display.flip()
                reloj.tick(60)


if __name__ == "__main__":
    main()

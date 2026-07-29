#Proyecto final - Luis Felipe Pulido Segura
import os
import pygame
import sys
import random

pygame.init()
pygame.font.init()

#Musica
pygame.mixer.init()
BASE_DIR = os.path.dirname(__file__)
AUDIO_PATH = os.path.join(
    BASE_DIR, "Best Dubstep Mix 2020 [Brutal Dubstep Drops].mp3"
)
pygame.mixer.music.load(AUDIO_PATH)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

#Crear Pantalla
ANCHO, ALTO = 1000, 650
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("PONG REMAKE")
reloj = pygame.time.Clock()

# Declarar colores y fuentes
NEGRO = (15, 15, 20)
BLANCO = (240, 240, 240)
GRIS = (100, 100, 110)
GRIS_OSCURO = (40, 40, 50)
AZUL = (0, 180, 255)
ROJO = (255, 70, 70)
VERDE = (50, 220, 100)
AMARILLO = (255, 200, 0)
PURPURA = (180, 70, 255)
fuente_titulo = pygame.font.Font(None, 72)
fuente_menu = pygame.font.Font(None, 42)
fuente_hud = pygame.font.Font(None, 28)
fuente_sub = pygame.font.Font(None, 22)

# Habilidades
HABILIDADES = {
    "DASH": {
        "nombre": "Dash Rapido",
        "cooldown": 3000,  
        "duracion": 200    
    },
    "PALETA_GRANDE": {
        "nombre": "Paleta Gigante",
        "cooldown": 11000,
        "duracion": 4000
    },
    "ESCUDO": {
        "nombre": "Escudo Defensivo",
        "cooldown": 13500,
        "duracion": 3500
    },
    "GOLPE_RANDOM": {
        "nombre": "Golpe Random",
        "cooldown": 5000,
        "duracion": 500
    },
    "GOLPE_FUERTE": {
        "nombre": "Golpe Fuerte",
        "cooldown": 0,
        "duracion": 250
    }
}

LISTA_HABILIDADES = list(HABILIDADES.keys())

habilidad_j1_idx = 0  
habilidad_j2_idx = 0  

# Declarar Estados
estado = "MENU"
opcion_menu_idx = 0
opciones_menu = ["Play", "Selección de Habilidades", "Salir"]

# Parametros inciales
ANCHO_PALETA, ALTO_PALETA_BASE = 15, 90
TAMANO_PELOTA = 16
VEL_PALETA = 8

# Objetos
j1_rect = pygame.Rect(40, ALTO // 2 - ALTO_PALETA_BASE // 2, ANCHO_PALETA, ALTO_PALETA_BASE)
j2_rect = pygame.Rect(ANCHO - 40 - ANCHO_PALETA, ALTO // 2 - ALTO_PALETA_BASE // 2, ANCHO_PALETA, ALTO_PALETA_BASE)
pelota_rect = pygame.Rect(ANCHO // 2 - TAMANO_PELOTA // 2, ALTO // 2 - TAMANO_PELOTA // 2, TAMANO_PELOTA, TAMANO_PELOTA)

# Variables de juego
j1_puntos = 0
j2_puntos = 0
vel_pelota_x = 7.0 * random.choice((1, -1))
vel_pelota_y = 7.0 * random.choice((1, -1))

# Tiempos de habilidades
j1_ultimo_uso = 0
j1_activo_hasta = 0
j2_ultimo_uso = 0
j2_activo_hasta = 0

def reiniciar_juego():
    global j1_puntos, j2_puntos, j1_ultimo_uso, j2_ultimo_uso, j1_activo_hasta, j2_activo_hasta
    j1_puntos = 0
    j2_puntos = 0
    j1_ultimo_uso = 0
    j2_ultimo_uso = 0
    j1_activo_hasta = 0
    j2_activo_hasta = 0
    reiniciar_pelota()

def reiniciar_pelota():
    global vel_pelota_x, vel_pelota_y
    pelota_rect.center = (ANCHO // 2, ALTO // 2)
    vel_pelota_x = 7.0 * random.choice((1, -1))
    vel_pelota_y = 5.0 * random.choice((1, -1))

def aplicar_golpe_random():
    global vel_pelota_x, vel_pelota_y
    factor_x = random.uniform(1.0, 2.5)
    factor_y = random.uniform(1.0, 2.5)
    
    dir_x = 1 if vel_pelota_x >= 0 else -1
    dir_y = 1 if vel_pelota_y >= 0 else -1
    
    vel_pelota_x = (abs(vel_pelota_x) * factor_x) * dir_x
    vel_pelota_y = (abs(vel_pelota_y) * factor_y) * dir_y

def aplicar_golpe_fuerte():
    global vel_pelota_x, vel_pelota_y
    dir_x = 1 if vel_pelota_x >= 0 else -1
    dir_y = 1 if vel_pelota_y >= 0 else -1
    vel_pelota_x = (abs(vel_pelota_x) + 0.5) * dir_x
    vel_pelota_y = (abs(vel_pelota_y) + 0.5) * dir_y

def obtener_color_paleta(tiempo_actual, hab_key, esta_activa, color_por_defecto):
    if esta_activa:
        if hab_key == "GOLPE_RANDOM":
            return PURPURA
        elif hab_key == "GOLPE_FUERTE":
            return ROJO
        else:
            return color_por_defecto
    return BLANCO

# Ejecuta juego
ejecutando = True
while ejecutando:
    tiempo_actual = pygame.time.get_ticks()

    # Gestion
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.KEYDOWN:
            # Mov menu
            if estado == "MENU":
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    opcion_menu_idx = (opcion_menu_idx - 1) % len(opciones_menu)
                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    opcion_menu_idx = (opcion_menu_idx + 1) % len(opciones_menu)
                elif evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if opcion_menu_idx == 0:
                        reiniciar_juego()
                        estado = "JUEGO"
                    elif opcion_menu_idx == 1:
                        estado = "SELECCION"
                    elif opcion_menu_idx == 2: 
                        ejecutando = False

            # Mov seleccion
            elif estado == "SELECCION":
                # Mov J1
                if evento.key == pygame.K_w:
                    habilidad_j1_idx = (habilidad_j1_idx - 1) % len(LISTA_HABILIDADES)
                elif evento.key == pygame.K_s:
                    habilidad_j1_idx = (habilidad_j1_idx + 1) % len(LISTA_HABILIDADES)
                
                # Mov J2
                if evento.key == pygame.K_UP:
                    habilidad_j2_idx = (habilidad_j2_idx - 1) % len(LISTA_HABILIDADES)
                elif evento.key == pygame.K_DOWN:
                    habilidad_j2_idx = (habilidad_j2_idx + 1) % len(LISTA_HABILIDADES)

                # Bot listo
                if evento.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    estado = "MENU"

            # Mov in game
            elif estado == "JUEGO":
                if evento.key == pygame.K_ESCAPE:
                    estado = "MENU"

                # Hab J1
                hab_j1_key = LISTA_HABILIDADES[habilidad_j1_idx]
                cd_j1 = HABILIDADES[hab_j1_key]["cooldown"]
                if evento.key in (pygame.K_SPACE, pygame.K_f):
                    if tiempo_actual - j1_ultimo_uso >= cd_j1:
                        j1_ultimo_uso = tiempo_actual
                        j1_activo_hasta = tiempo_actual + HABILIDADES[hab_j1_key]["duracion"]
                        
                        # Efectos insta J1
                        if hab_j1_key == "DASH":
                            teclas = pygame.key.get_pressed()
                            if teclas[pygame.K_w]: j1_rect.y -= 120
                            elif teclas[pygame.K_s]: j1_rect.y += 120
                            j1_rect.clamp_ip(pantalla.get_rect())
                        elif hab_j1_key == "GOLPE_RANDOM":
                            aplicar_golpe_random()
                        elif hab_j1_key == "GOLPE_FUERTE":
                            aplicar_golpe_fuerte()

                # Hab J2
                hab_j2_key = LISTA_HABILIDADES[habilidad_j2_idx]
                cd_j2 = HABILIDADES[hab_j2_key]["cooldown"]
                if evento.key in (pygame.K_RETURN, pygame.K_l):
                    if tiempo_actual - j2_ultimo_uso >= cd_j2:
                        j2_ultimo_uso = tiempo_actual
                        j2_activo_hasta = tiempo_actual + HABILIDADES[hab_j2_key]["duracion"]

                        # Efectos insta J2
                        if hab_j2_key == "DASH":
                            teclas = pygame.key.get_pressed()
                            if teclas[pygame.K_UP]: j2_rect.y -= 120
                            elif teclas[pygame.K_DOWN]: j2_rect.y += 120
                            j2_rect.clamp_ip(pantalla.get_rect())
                        elif hab_j2_key == "GOLPE_RANDOM":
                            aplicar_golpe_random()
                        elif hab_j2_key == "GOLPE_FUERTE":
                            aplicar_golpe_fuerte()

    # Logica
    if estado == "JUEGO":
        teclas = pygame.key.get_pressed()

        # Ajuste Pal_Gra
        hab_j1_nombre = LISTA_HABILIDADES[habilidad_j1_idx]
        hab_j2_nombre = LISTA_HABILIDADES[habilidad_j2_idx]

        j1_altura = ALTO_PALETA_BASE * 1.6 if (hab_j1_nombre == "PALETA_GRANDE" and tiempo_actual < j1_activo_hasta) else ALTO_PALETA_BASE
        j2_altura = ALTO_PALETA_BASE * 1.6 if (hab_j2_nombre == "PALETA_GRANDE" and tiempo_actual < j2_activo_hasta) else ALTO_PALETA_BASE

        j1_rect.height = int(j1_altura)
        j2_rect.height = int(j2_altura)

        # Mov j1
        if teclas[pygame.K_w] and j1_rect.top > 0:
            j1_rect.y -= VEL_PALETA
        if teclas[pygame.K_s] and j1_rect.bottom < ALTO:
            j1_rect.y += VEL_PALETA

        # Mov J2
        if teclas[pygame.K_UP] and j2_rect.top > 0:
            j2_rect.y -= VEL_PALETA
        if teclas[pygame.K_DOWN] and j2_rect.bottom < ALTO:
            j2_rect.y += VEL_PALETA

        # Pelota
        pelota_rect.x += int(vel_pelota_x)
        pelota_rect.y += int(vel_pelota_y)

        # Rebote
        if pelota_rect.top <= 0 or pelota_rect.bottom >= ALTO:
            vel_pelota_y *= -1

        # Colision
        if pelota_rect.colliderect(j1_rect) and vel_pelota_x < 0:
            vel_pelota_x *= -1
            vel_pelota_x += 0.3
        if pelota_rect.colliderect(j2_rect) and vel_pelota_x > 0:
            vel_pelota_x *= -1
            vel_pelota_x -= 0.3

        # Escudo
        escudo_j1_activo = (hab_j1_nombre == "ESCUDO" and tiempo_actual < j1_activo_hasta)
        escudo_j2_activo = (hab_j2_nombre == "ESCUDO" and tiempo_actual < j2_activo_hasta)

        if escudo_j1_activo and pelota_rect.left <= 15:
            vel_pelota_x = abs(vel_pelota_x)

        if escudo_j2_activo and pelota_rect.right >= ANCHO - 15:
            vel_pelota_x = -abs(vel_pelota_x)

        # Anot SCORE
        if pelota_rect.left <= 0:
            j2_puntos += 1
            reiniciar_pelota()
        elif pelota_rect.right >= ANCHO:
            j1_puntos += 1
            reiniciar_pelota()

    pantalla.fill(NEGRO)

    # Menu
    if estado == "MENU":
        titulo = fuente_titulo.render("> PONG HABILIDADES <", True, AZUL)
        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 100))

        for idx, opcion in enumerate(opciones_menu):
            color = AMARILLO if idx == opcion_menu_idx else GRIS
            prefijo = "> " if idx == opcion_menu_idx else "  "
            txt = fuente_menu.render(prefijo + opcion, True, color)
            pantalla.blit(txt, (ANCHO // 2 - 140, 260 + idx * 70))

        sub = fuente_sub.render("Usa Flechas / W-S para navegar y ENTER para seleccionar", True, GRIS)
        pantalla.blit(sub, (ANCHO // 2 - sub.get_width() // 2, ALTO - 50))

    # Seleccion
    elif estado == "SELECCION":
        titulo = fuente_titulo.render("SELECCIÓN DE HABILIDADES", True, BLANCO)
        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 50))

        # J1
        pygame.draw.rect(pantalla, GRIS_OSCURO, (100, 160, 360, 380), border_radius=12)
        pygame.draw.rect(pantalla, AZUL, (100, 160, 360, 380), 3, border_radius=12)
        txt_j1 = fuente_menu.render("JUGADOR 1", True, AZUL)
        pantalla.blit(txt_j1, (130, 180))

        for idx, hab_key in enumerate(LISTA_HABILIDADES):
            color = VERDE if idx == habilidad_j1_idx else BLANCO
            marcador = "[X] " if idx == habilidad_j1_idx else "[  ] "
            txt_hab = fuente_hud.render(marcador + HABILIDADES[hab_key]["nombre"], True, color)
            pantalla.blit(txt_hab, (120, 240 + idx * 45))

        # J2
        pygame.draw.rect(pantalla, GRIS_OSCURO, (540, 160, 360, 380), border_radius=12)
        pygame.draw.rect(pantalla, ROJO, (540, 160, 360, 380), 3, border_radius=12)
        txt_j2 = fuente_menu.render("JUGADOR 2", True, ROJO)
        pantalla.blit(txt_j2, (560, 180))

        for idx, hab_key in enumerate(LISTA_HABILIDADES):
            color = VERDE if idx == habilidad_j2_idx else BLANCO
            marcador = "[X] " if idx == habilidad_j2_idx else "[  ] "
            txt_hab = fuente_hud.render(marcador + HABILIDADES[hab_key]["nombre"], True, color)
            pantalla.blit(txt_hab, (560, 240 + idx * 45))

        sub = fuente_sub.render("Presiona ENTER o ESC para guardar y volver al Menú", True, AMARILLO)
        pantalla.blit(sub, (ANCHO // 2 - sub.get_width() // 2, ALTO - 40))

    # Play
    elif estado == "JUEGO":
        for y in range(0, ALTO, 25):
            pygame.draw.rect(pantalla, GRIS_OSCURO, (ANCHO // 2 - 2, y, 4, 12))

        hab_j1_key = LISTA_HABILIDADES[habilidad_j1_idx]
        hab_j2_key = LISTA_HABILIDADES[habilidad_j2_idx]

        # Barrera de Escudo en VERDE
        if hab_j1_key == "ESCUDO" and tiempo_actual < j1_activo_hasta:
            pygame.draw.rect(pantalla, VERDE, (5, 0, 8, ALTO))

        if hab_j2_key == "ESCUDO" and tiempo_actual < j2_activo_hasta:
            pygame.draw.rect(pantalla, VERDE, (ANCHO - 13, 0, 8, ALTO))

        # Colores de paletas según estado de la habilidad activa
        j1_activa = (tiempo_actual < j1_activo_hasta)
        j2_activa = (tiempo_actual < j2_activo_hasta)

        color_p1 = obtener_color_paleta(tiempo_actual, hab_j1_key, j1_activa, AZUL)
        color_p2 = obtener_color_paleta(tiempo_actual, hab_j2_key, j2_activa, ROJO)

        pygame.draw.rect(pantalla, color_p1, j1_rect, border_radius=4)
        pygame.draw.rect(pantalla, color_p2, j2_rect, border_radius=4)
        pygame.draw.ellipse(pantalla, BLANCO, pelota_rect)

        # Score
        txt_puntos_j1 = fuente_titulo.render(str(j1_puntos), True, BLANCO)
        txt_puntos_j2 = fuente_titulo.render(str(j2_puntos), True, BLANCO)
        pantalla.blit(txt_puntos_j1, (ANCHO // 4, 30))
        pantalla.blit(txt_puntos_j2, (3 * ANCHO // 4, 30))

        # Cooldowns
        cd_max_j1 = HABILIDADES[hab_j1_key]["cooldown"]
        restante_j1 = max(0, (cd_max_j1 - (tiempo_actual - j1_ultimo_uso)) / 1000)
        estado_j1 = "LISTO (ESPACIO)" if restante_j1 == 0 else f"{restante_j1:.1f}s"
        col_j1 = VERDE if restante_j1 == 0 else ROJO

        hud_j1 = fuente_hud.render(f"J1 [{HABILIDADES[hab_j1_key]['nombre']}]: {estado_j1}", True, col_j1)
        pantalla.blit(hud_j1, (30, ALTO - 40))

        cd_max_j2 = HABILIDADES[hab_j2_key]["cooldown"]
        restante_j2 = max(0, (cd_max_j2 - (tiempo_actual - j2_ultimo_uso)) / 1000)
        estado_j2 = "LISTO (ENTER)" if restante_j2 == 0 else f"{restante_j2:.1f}s"
        col_j2 = VERDE if restante_j2 == 0 else ROJO

        hud_j2 = fuente_hud.render(f"J2 [{HABILIDADES[hab_j2_key]['nombre']}]: {estado_j2}", True, col_j2)
        pantalla.blit(hud_j2, (ANCHO - 380, ALTO - 40))

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()
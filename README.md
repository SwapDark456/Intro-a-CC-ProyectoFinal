# 🎮 Pong Remake

Este adaptacion del juego clasico Pong fue desarrollado por Luis Felipe Pulido Segura como Proyecto final para la clase de Introducción a Ciencias de la Computacion de la Universidad Nacional de Colombia.

---

## 🏗️ Arquitectura y Mecánicas Técnicas

### 1. Sistema de Colisiones (`pygame.Rect`)
El motor de física utiliza una aproximación basada en **AABB (Axis-Aligned Bounding Boxes)** a través de los objetos `pygame.Rect` de los *sprites*:

* **Detección entre Entidades (AABB):** Se evalúa la superposición de cajas delimitadoras utilizando la función `pygame.Rect.colliderect()`. Esto permite resolver impactos entre proyectiles, jugadores y elementos del entorno con bajo costo computacional.
* **Agrupación y Recorrido de Sprites:** Las entidades interactivas están organizadas en `pygame.sprite.Group()`. Las colisiones múltiples se gestionan mediante `pygame.sprite.spritecollide()` o `groupcollide()`, eliminando proyectiles en impacto (`dokill=True`) y procesando los eventos de daño inmediatamente en la misma iteración del bucle principal.
* **Delimitación de Pantalla (Boundary Checks):** La posición de los personajes y sus rectángulos (`rect.x`, `rect.y`) se restringen continuamente respecto a la superficie principal (`screen.get_rect()`) para evitar que las entidades salgan del área de renderizado.

### 2. Sistema de Habilidades (Abstracción y Estado)
La selección y ejecución de habilidades se gestiona mediante una estructura de estados modular:

* **Matriz / Diccionario de Habilidades:** Cada habilidad está definida con sus atributos clave: *cooldown* (tiempo de recarga en ms), *daño*, *costo de energía/maná*, y *función de efecto/proyectil*.
* **Control de Cooldown (Tick System):** La recarga de habilidades utiliza la marca de tiempo absoluta de Pygame mediante `pygame.time.get_ticks()`. Se compara la diferencia de tiempo actual frente al momento del último uso:
  Si $\Delta t \ge \text{cooldown}$, la habilidad se activa y rescata el tick actual.
* **Instanciación Dinámica:** Al activar una habilidad de ataque, el juego instancia un objeto `Projectile` o `AreaOfEffect` que hereda de `pygame.sprite.Sprite`, asignándole un vector de movimiento (`velocity_x`, `velocity_y`) y registrándolo en el grupo de proyectiles activos.

---

## 🎵 Sistema de Audio Adaptativo

Para evitar el uso excesivo de RAM, el motor diferencia los efectos de sonido efímeros del flujo de audio principal:
* **Audio en Streaming:** Se utiliza `pygame.mixer.music` para transmitir la música de fondo directamente desde el almacenamiento.
* **Gestor de Transición:** La reproducción cambia dinámicamente según el estado global (`game_state`), aplicando transiciones suaves con `fade_ms`.

---

## 📥 Descarga de Recurso de Audio Externo

Por restricciones de tamaño en el repositorio, la pista musical principal debe descargarse de forma independiente:

🔗 **[Descargar Banda Sonora del Juego (Google Drive)](https://drive.google.com/file/d/1Drcs7ESv9tZg5x0gYHVEcvaBoMGF1pXq/view?usp=sharing)**

> **Ubicación del archivo:** Una vez descargado, coloca el archivo `.mp3` dentro de la carpeta raíz del proyecto para que la ruta relativa o la variable `BASE_DIR` de Python lo detecte automáticamente al arrancar.

---

## 🚀 Instalación y Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
   cd tu-repositorio

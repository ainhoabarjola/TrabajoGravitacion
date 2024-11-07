import pygame  # Para dibujar el sistema 
import numpy as np

# Configuración de la ventana de simulación
WIDTH, HEIGHT = 1400, 800
DARK_BLUE = (10, 10, 30)
WHITE = (255, 255, 255)

# Constantes físicas
G = 6.67430e-11  # Constante gravitacional (m^3 kg^-1 s^-2)
TIME_STEP = 3600  # Paso de tiempo en segundos (1 hora)

class Cuerpo:
    def __init__(self, x, y, masa, vx=0, vy=0, radio=10, color=WHITE, nombre=""):
        self.x = x  # posición en el eje x
        self.y = y  # posición en el eje y
        self.masa = masa
        self.vx = vx  # velocidad en el eje x
        self.vy = vy  # velocidad en el eje y
        self.radio = radio
        self.color = color
        self.nombre = nombre  # Nombre del cuerpo celeste
        self.historial_posiciones = []  # Lista para almacenar la trayectoria

    def calcular_fuerza_gravitacional(self, otro_cuerpo):
        # Distancia entre los cuerpos
        dx = otro_cuerpo.x - self.x
        dy = otro_cuerpo.y - self.y
        distancia = np.sqrt(dx**2 + dy**2)  # módulo
        
        if distancia == 0:
            return 0, 0  # Para evitar divisiones por cero
        
        # Ley de gravitación de Newton
        fuerza = G * self.masa * otro_cuerpo.masa / distancia**2
        angulo = np.arctan2(dy, dx)
        
        # Componentes de la fuerza
        fx = np.cos(angulo) * fuerza
        fy = np.sin(angulo) * fuerza
        return fx, fy

    def actualizar_posicion(self, fx, fy):
        # Actualizar velocidades según la fuerza aplicada y la masa
        ax = fx / self.masa
        ay = fy / self.masa
        self.vx += ax * TIME_STEP
        self.vy += ay * TIME_STEP
        
        # Actualizar posición según la velocidad
        self.x += self.vx * TIME_STEP
        self.y += self.vy * TIME_STEP

        # Guardar la posición en el historial para trazar la órbita
        self.historial_posiciones.append((self.x, self.y))

    def dibujar(self, pantalla):
        # Convertir la posición en coordenadas de pantalla
        x = int(self.x * WIDTH / (3e11) + WIDTH / 2)
        y = int(self.y * HEIGHT / (3e11) + HEIGHT / 2)
        
        # Dibujar la trayectoria
        if len(self.historial_posiciones) > 2:
            puntos = [(int(px * WIDTH / (3e11) + WIDTH / 2), int(py * HEIGHT / (3e11) + HEIGHT / 2))
                      for px, py in self.historial_posiciones]
            pygame.draw.lines(pantalla, self.color, False, puntos, 1)
        
        # Dibujar el cuerpo como un círculo
        pygame.draw.circle(pantalla, self.color, (x, y), self.radio)
        
        # Dibujar el nombre del cuerpo celeste
        self.dibujar_nombre(pantalla, x, y)

    def dibujar_nombre(self, pantalla, x, y):
        # Establecer la fuente y el tamaño del texto
        font = pygame.font.Font(None, 36)  # Fuente predeterminada de Pygame
        texto = font.render(self.nombre, True, WHITE)
        texto_rect = texto.get_rect(center=(x, y - self.radio - 15))  # Posicionar arriba del cuerpo
        pantalla.blit(texto, texto_rect)  # Dibujar el texto en la pantalla

def dibujar_estrellas(pantalla, cantidad=100):
    """Dibuja estrellas en el fondo de la pantalla."""
    for _ in range(cantidad):
        x = np.random.randint(0, WIDTH)
        y = np.random.randint(0, HEIGHT)
        pygame.draw.circle(pantalla, WHITE, (x, y), 1)  # Dibujar estrella

def dibujar_texto(pantalla, texto, pos_x, pos_y):
    """Dibuja texto en la pantalla."""
    font = pygame.font.Font(None, 36)  # Fuente predeterminada de Pygame
    texto_superior = font.render(texto, True, WHITE)
    pantalla.blit(texto_superior, (pos_x, pos_y))

# Inicializar pygame y crear ventana
pygame.init()
pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Órbita en Campo Gravitatorio")

# Creación de cuerpos: 
sol = Cuerpo(x=0, y=0, masa=1.989e30, radio=20, color=(255, 204, 0), nombre="Sol")
# Ajustar la distancia orbital del planeta Flopii más cerca del Sol
flopii = Cuerpo(x=8.0e10, y=0, masa=5.972e24, vy=37783, radio=5, color=(100, 100, 255), nombre="Flopii")  # Distancia orbital ajustada
planeta_rapido = Cuerpo(x=6.0e10, y=0, masa=4.867e24, vy=40000, radio=6, color=(255, 100, 100), nombre="Mercurio")  # Mercurio

# Llamada para dibujar estrellas al inicio
estrellas = []  # Almacenar posiciones de estrellas fijas
dibujar_estrellas(pantalla, 200)  # Puedes ajustar la cantidad de estrellas aquí

# Bucle de simulación
corriendo = True
reloj = pygame.time.Clock()

# Generar estrellas fijas
for _ in range(200):
    x = np.random.randint(0, WIDTH)
    y = np.random.randint(0, HEIGHT)
    estrellas.append((x, y))  # Almacena las posiciones de las estrellas

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    # Limpiar pantalla
    pantalla.fill(DARK_BLUE)

    # Dibujar estrellas fijas
    for estrella in estrellas:
        pygame.draw.circle(pantalla, WHITE, estrella, 1)  # Dibujar estrella

    # Calcular la fuerza gravitacional entre los planetas y el sol
    fx_flopii, fy_flopii = flopii.calcular_fuerza_gravitacional(sol)
    fx_planeta_rapido, fy_planeta_rapido = planeta_rapido.calcular_fuerza_gravitacional(sol)
    
    # Actualizar posición de los cuerpos
    flopii.actualizar_posicion(fx_flopii, fy_flopii)
    planeta_rapido.actualizar_posicion(fx_planeta_rapido, fy_planeta_rapido)

    # Dibujar los cuerpos
    sol.dibujar(pantalla)
    flopii.dibujar(pantalla)
    planeta_rapido.dibujar(pantalla)

    # Calcular período orbital para Flopii y Mercurio
    r_flopii = 8.0e10  # Distancia media de Flopii al Sol (en metros)
    r_mercurio = 6.0e10  # Distancia media de Mercurio al Sol (en metros)

    T_flopii = 2 * np.pi * np.sqrt(r_flopii**3 / (G * sol.masa))  # Período de Flopii
    T_mercurio = 2 * np.pi * np.sqrt(r_mercurio**3 / (G * sol.masa))  # Período de Mercurio

    # Dibujar texto informativo sobre fuerzas y períodos orbitales
    dibujar_texto(pantalla, "Simulador del Sistema Solar", 10, 10)
    dibujar_texto(pantalla, "Fuerza Flopii-Sol: {:.2e} N".format(np.sqrt(fx_flopii**2 + fy_flopii**2)), 10, 50)
    dibujar_texto(pantalla, "Fuerza Mercurio-Sol: {:.2e} N".format(np.sqrt(fx_planeta_rapido**2 + fy_planeta_rapido**2)), 10, 90)
    dibujar_texto(pantalla, "Período Flopii: {:.2f} días".format(T_flopii / (86400)), 10, 130)  # Convertir a días
    dibujar_texto(pantalla, "Período Mercurio: {:.2f} días".format(T_mercurio / (86400)), 10, 170)  # Convertir a días

    pygame.display.flip()
    reloj.tick(60)  # Limitar a 60 FPS

pygame.quit()

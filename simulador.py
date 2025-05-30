import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Parámetros
ovejas_nacidas_al_año = 2  # tasa de crías por pareja por año

# Ecuación diferencial
def crecimiento_ovejas(tiempo, poblacion):
    return ovejas_nacidas_al_año * (poblacion / 2)

# Condiciones iniciales
poblacion_inicial = 2

intervalo_tiempo = (0, 3.91)
tiempos_simulacion = np.linspace(intervalo_tiempo[0], intervalo_tiempo[1], 100)

# Resolver la ecuación diferencial de primer orden (initial value problem)
solucion = solve_ivp(crecimiento_ovejas, intervalo_tiempo, [poblacion_inicial], t_eval=tiempos_simulacion)

# Graficar solución tradicional
plt.figure()
plt.plot(solucion.t, solucion.y[0], label="Crecimiento de las ovejas")

ovejas = solucion.y[0]
tiempos = solucion.t
indices_marker = [i for i, n in enumerate(ovejas) if int(n) % 10 == 0 and i > 0 and int(ovejas[i-1]) % 10 != 0]

plt.plot(tiempos[indices_marker], ovejas[indices_marker], 'ro', label="Cada 10 ovejas")
plt.xlabel("Años transcurridos") 
plt.ylabel("Número de ovejas")
plt.title("Crecimiento exponencial de ovejas")
plt.grid(True)
plt.legend()

# Animación de ovejas como puntos negros
figura_animacion, ejes_animacion = plt.subplots()
ejes_animacion.set_xlim(0, 10)
ejes_animacion.set_ylim(0, 10)
ejes_animacion.set_title("Las ovejas reproduciendose como locas")
ejes_animacion.set_xlabel("X")
ejes_animacion.set_ylabel("Y")
dispersión_ovejas = ejes_animacion.scatter([], [], c='black')
texto_cantidad_ovejas = ejes_animacion.text(0.02, 0.95, '', transform=ejes_animacion.transAxes, fontsize=12, color='black', bbox=dict(facecolor='white', alpha=0.7))

# Inicializar lista de posiciones
posiciones_ovejas = []

# Carga la imagen de la oveja (ajusta el path si es necesario)
path = "Jeb_Sheep_JE2.webp"
imagen_oveja = plt.imread(path)  # Debe estar en la misma carpeta o poner el path completo

# Variable para usar la imagen en la animación:
imagen_offset_oveja = OffsetImage(imagen_oveja, zoom=0.1)  # Puedes ajustar el zoom

def iniciar_animacion():
    dispersión_ovejas.set_offsets(np.empty((0, 2)))
    texto_cantidad_ovejas.set_text('')
    return dispersión_ovejas, texto_cantidad_ovejas

def animar_ovejas(indice):
    # Número de ovejas en este tiempo (redondeado)
    cantidad_ovejas = int(round(solucion.y[0][indice]))
    # Si hay más ovejas que puntos, agregamos nuevas posiciones aleatorias
    while len(posiciones_ovejas) < cantidad_ovejas:
        x, y = np.random.uniform(0, 10), np.random.uniform(0, 10)
        posiciones_ovejas.append([x, y])
    # Si hay menos ovejas que puntos, quitamos posiciones
    while len(posiciones_ovejas) > cantidad_ovejas:
        posiciones_ovejas.pop()
    if posiciones_ovejas:
        dispersión_ovejas.set_offsets(np.array(posiciones_ovejas))
    else:
        dispersión_ovejas.set_offsets(np.empty((0, 2)))
    texto_cantidad_ovejas.set_text(f'Ovejas: {cantidad_ovejas}\nTiempo: {solucion.t[indice]:.2f} años')
    
    # Limpiar artistas anteriores
    for artist in ejes_animacion.artists:
        artist.remove()
    
    # Agregar nuevas ovejas como imágenes
    for pos in posiciones_ovejas:
        ab = AnnotationBbox(imagen_offset_oveja, pos, frameon=False)
        ejes_animacion.add_artist(ab)
        
    return dispersión_ovejas, texto_cantidad_ovejas

animacion = FuncAnimation(figura_animacion, animar_ovejas, frames=len(solucion.t), init_func=iniciar_animacion, interval=1000, blit=True, repeat=False)


# Botón reinicio
ejes_boton_reiniciar = plt.axes([0.4, 0.01, 0.2, 0.05])  # [izquierda, abajo, ancho, alto]
boton_reiniciar = Button(ejes_boton_reiniciar, 'Reiniciar', color='blue', hovercolor='0.85')

def reiniciar(evento):
    global posiciones_ovejas
    posiciones_ovejas.clear()
    animacion.frame_seq = animacion.new_frame_seq()
    iniciar_animacion()
    figura_animacion.canvas.draw_idle()

boton_reiniciar.on_clicked(reiniciar)

plt.show()
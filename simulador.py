import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Parámetros
poblacion_inicial = 2
tiempo_total = 4

paso_meses = 6
paso_años = paso_meses / 12
tiempos = np.arange(0, tiempo_total + paso_años, paso_años)

comunidad_now = [poblacion_inicial]

#cada 6 meses, cada pareja tiene una cría
for t in tiempos[1:]:
    ovejas_actual = comunidad_now[-1]
    if ovejas_actual >= 2:
        parejas = ovejas_actual // 2

        nuevas_ovejas = parejas  # una cría por pareja cada 6 meses
        comunidad_now.append(ovejas_actual + nuevas_ovejas)
    else:
        comunidad_now.append(ovejas_actual)

# Gráfica tradicional
plt.figure()
plt.plot(tiempos, comunidad_now, marker='o', label="Crecimiento de las ovejas")
plt.xlabel("Años transcurridos")
plt.ylabel("Número de ovejas")
plt.title("Intervalos de 6 meses")
plt.grid(True)
plt.legend()

figura_animacion, ejes_animacion = plt.subplots()
ejes_animacion.set_xlim(0, 10)
ejes_animacion.set_ylim(0, 10)
ejes_animacion.set_title("Las ovejas reproduciéndose como locas")
ejes_animacion.set_xlabel("X")
ejes_animacion.set_ylabel("Y")

texto_cantidad_ovejas = ejes_animacion.text(
    0.98, 0.95, '',
    transform=ejes_animacion.transAxes,
    fontsize=12, color='black',
    ha='right', va='top',
    bbox=dict(facecolor='white', alpha=0.7)
)

posiciones_ovejas = []

# Carga la imagen de la oveja
laovejaquenopudeponerporincompatibilidadconlalibreriamatplotlib = "Jeb_Sheep_JE2.webp"
imagen_oveja = plt.imread("Sheep.png")
imagen_offset_oveja = OffsetImage(imagen_oveja, zoom=0.2)

def iniciar_animacion():
    texto_cantidad_ovejas.set_text('')
    for artist in ejes_animacion.artists[:]:
        artist.remove()
    return texto_cantidad_ovejas,

def animar_ovejas(indice):
    cantidad_ovejas = int(comunidad_now[indice])
    while len(posiciones_ovejas) < cantidad_ovejas:
        x, y = np.random.uniform(0, 10), np.random.uniform(0, 10)
        posiciones_ovejas.append([x, y])
    while len(posiciones_ovejas) > cantidad_ovejas:
        posiciones_ovejas.pop()
    texto_cantidad_ovejas.set_text(f'Ovejas: {cantidad_ovejas}\nTiempo: {tiempos[indice]:.2f} años')
    for artist in ejes_animacion.artists[:]:
        artist.remove()
    for pos in posiciones_ovejas:
        ab = AnnotationBbox(imagen_offset_oveja, pos, frameon=False)
        ejes_animacion.add_artist(ab)
    return texto_cantidad_ovejas,

animacion = FuncAnimation(
    figura_animacion,
    animar_ovejas,
    frames=len(tiempos),
    init_func=iniciar_animacion,
    interval=1000,
    blit=False,
    repeat=False
)

ejes_boton_reiniciar = plt.axes([0.4, 0.01, 0.2, 0.05])
boton_reiniciar = Button(ejes_boton_reiniciar, 'Reiniciar', color='blue', hovercolor='0.85')

def reiniciar(evento):
    global posiciones_ovejas
    posiciones_ovejas.clear()
    animacion.frame_seq = animacion.new_frame_seq()
    iniciar_animacion()
    figura_animacion.canvas.draw_idle()

boton_reiniciar.on_clicked(reiniciar)

plt.show()
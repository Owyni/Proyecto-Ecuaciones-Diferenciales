import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# Parámetros del modelo
r = 0.5     # tasa de spawn
d = 0.1     # tasa de despawn
M_max = 70  # cantidad máxima de mobs
M0 = 10     # mobs iniciales
area_size = 10  # tamaño del área cuadrada

# Estado inicial
mobs = [ (random.uniform(0, area_size), random.uniform(0, area_size)) for _ in range(M0) ]

# Configurar figura
fig, ax = plt.subplots()
sc = ax.scatter([], [], c='green')
ax.set_xlim(0, area_size)
ax.set_ylim(0, area_size)
ax.set_title('Simulación de Spawn de Mobs en Minecraft')
ax.set_xlabel('X')
ax.set_ylabel('Y')

def update(frame):
    global mobs

    M = len(mobs)

    # Cálculo de cantidad a spawnear y despawnear
    spawn_chance = r * (M_max - M)
    despawn_chance = d * M

    # Spawning
    new_mobs = []
    for _ in range(int(spawn_chance)):
        x, y = random.uniform(0, area_size), random.uniform(0, area_size)
        new_mobs.append((x, y))
    mobs.extend(new_mobs)

    # Despawning
    despawn_count = min(int(despawn_chance), len(mobs))
    mobs = random.sample(mobs, len(mobs) - despawn_count) if despawn_count < len(mobs) else []

    # Actualizar gráfico
    if mobs:
        x_vals, y_vals = zip(*mobs)
    else:
        x_vals, y_vals = [], []
    sc.set_offsets(np.column_stack([x_vals, y_vals]))
    ax.set_title(f'Tiempo: {frame} - Mobs: {len(mobs)}')
    return sc,

# Animación
ani = FuncAnimation(fig, update, frames=200, interval=200, blit=True)
plt.show()

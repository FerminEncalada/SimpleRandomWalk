import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np

class Visualizador:
    """
    Clase para visualizar el resultado de la simulación Random Walk.
    
    Crea gráficos que muestran el camino recorrido con el estilo de líneas
    conectadas similar a un laberinto.
    """
    
    @staticmethod
    def visualizar_camino_estatico(estadisticas, entorno):
        """
        Crea una visualización estática del camino completo recorrido.
        
        Args:
            estadisticas (dict): Diccionario con las estadísticas de la simulación
            entorno (Entorno): El entorno donde se realizó la simulación
        """
        camino = estadisticas['camino']
        pos_inicial = estadisticas['posicion_inicial']
        pos_final = estadisticas['posicion_final']
        
        fig, ax = plt.subplots(figsize=(14, 14))
        
        # Configurar límites
        ax.set_xlim(-1, entorno.ancho)
        ax.set_ylim(-1, entorno.alto)
        ax.set_aspect('equal')
        
        # Fondo blanco
        ax.set_facecolor('white')
        fig.patch.set_facecolor('white')
        
        # Ocultar grid por defecto
        ax.grid(False)
        
        # Dibujar camino como líneas conectadas (estilo imagen)
        if len(camino) > 1:
            xs = [pos[0] for pos in camino]
            ys = [pos[1] for pos in camino]
            
            # Líneas rojas conectadas
            ax.plot(xs, ys, 'r-', linewidth=2, solid_capstyle='projecting',
                   solid_joinstyle='miter')
        
        # Marcar posición inicial con círculo verde
        ax.plot(pos_inicial[0], pos_inicial[1], 'go', markersize=10,
               label='Inicio', zorder=5)
        
        # Marcar posición final con punto rojo más grande
        ax.plot(pos_final[0], pos_final[1], 'ro', markersize=8,
               label='Fin', zorder=5)
        
        # Etiquetas y título
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        ax.set_title('Simulación Random Walk 2D - Camino Completo\n' + 
                    f"Pasos: {estadisticas['pasos_realizados']} | " +
                    f"Bloqueados: {estadisticas['intentos_bloqueados']} | " +
                    f"Distancia final: {estadisticas['distancia_euclidiana']:.2f}",
                    fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper right')
        
        # Invertir eje Y para que (0,0) esté arriba a la izquierda
        ax.invert_yaxis()
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def visualizar_camino_animado(estadisticas, entorno, intervalo=50):
        """
        Crea una animación del camino recorrido paso a paso.
        
        Args:
            estadisticas (dict): Diccionario con las estadísticas de la simulación
            entorno (Entorno): El entorno donde se realizó la simulación
            intervalo (int): Milisegundos entre frames de la animación
        """
        camino = estadisticas['camino']
        pos_inicial = estadisticas['posicion_inicial']
        
        fig, ax = plt.subplots(figsize=(14, 14))
        
        # Configurar límites
        ax.set_xlim(-1, entorno.ancho)
        ax.set_ylim(-1, entorno.alto)
        ax.set_aspect('equal')
        
        # Fondo blanco
        ax.set_facecolor('white')
        fig.patch.set_facecolor('white')
        ax.grid(False)
        
        # Marcar posición inicial
        ax.plot(pos_inicial[0], pos_inicial[1], 'go', markersize=10,
               label='Inicio', zorder=5)
        
        # Invertir eje Y
        ax.invert_yaxis()
        
        # Elementos que se actualizarán
        line, = ax.plot([], [], 'r-', linewidth=2, solid_capstyle='projecting',
                       solid_joinstyle='miter')
        point, = ax.plot([], [], 'ro', markersize=8, zorder=5)
        
        # Etiquetas
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        titulo = ax.set_title('', fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper right')
        
        def init():
            line.set_data([], [])
            point.set_data([], [])
            return line, point, titulo
        
        def animate(frame):
            # Obtener camino hasta el frame actual
            camino_actual = camino[:frame+1]
            xs = [pos[0] for pos in camino_actual]
            ys = [pos[1] for pos in camino_actual]
            
            # Actualizar línea
            line.set_data(xs, ys)
            
            # Actualizar punto actual
            if len(camino_actual) > 0:
                point.set_data([xs[-1]], [ys[-1]])
            
            # Actualizar título con información de progreso
            progreso = (frame / len(camino)) * 100
            titulo.set_text(f'Simulación Random Walk 2D - Paso {frame}/{len(camino)-1}\n' +
                          f'Progreso: {progreso:.1f}% | Posición: ({xs[-1]}, {ys[-1]})')
            
            return line, point, titulo
        
        anim = FuncAnimation(fig, animate, init_func=init, frames=len(camino),
                           interval=intervalo, blit=True, repeat=False)
        
        plt.tight_layout()
        plt.show()
        
        return anim
    
    @staticmethod
    def mostrar_estadisticas(estadisticas):
        """
        Imprime las estadísticas de la simulación de forma formateada.
        
        Args:
            estadisticas (dict): Diccionario con las estadísticas
        """
        print("\n" + "="*70)
        print("📊 ESTADÍSTICAS DE LA SIMULACIÓN")
        print("="*70)
        print(f"✅ Pasos realizados:           {estadisticas['pasos_realizados']}")
        print(f"🚫 Intentos bloqueados:        {estadisticas['intentos_bloqueados']}")
        print(f"📍 Posición inicial:           {estadisticas['posicion_inicial']}")
        print(f"🎯 Posición final:             {estadisticas['posicion_final']}")
        print(f"📏 Distancia euclidiana:       {estadisticas['distancia_euclidiana']:.2f}")
        print(f"📐 Distancia Manhattan:        {estadisticas['distancia_manhattan']}")
        
        # Calcular eficiencia
        if estadisticas['pasos_realizados'] > 0:
            eficiencia = (estadisticas['pasos_realizados'] / 
                         (estadisticas['pasos_realizados'] + estadisticas['intentos_bloqueados'])) * 100
            print(f"⚡ Eficiencia:                 {eficiencia:.2f}%")
        
        print("="*70 + "\n")


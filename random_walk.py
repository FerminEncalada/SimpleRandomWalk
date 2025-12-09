import random

class RandomWalk:
    """
    Implementación del algoritmo Random Walk 2D con límites.
    
    El agente se mueve aleatoriamente en 4 direcciones (arriba, abajo,
    izquierda, derecha). Si un movimiento choca con las paredes, se
    descarta y se calcula uno nuevo hasta encontrar un movimiento válido.
    
    Attributes:
        entorno (Entorno): El entorno donde se ejecuta el Random Walk
        posicion_actual (tuple): Posición actual (x, y) del agente
        camino (list): Lista de todas las posiciones visitadas
        pasos_realizados (int): Contador de pasos válidos realizados
        intentos_bloqueados (int): Contador de intentos inválidos (choques)
    """
    
    # Direcciones posibles: arriba, abajo, izquierda, derecha
    DIRECCIONES = [
        (0, -1),   # Arriba
        (0, 1),    # Abajo
        (-1, 0),   # Izquierda
        (1, 0)     # Derecha
    ]
    
    NOMBRES_DIRECCIONES = {
        (0, -1): "Arriba",
        (0, 1): "Abajo",
        (-1, 0): "Izquierda",
        (1, 0): "Derecha"
    }
    
    def __init__(self, entorno):
        """
        Inicializa el Random Walk con un entorno dado.
        
        Args:
            entorno (Entorno): El entorno donde se ejecutará la simulación
        """
        self.entorno = entorno
        self.posicion_actual = entorno.pos_inicial
        self.camino = [self.posicion_actual]
        self.pasos_realizados = 0
        self.intentos_bloqueados = 0
    
    def _obtener_direccion_aleatoria(self):
        """
        Selecciona una dirección aleatoria de las 4 posibles.
        
        Returns:
            tuple: (dx, dy) representando el desplazamiento en X e Y
        """
        return random.choice(self.DIRECCIONES)
    
    def realizar_paso(self, max_intentos=1000, mostrar_info=False):
        """
        Realiza un paso válido en el Random Walk.
        
        Intenta mover el agente en una dirección aleatoria. Si el movimiento
        choca con las paredes, descarta ese movimiento y elige otra dirección
        aleatoria hasta encontrar un movimiento válido.
        
        Args:
            max_intentos (int): Número máximo de intentos para encontrar un
                              movimiento válido. Previene bucles infinitos.
            mostrar_info (bool): Si es True, muestra información de cada intento
        
        Returns:
            bool: True si se realizó un paso válido, False si no se encontró
                 ningún movimiento válido después de max_intentos
        """
        intentos_locales = 0
        
        while intentos_locales < max_intentos:
            # Obtener dirección aleatoria
            direccion = self._obtener_direccion_aleatoria()
            dx, dy = direccion
            
            # Calcular nueva posición
            nueva_x = self.posicion_actual[0] + dx
            nueva_y = self.posicion_actual[1] + dy
            
            # Verificar si el movimiento es válido
            if self.entorno.es_posicion_valida(nueva_x, nueva_y):
                # Movimiento válido - actualizar posición
                if mostrar_info:
                    print(f"  ✓ Movimiento válido: {self.NOMBRES_DIRECCIONES[direccion]} "
                          f"-> ({nueva_x}, {nueva_y})")
                
                self.posicion_actual = (nueva_x, nueva_y)
                self.camino.append(self.posicion_actual)
                self.pasos_realizados += 1
                return True
            else:
                # Movimiento inválido - contar intento bloqueado
                if mostrar_info:
                    print(f"  ✗ Movimiento bloqueado: {self.NOMBRES_DIRECCIONES[direccion]} "
                          f"(choque con pared)")
                
                self.intentos_bloqueados += 1
                intentos_locales += 1
        
        # No se encontró movimiento válido
        print(f"⚠ Advertencia: No se encontró movimiento válido después de {max_intentos} intentos")
        return False
    
    def simular(self, num_pasos, mostrar_progreso=True, mostrar_cada=10):
        """
        Ejecuta la simulación completa del Random Walk de forma gradual.
        
        Args:
            num_pasos (int): Número de pasos válidos a realizar
            mostrar_progreso (bool): Si es True, muestra el progreso gradualmente
            mostrar_cada (int): Mostrar información cada N pasos
            
        Returns:
            dict: Diccionario con estadísticas de la simulación
        """
        print("\n" + "="*70)
        print("INICIANDO SIMULACIÓN RANDOM WALK")
        print("="*70)
        print(f"📍 Posición inicial: {self.posicion_actual}")
        print(f"📏 Dimensiones del entorno: {self.entorno.obtener_dimensiones()}")
        print(f"🎯 Pasos a realizar: {num_pasos}")
        print("="*70 + "\n")
        
        for paso in range(num_pasos):
            if mostrar_progreso:
                print(f"\n🚶 Paso {paso + 1}/{num_pasos}")
                print(f"   Posición actual: {self.posicion_actual}")
            
            # Realizar paso mostrando intentos
            exito = self.realizar_paso(mostrar_info=mostrar_progreso)
            
            if not exito:
                print(f"\n⛔ Simulación detenida en el paso {paso + 1}")
                break
            
            # Mostrar progreso resumido cada N pasos
            if not mostrar_progreso and (paso + 1) % mostrar_cada == 0:
                progreso = (paso + 1) / num_pasos * 100
                print(f"⏳ Progreso: {paso + 1}/{num_pasos} pasos ({progreso:.1f}%) - "
                      f"Posición: {self.posicion_actual} - "
                      f"Bloqueados: {self.intentos_bloqueados}")
        
        print("\n" + "="*70)
        print("✅ SIMULACIÓN COMPLETADA")
        print("="*70 + "\n")
        
        return self.obtener_estadisticas()
    
    def obtener_estadisticas(self):
        """
        Obtiene estadísticas de la simulación actual.
        
        Returns:
            dict: Diccionario con las estadísticas
        """
        return {
            'pasos_realizados': self.pasos_realizados,
            'intentos_bloqueados': self.intentos_bloqueados,
            'posicion_inicial': self.entorno.pos_inicial,
            'posicion_final': self.posicion_actual,
            'camino': self.camino.copy(),
            'distancia_euclidiana': self._calcular_distancia_euclidiana(),
            'distancia_manhattan': self._calcular_distancia_manhattan()
        }
    
    def _calcular_distancia_euclidiana(self):
        """Calcula la distancia euclidiana desde el inicio hasta la posición actual."""
        x0, y0 = self.entorno.pos_inicial
        x1, y1 = self.posicion_actual
        return ((x1 - x0)**2 + (y1 - y0)**2)**0.5
    
    def _calcular_distancia_manhattan(self):
        """Calcula la distancia Manhattan desde el inicio hasta la posición actual."""
        x0, y0 = self.entorno.pos_inicial
        x1, y1 = self.posicion_actual
        return abs(x1 - x0) + abs(y1 - y0)
    
    def reiniciar(self):
        """
        Reinicia la simulación a su estado inicial.
        """
        self.posicion_actual = self.entorno.pos_inicial
        self.camino = [self.posicion_actual]
        self.pasos_realizados = 0
        self.intentos_bloqueados = 0

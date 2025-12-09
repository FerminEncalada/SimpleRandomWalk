class Entorno:
    """
    Clase que representa el entorno delimitado por paredes donde se realiza
    el Random Walk.
    
    Attributes:
        ancho (int): Ancho del entorno (número de celdas en X)
        alto (int): Alto del entorno (número de celdas en Y)
        pos_inicial (tuple): Posición inicial (x, y) del agente
    """
    
    def __init__(self, ancho=100, alto=100, pos_inicial=None):
        """
        Inicializa el entorno con dimensiones específicas.
        
        Args:
            ancho (int): Ancho del entorno. Default: 100
            alto (int): Alto del entorno. Default: 100
            pos_inicial (tuple): Posición inicial (x, y). Si es None, se coloca
                               en el centro del entorno.
        """
        self.ancho = ancho
        self.alto = alto
        
        if pos_inicial is None:
            self.pos_inicial = (ancho // 2, alto // 2)
        else:
            self.pos_inicial = pos_inicial
    
    def es_posicion_valida(self, x, y):
        """
        Verifica si una posición está dentro de los límites del entorno.
        
        Args:
            x (int): Coordenada X
            y (int): Coordenada Y
            
        Returns:
            bool: True si la posición es válida, False si choca con las paredes
        """
        return 0 <= x < self.ancho and 0 <= y < self.alto
    
    def obtener_dimensiones(self):
        """
        Retorna las dimensiones del entorno.
        
        Returns:
            tuple: (ancho, alto)
        """
        return (self.ancho, self.alto)

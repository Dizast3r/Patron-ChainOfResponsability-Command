import pygame
import random
from Entidades import Jugador, Obstaculo
from Handlers import HandlerMoverDerecha, HandlerMoverIzquierda, HandlerSalir, HandlerColisiones, HandlerPuntaje
from Comandos import ComandoMoverDerecha, ComandoMoverIzquierda

class Juego:
    def __init__(self):
        # Inicializar pygame
        pygame.init()
        
        # Configuración de la ventana
        self.ANCHO_VENTANA = 800
        self.ALTO_VENTANA = 600
        self.pantalla = pygame.display.set_mode((self.ANCHO_VENTANA, self.ALTO_VENTANA))
        pygame.display.set_caption("Juego de Carriles")
        
        # Configuración de carriles
        self.desplazamientoX = self.ANCHO_VENTANA // 4  # Ancho de un carril
        self.carriles = self._calcularCarriles()
        
        # Crear jugador en el carril izquierdo (carril 0)
        posicion_inicial_x = self.carriles[0]
        posicion_inicial_y = self.ALTO_VENTANA - 100
        self.jugador = Jugador(
            "Assets/jugador.png",
            posicion_inicial_x,
            posicion_inicial_y,
            self.desplazamientoX,
            self.ANCHO_VENTANA,
            velocidadY=0  # El jugador no se mueve verticalmente
        )
        
        # Lista de obstáculos (Sustitución de Liskov: Obstaculo es subtipo de Entidad)
        self.vehiculos = []
        
        # Mapeo de comandos
        self.comandos = {
            pygame.K_RIGHT: ComandoMoverDerecha(),
            pygame.K_LEFT: ComandoMoverIzquierda()
        }
        
        # Configurar cadena de handlers de entrada
        self.handlerMoverDerecha = HandlerMoverDerecha(self.comandos)
        self.handlerMoverIzquierda = HandlerMoverIzquierda(self.comandos)
        self.handlerSalir = HandlerSalir(self.comandos)
        
        self.handlerMoverDerecha.SetSucesor(self.handlerMoverIzquierda)
        self.handlerMoverIzquierda.SetSucesor(self.handlerSalir)
        
        # Configurar cadena de handlers de eventos
        self.handlerColisiones = HandlerColisiones()
        self.handlerPuntaje = HandlerPuntaje()
        
        self.handlerColisiones.SetSucesor(self.handlerPuntaje)
        
        # Control del juego
        self.corriendo = True
        self.reloj = pygame.time.Clock()
        self.FPS = 60
        
        # Control de aparición de obstáculos
        self.tiempo_ultimo_obstaculo = 0
        self.intervalo_obstaculos = 2000  # Milisegundos (2 segundos)
        
        # Fuente para el puntaje
        self.fuente = pygame.font.Font(None, 36)
        
    def _calcularCarriles(self):
        """Calcula las posiciones centrales de los 4 carriles"""
        ancho_carril = self.ANCHO_VENTANA // 4
        return [
            ancho_carril // 2,                      # Carril 0 (izquierda)
            ancho_carril + ancho_carril // 2,       # Carril 1
            2 * ancho_carril + ancho_carril // 2,   # Carril 2
            3 * ancho_carril + ancho_carril // 2    # Carril 3 (derecha)
        ]
    
    def _crearObstaculo(self):
        """Crea un obstáculo en un carril aleatorio en la parte superior"""
        carril_aleatorio = random.randint(0, 3)
        posicion_x = self.carriles[carril_aleatorio]
        posicion_y = -50  # Aparece fuera de la pantalla en la parte superior
        
        # Elegir imagen aleatoria de carro
        imagen_carro = f"Assets/carro{random.randint(1, 3)}.png"
        
        # Sustitución de Liskov: Obstaculo puede usarse como Entidad
        obstaculo = Obstaculo(imagen_carro, posicion_x, posicion_y, velocidadY=5)
        self.vehiculos.append(obstaculo)
    
    def _actualizarObstaculos(self):
        """Actualiza la posición de los obstáculos y elimina los que salen de pantalla"""
        for obstaculo in self.vehiculos[:]:
            obstaculo.Update()
            # Eliminar obstáculos que salieron de la pantalla
            if obstaculo.GetRect().y > self.ALTO_VENTANA:
                self.vehiculos.remove(obstaculo)
    
    def _dibujar(self):
        """Dibuja todos los elementos en la pantalla"""
        # Fondo
        self.pantalla.fill((50, 50, 50))  # Gris oscuro (carretera)
        
        # Dibujar líneas de carriles
        for i in range(1, 4):
            pygame.draw.line(
                self.pantalla,
                (255, 255, 255),
                (i * self.desplazamientoX, 0),
                (i * self.desplazamientoX, self.ALTO_VENTANA),
                2
            )
        
        # Dibujar jugador
        self.jugador.Draw(self.pantalla)
        
        # Dibujar obstáculos
        for obstaculo in self.vehiculos:
            obstaculo.Draw(self.pantalla)
        
        # Dibujar puntaje
        texto_puntaje = self.fuente.render(f"Puntaje: {self.jugador.GetPuntaje()}", True, (255, 255, 255))
        self.pantalla.blit(texto_puntaje, (10, 10))
        
        pygame.display.flip()
    
    def perder(self):
        """Se ejecuta cuando el jugador pierde"""
        print(f"¡Juego terminado! Puntaje final: {self.jugador.GetPuntaje()}")
        self.corriendo = False
    
    def run(self):
        """Loop principal del juego"""
        while self.corriendo:
            tiempo_actual = pygame.time.get_ticks()
            
            # Manejar eventos de entrada (Cadena 1)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.corriendo = False
                self.handlerMoverDerecha.manejarEntrada(evento, self)
            
            # Crear obstáculos periódicamente
            if tiempo_actual - self.tiempo_ultimo_obstaculo > self.intervalo_obstaculos:
                self._crearObstaculo()
                self.tiempo_ultimo_obstaculo = tiempo_actual
            
            # Actualizar obstáculos
            self._actualizarObstaculos()
            
            # Manejar eventos del juego (Cadena 2: Colisiones y Puntaje)
            self.handlerColisiones.manejarEvento(self)
            
            # Dibujar todo
            self._dibujar()
            
            # Controlar FPS
            self.reloj.tick(self.FPS)
        
        pygame.quit()



if __name__ == "__main__":
    juego = Juego()
    juego.run()
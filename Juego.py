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
        pygame.display.set_caption("Patron Chain of Responsability / Command")
        
        # Estado del juego
        self.estado = "jugando"  # "jugando" o "game_over"
        
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
        self.velocidad_obstaculos = 5  # Velocidad inicial
        self.tiempo_inicio = pygame.time.get_ticks()
        
        # Fuentes
        self.fuente = pygame.font.Font(None, 36)
        self.fuente_grande = pygame.font.Font(None, 72)
        self.fuente_mediana = pygame.font.Font(None, 48)
        
        # Botones para Game Over
        self.boton_reintentar = pygame.Rect(self.ANCHO_VENTANA // 2 - 150, 350, 300, 60)
        self.boton_salir = pygame.Rect(self.ANCHO_VENTANA // 2 - 150, 430, 300, 60)
        
    def _calcularCarriles(self):
        """Calcula las posiciones centrales de los 4 carriles"""
        ancho_carril = self.ANCHO_VENTANA // 4
        return [
            ancho_carril // 2,                      # Carril 0 (izquierda)
            ancho_carril + ancho_carril // 2,       # Carril 1
            2 * ancho_carril + ancho_carril // 2,   # Carril 2
            3 * ancho_carril + ancho_carril // 2    # Carril 3 (derecha)
        ]
    
    def _actualizarVelocidadObstaculos(self):
        """Aumenta la velocidad de los obstáculos con el tiempo"""
        tiempo_transcurrido = (pygame.time.get_ticks() - self.tiempo_inicio) // 1000  # Segundos
        # Aumenta 0.5 de velocidad cada 10 segundos
        self.velocidad_obstaculos = 5 + (tiempo_transcurrido // 10) * 0.5
    
    def _crearObstaculo(self):
        """Crea un obstáculo en un carril aleatorio en la parte superior"""
        carril_aleatorio = random.randint(0, 3)
        posicion_x = self.carriles[carril_aleatorio]
        posicion_y = -50  # Aparece fuera de la pantalla en la parte superior
        
        # Elegir imagen aleatoria de carro
        imagen_carro = f"Assets/carro{random.randint(1, 3)}.png"
        
        # Sustitución de Liskov: Obstaculo puede usarse como Entidad
        obstaculo = Obstaculo(imagen_carro, posicion_x, posicion_y, velocidadY=self.velocidad_obstaculos)
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
        
        # Dibujar velocidad actual
        texto_velocidad = self.fuente.render(f"Velocidad: {self.velocidad_obstaculos:.1f}", True, (255, 255, 255))
        self.pantalla.blit(texto_velocidad, (10, 50))
        
        pygame.display.flip()
    
    def _dibujarGameOver(self):
        """Dibuja la pantalla de Game Over"""
        # Fondo semi-transparente
        overlay = pygame.Surface((self.ANCHO_VENTANA, self.ALTO_VENTANA))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.pantalla.blit(overlay, (0, 0))
        
        # Texto "PERDISTE"
        texto_perdiste = self.fuente_grande.render("PERDISTE", True, (255, 50, 50))
        rect_perdiste = texto_perdiste.get_rect(center=(self.ANCHO_VENTANA // 2, 150))
        self.pantalla.blit(texto_perdiste, rect_perdiste)
        
        # Texto de puntuación
        texto_puntuacion = self.fuente_mediana.render(f"Puntuación: {self.jugador.GetPuntaje()}", True, (255, 255, 255))
        rect_puntuacion = texto_puntuacion.get_rect(center=(self.ANCHO_VENTANA // 2, 250))
        self.pantalla.blit(texto_puntuacion, rect_puntuacion)
        
        # Obtener posición del mouse
        mouse_pos = pygame.mouse.get_pos()
        
        # Botón Reintentar
        color_reintentar = (0, 200, 0) if self.boton_reintentar.collidepoint(mouse_pos) else (0, 150, 0)
        pygame.draw.rect(self.pantalla, color_reintentar, self.boton_reintentar, border_radius=10)
        pygame.draw.rect(self.pantalla, (255, 255, 255), self.boton_reintentar, 3, border_radius=10)
        texto_reintentar = self.fuente.render("REINTENTAR", True, (255, 255, 255))
        rect_texto_reintentar = texto_reintentar.get_rect(center=self.boton_reintentar.center)
        self.pantalla.blit(texto_reintentar, rect_texto_reintentar)
        
        # Botón Salir
        color_salir = (200, 0, 0) if self.boton_salir.collidepoint(mouse_pos) else (150, 0, 0)
        pygame.draw.rect(self.pantalla, color_salir, self.boton_salir, border_radius=10)
        pygame.draw.rect(self.pantalla, (255, 255, 255), self.boton_salir, 3, border_radius=10)
        texto_salir = self.fuente.render("SALIR", True, (255, 255, 255))
        rect_texto_salir = texto_salir.get_rect(center=self.boton_salir.center)
        self.pantalla.blit(texto_salir, rect_texto_salir)
        
        pygame.display.flip()
    
    def _manejarClickGameOver(self, pos):
        """Maneja los clicks en la pantalla de Game Over"""
        if self.boton_reintentar.collidepoint(pos):
            self._reiniciarJuego()
        elif self.boton_salir.collidepoint(pos):
            self.corriendo = False
    
    def _reiniciarJuego(self):
        """Reinicia el juego"""
        # Reiniciar jugador
        posicion_inicial_x = self.carriles[0]
        posicion_inicial_y = self.ALTO_VENTANA - 100
        self.jugador = Jugador(
            "Assets/jugador.png",
            posicion_inicial_x,
            posicion_inicial_y,
            self.desplazamientoX,
            self.ANCHO_VENTANA,
            velocidadY=0
        )
        
        # Limpiar obstáculos
        self.vehiculos = []
        
        # Reiniciar tiempos y velocidades
        self.tiempo_ultimo_obstaculo = 0
        self.velocidad_obstaculos = 5
        self.tiempo_inicio = pygame.time.get_ticks()
        
        # Cambiar estado
        self.estado = "jugando"
    
    def perder(self):
        """Se ejecuta cuando el jugador pierde"""
        print(f"¡Juego terminado! Puntaje final: {self.jugador.GetPuntaje()}")
        self.estado = "game_over"
    
    def run(self):
        """Loop principal del juego"""
        while self.corriendo:
            if self.estado == "jugando":
                tiempo_actual = pygame.time.get_ticks()
                
                # Manejar eventos de entrada (Cadena 1)
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        self.corriendo = False
                    self.handlerMoverDerecha.manejarEntrada(evento, self)
                
                # Actualizar velocidad de obstáculos
                self._actualizarVelocidadObstaculos()
                
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
            
            elif self.estado == "game_over":
                # Manejar eventos en Game Over
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        self.corriendo = False
                    elif evento.type == pygame.MOUSEBUTTONDOWN:
                        self._manejarClickGameOver(evento.pos)
                
                # Dibujar pantalla de Game Over
                self._dibujarGameOver()
            
            # Controlar FPS
            self.reloj.tick(self.FPS)
        
        pygame.quit()



if __name__ == "__main__":
    juego = Juego()
    juego.run()
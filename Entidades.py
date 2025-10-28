import pygame
import Comandos

class Entidad:
    def __init__(self, imagenRuta: str, x: int, y: int, velocidadY: float = 5.0):
        self.__imagen = pygame.image.load(imagenRuta).convert_alpha()
        self.__rect = self.__imagen.get_rect(center=(x, y))
        self.__velocidadY = velocidadY
        self.__velocidadX = 0

    def GetImagen(self):
        return self.__imagen

    def GetRect(self):
        return self.__rect

    def GetPosicion(self):
        return (self.__rect.x, self.__rect.y)

    def SetPosicion(self, x: int, y: int):
        self.__rect.x = x
        self.__rect.y = y

    def GetVelocidadY(self):
        return self.__velocidadY

    def SetVelocidadY(self, v: float):
        self.__velocidadY = v

    def GetVelocidadX(self):
        return self.__velocidadX

    def SetVelocidadX(self, v: float):
        self.__velocidadX = v

    def Update(self):
        self.__rect.y += self.__velocidadY

    def Draw(self, pantalla: pygame.Surface):
        pantalla.blit(self.__imagen, self.__rect)

    def ColisionaCon(self, Entidad):
        return self.__rect.colliderect(Entidad.GetRect())


class Jugador(Entidad):
    def __init__(self, imagenRuta: str, x: int, y: int, desplazamientoX: int, anchoVentana: int, velocidadY: float = 5.0):
        super().__init__(imagenRuta, x, y, velocidadY)
        self.__puntaje = 0
        self.__desplazamientoX = desplazamientoX
        self.__anchoVentana = anchoVentana

    def GetPuntaje(self):
        return self.__puntaje
    
    def SetPuntaje(self, puntaje: int):
        self.__puntaje = puntaje
    
    def MoverDerecha(self):
        rect = self.GetRect()
        nueva_posicion = rect.x + self.__desplazamientoX
        
        # Validar que no se salga de la ventana (considerando el ancho del carro)
        if nueva_posicion + rect.width <= self.__anchoVentana:
            rect.x = nueva_posicion

    def MoverIzquierda(self):
        rect = self.GetRect()
        nueva_posicion = rect.x - self.__desplazamientoX
        
        # Validar que no se salga de la ventana
        if nueva_posicion >= 0:
            rect.x = nueva_posicion

class Obstaculo(Entidad):
    def __init__(self, imagenRuta, x, y, velocidadY = 5):
        super().__init__(imagenRuta, x, y, velocidadY)

    def Update(self):
        super().Update()
import pygame

#Cadena 1: Relaciona con todos los inputs
class HandlerEntradas:
    def __init__(self):
        self.__sucesor__ = None
    
    def SetSucesor(self, sucesor):
        self.__sucesor__ = sucesor

    def manejarEntrada(self, opcion, juego):
        pass

#Maneja los eventos del juego (no se relaciona en nada, con las teclas presionadas)
class HandlerEventos:
    def __init__(self):
        self.__sucesor__ = None
    
    def SetSucesor(self, sucesor):
        self.__sucesor__ = sucesor

    def manejarEvento(self, juego):
        pass

#Handler 1 de la cadena de entradas
class HandlerMoverDerecha(HandlerEntradas):

    def __init__(self, comandos = None):
        super().__init__()
        self.comandos = comandos
    

    def manejarEntrada(self, opcion, juego):
        if opcion.type == pygame.KEYDOWN:
            if opcion.key == pygame.K_RIGHT:
                self.comandos[pygame.K_RIGHT].Ejecutar(juego.jugador)
                return
            
        if self.__sucesor__:
            self.__sucesor__.manejarEntrada(opcion, juego)

#Handler 2 de la cadena de entradas
class HandlerMoverIzquierda(HandlerEntradas):

    def __init__(self, comandos = None):
        super().__init__()
        self.comandos = comandos
    

    def manejarEntrada(self, opcion, juego):
        if opcion.type == pygame.KEYDOWN:
            if opcion.key == pygame.K_LEFT:
                self.comandos[pygame.K_LEFT].Ejecutar(juego.jugador)
                return

        if self.__sucesor__:
            self.__sucesor__.manejarEntrada(opcion, juego)

#Ultimo handler de la cadena de entradas
class HandlerSalir(HandlerEntradas):

    def __init__(self, comandos = None):
        super().__init__()
        self.comandos = comandos
    

    def manejarEntrada(self, opcion, juego):
        if opcion.type == pygame.KEYDOWN:
            if opcion.key == pygame.K_ESCAPE:
                juego.corriendo = False
                return

        #se detendria aca la cadena de entradas
        if self.__sucesor__:
            self.__sucesor__.manejarEntrada(opcion, juego)

#Handler 1 de la cadena de eventos
class HandlerColisiones(HandlerEventos):
    def manejarEvento(self, juego):
        for carro in juego.vehiculos:
            if juego.jugador.ColisionaCon(carro):
                juego.perder()
                return
        if self.__sucesor__:
            self.__sucesor__.manejarEvento(juego)

#Este deberia ser el handler por defecto de la cadena de eventos, ya que el jugador va avanzando sin chocarse, se van sumando punticos
class HandlerPuntaje(HandlerEventos):
    def manejarEvento(self, juego):
        juego.jugador.SetPuntaje(juego.jugador.GetPuntaje() + 1)

        if self.__sucesor__:
            self.__sucesor__.manejarEvento(juego)


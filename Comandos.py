class Comando:
    def Ejecutar(self, jugador):
        pass

class ComandoMoverDerecha(Comando):
    def Ejecutar(self, jugador):
        jugador.MoverDerecha()
    

class ComandoMoverIzquierda(Comando):
    def Ejecutar(self, jugador):
        jugador.MoverIzquierda()


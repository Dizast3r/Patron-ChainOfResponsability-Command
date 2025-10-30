# Juego de Carriles - Patrones de Diseño

Juego de autos desarrollado en Pygame que implementa los patrones **Command** y **Chain of Responsibility** para gestionar la entrada del usuario y la lógica del juego.

<img width="1972" height="592" alt="image" src="https://github.com/user-attachments/assets/e2761244-440f-4924-8b6a-213762d96932" />

---

## 🎮 Descripción del Juego

El jugador controla un auto que se desplaza entre 4 carriles en una autopista. Los obstáculos (otros autos) aparecen aleatoriamente en la parte superior de la pantalla y se mueven hacia abajo con velocidad creciente. El objetivo es esquivar los obstáculos el mayor tiempo posible para acumular puntos.

### Características:
- **4 carriles** distribuidos equitativamente en la pantalla
- **Dificultad progresiva**: Los obstáculos aumentan su velocidad cada 10 segundos
- **Sistema de puntuación** basado en el tiempo sobrevivido
- **Pantalla de Game Over** con opciones de reintentar o salir
- **Controles simples**: Flechas izquierda/derecha para cambiar de carril, ESC para salir

---

## 🏗️ Patrones de Diseño Implementados

### 1. **Patrón Command** 

#### ¿Dónde se utiliza?
En el módulo `Comandos.py` para encapsular las acciones del jugador.

#### ¿Cómo se aplica?
```python
class Comando:
    def Ejecutar(self, jugador):
        pass

class ComandoMoverDerecha(Comando):
    def Ejecutar(self, jugador):
        jugador.MoverDerecha()

class ComandoMoverIzquierda(Comando):
    def Ejecutar(self, jugador):
        jugador.MoverIzquierda()
```

#### Ventajas en el proyecto:
- **Desacoplamiento**: La lógica de entrada (handlers) no depende directamente de los métodos del jugador
- **Extensibilidad**: Es fácil agregar nuevos comandos (saltar, disparar, etc.) sin modificar el código existente
- **Configurabilidad**: El mapeo de teclas a comandos se define en un diccionario, permitiendo cambiar controles fácilmente

#### Implementación en Game.py:
```python
self.comandos = {
    pygame.K_RIGHT: ComandoMoverDerecha(),
    pygame.K_LEFT: ComandoMoverIzquierda()
}
```

---

### 2. **Patrón Chain of Responsibility**

#### ¿Dónde se utiliza?
En el módulo `Handlers.py` para procesar eventos de entrada y lógica del juego.

#### ¿Cómo se aplica?

**Cadena 1: Manejo de Entradas del Usuario**
```
HandlerMoverDerecha → HandlerMoverIzquierda → HandlerSalir
```

Cada handler verifica si puede procesar el evento (tecla presionada). Si no puede, lo pasa al siguiente handler en la cadena.

```python
class HandlerMoverDerecha(HandlerEntradas):
    def manejarEntrada(self, opcion, juego):
        if opcion.type == pygame.KEYDOWN:
            if opcion.key == pygame.K_RIGHT:
                self.comandos[pygame.K_RIGHT].Ejecutar(juego.jugador)
                return  # Detiene la cadena
        
        # Si no procesó el evento, lo pasa al siguiente
        if self.__sucesor__:
            self.__sucesor__.manejarEntrada(opcion, juego)
```

**Cadena 2: Lógica del Juego (ejecutada cada frame)**
```
HandlerColisiones → HandlerPuntuaje
```

Esta cadena procesa la lógica del juego en cada frame:
1. **HandlerColisiones**: Verifica si hay colisiones. Si hay, termina el juego y detiene la cadena.
2. **HandlerPuntuaje**: Si no hay colisiones, suma puntos al jugador.

```python
class HandlerColisiones(HandlerEventos):
    def manejarEvento(self, juego):
        for carro in juego.vehiculos:
            if juego.jugador.ColisionaCon(carro):
                juego.perder()
                return  # Detiene la cadena (no suma puntos)
        
        # Solo continúa si NO hubo colisión
        if self.__sucesor__:
            self.__sucesor__.manejarEvento(juego)
```

#### Ventajas en el proyecto:
- **Separación de responsabilidades**: Cada handler tiene una única tarea específica
- **Flexibilidad**: Es fácil agregar, quitar o reordenar handlers sin afectar el resto del código
- **Lógica secuencial clara**: El flujo de procesamiento es explícito y fácil de seguir
- **Dos cadenas independientes**: Una para eventos de usuario y otra para lógica del juego

---

## 📁 Estructura del Proyecto

```
ChainOfResponsability-Command/
│
├── Juego.py              # Clase Game - Loop principal y lógica del juego
├── Entidades.py          # Clases Entidad, Jugador, Obstaculo
├── Comandos.py           # Patrón Command - Comandos de movimiento
├── Handlers.py           # Patrón Chain of Responsibility - Handlers
├── jugador.png           # Sprite del jugador
├── carro1.png            # Sprite de obstáculo 1
├── carro2.png            # Sprite de obstáculo 2
├── carro3.png            # Sprite de obstáculo 3
└── README.md
```

---

## 🚀 Cómo Ejecutar

### Requisitos:
- Python 3.7+
- Pygame

### Instalación de dependencias:
```bash
pip install pygame
```

### Ejecución:
```bash
python Juego.py
```

---

## 🎯 Controles

| Tecla | Acción |
|-------|--------|
| ⬅️ Flecha Izquierda | Mover al carril izquierdo |
| ➡️ Flecha Derecha | Mover al carril derecho |
| ESC | Salir del juego |

---

## 📊 Diagrama UML

<img width="1972" height="592" alt="image" src="https://github.com/user-attachments/assets/e2761244-440f-4924-8b6a-213762d96932" />

---

## 👥 Autores

- **Ladi Yolima Martínez Quiñones** — 20231020197  
- **Juan Esteban Ariza Ortiz** — 20241020005  
- **Jorge Miguel Méndez Barón** — 20241020030

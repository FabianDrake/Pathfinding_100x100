import tkinter as tk
from tkinter import messagebox
import heapq

# Definimos la clase Nodo para el algoritmo A*
class Nodo:
    def __init__(self, x, y, costo=0, heuristica=0, padre=None):
        self.x = x
        self.y = y
        self.costo = costo
        self.heuristica = heuristica
        self.padre = padre

    def __lt__(self, otro):
        return (self.costo + self.heuristica) < (otro.costo + otro.heuristica)

# Función para calcular la heurística de Manhattan
def heuristica_manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

# Implementación del algoritmo A*
def a_star(inicio, objetivo, mapa):
    filas = len(mapa)
    columnas = len(mapa[0])
    abiertos = []
    cerrados = set()
    inicio_nodo = Nodo(inicio[0], inicio[1], costo=0, heuristica=heuristica_manhattan(*inicio, *objetivo))
    heapq.heappush(abiertos, inicio_nodo)

    while abiertos:
        nodo_actual = heapq.heappop(abiertos)
        if (nodo_actual.x, nodo_actual.y) == objetivo:
            camino = []
            while nodo_actual:
                camino.append((nodo_actual.x, nodo_actual.y))
                nodo_actual = nodo_actual.padre
            return camino[::-1]
        
        cerrados.add((nodo_actual.x, nodo_actual.y))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x_vecino, y_vecino = nodo_actual.x + dx, nodo_actual.y + dy
            if (0 <= x_vecino < filas and 0 <= y_vecino < columnas and (x_vecino, y_vecino) not in cerrados and mapa[x_vecino][y_vecino] == 0):
                nuevo_costo = nodo_actual.costo + 1
                heuristica = heuristica_manhattan(x_vecino, y_vecino, *objetivo)
                vecino_nodo = Nodo(x_vecino, y_vecino, costo=nuevo_costo, heuristica=heuristica, padre=nodo_actual)
                heapq.heappush(abiertos, vecino_nodo)
    return None

# Clase principal de la aplicación
class PathfindingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pathfinding A* - Matriz 100x100")
        self.centrar_ventana(850, 950)
        self.mapa = [[0 for _ in range(100)] for _ in range(100)]
        self.inicio = None
        self.objetivo = None
        self.crear_interfaz()
        self.arrastrando = False  # Para detectar si el mouse está arrastrando

    def centrar_ventana(self, ancho, alto):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - ancho) // 2
        y = (screen_height - alto) // 2
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_interfaz(self):
        frame_canvas = tk.Frame(self.root)
        frame_canvas.pack(pady=10)

        self.canvas = tk.Canvas(frame_canvas, width=800, height=800, bg="white")
        self.canvas.grid(row=0, column=0)

        self.dibujar_matriz()

        # Vincular eventos de mouse
        self.canvas.bind("<Button-1>", self.seleccionar_celda)
        self.canvas.bind("<B1-Motion>", self.arrastrar_celda)
        self.canvas.bind("<ButtonRelease-1>", self.liberar_mouse)

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Iniciar Pathfinding", command=self.iniciar_pathfinding).pack()

    def dibujar_matriz(self):
        self.rectangulos = []
        for i in range(100):
            fila = []
            for j in range(100):
                x1 = j * 8
                y1 = i * 8
                x2 = x1 + 8
                y2 = y1 + 8
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="gray")
                fila.append(rect)
            self.rectangulos.append(fila)

    def seleccionar_celda(self, event):
        x, y = event.x // 8, event.y // 8
        self.actualizar_celda(x, y)

    def arrastrar_celda(self, event):
        x, y = event.x // 8, event.y // 8
        self.actualizar_celda(x, y)

    def liberar_mouse(self, event):
        self.arrastrando = False

    def actualizar_celda(self, x, y):
        if 0 <= x < 100 and 0 <= y < 100:
            if self.inicio is None:
                self.inicio = (y, x)
                self.canvas.itemconfig(self.rectangulos[y][x], fill="green")
            elif self.objetivo is None:
                self.objetivo = (y, x)
                self.canvas.itemconfig(self.rectangulos[y][x], fill="red")
            else:
                self.mapa[y][x] = 1
                self.canvas.itemconfig(self.rectangulos[y][x], fill="black")

    def iniciar_pathfinding(self):
        if not self.inicio or not self.objetivo:
            messagebox.showwarning("Advertencia", "Por favor selecciona un punto de inicio y un objetivo.")
            return

        camino = a_star(self.inicio, self.objetivo, self.mapa)
        if camino:
            for y, x in camino:
                if (y, x) != self.inicio and (y, x) != self.objetivo:
                    self.canvas.itemconfig(self.rectangulos[y][x], fill="blue")
        else:
            messagebox.showinfo("Sin camino", "No se encontró un camino entre los puntos seleccionados.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PathfindingApp(root)
    root.mainloop()

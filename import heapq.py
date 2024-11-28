import heapq
from collections import deque 
import time
import networkx as nx
import matplotlib.pyplot as plt

# Mapa del desierto con consecuencias variadas y pesos en las rutas
mapa_intrincado = {
    "Arrakeen": {"vecinos": [("Sietch Tabr", 3), ("Oasis del Norte", 2), ("Campamento Fremen", 4)], "consecuencia": "neutral"},
    "Sietch Tabr": {"vecinos": [("Arrakeen", 3), ("Oasis del Este", 5), ("Montaña de la Especia", 6)], "consecuencia": "neutral"},
    "Oasis del Norte": {"vecinos": [("Arrakeen", 2), ("Campamento Fremen", 1)], "consecuencia": "recompensa"},
    "Campamento Fremen": {"vecinos": [("Arrakeen", 4), ("Oasis del Norte", 1), ("Oasis del Este", 3)], "consecuencia": "energía limitada"},
    "Oasis del Este": {"vecinos": [("Sietch Tabr", 5), ("Campamento Fremen", 3), ("Zona Peligrosa", 7)], "consecuencia": "recurso"},
    "Montaña de la Especia": {"vecinos": [("Sietch Tabr", 6), ("Zona Peligrosa", 8)], "consecuencia": "recurso"},
    "Zona Peligrosa": {"vecinos": [("Oasis del Este", 7), ("Montaña de la Especia", 8)], "consecuencia": "muerte"},
}

# 1. Verificar conectividad del grafo
def es_conexo(mapa):
    def dfs(nodo, visitados):
        visitados.add(nodo)
        for vecino, _ in mapa[nodo]["vecinos"]:
            if vecino not in visitados:
                dfs(vecino, visitados)
    
    visitados = set()
    dfs(list(mapa.keys())[0], visitados)
    return len(visitados) == len(mapa)

# 2. Algoritmo de Dijkstra para encontrar el camino de menor costo
def dijkstra_camino_minimo(mapa, origen, destino):
    # Cola de prioridad para explorar nodos (costo acumulado, nodo actual, camino)
    cola = [(0, origen, [])]
    visitados = set()

    while cola:
        costo_actual, nodo_actual, camino = heapq.heappop(cola)

        # Si llegamos al destino, devolvemos el camino y el costo total
        if nodo_actual == destino:
            return camino + [nodo_actual], costo_actual

        # Ignorar nodos visitados
        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)

        # Procesar vecinos
        for vecino, peso in mapa[nodo_actual]["vecinos"]:
            if vecino not in visitados:
                heapq.heappush(cola, (costo_actual + peso, vecino, camino + [nodo_actual]))

    return None, float('inf')  # Si no hay camino

# 3. Analizar rutas considerando consecuencias
def bfs_rutas_alternativas(mapa, origen, destino):
    cola = deque([(origen, [origen], [], 100, 0)])  # (nodo_actual, camino, recursos, energía, recompensas)
    rutas = []

    while cola:
        nodo_actual, camino, recursos, energia, recompensas = cola.popleft()

        # Si llegamos al destino, guardamos la ruta
        if nodo_actual == destino:
            rutas.append((camino, recursos, energia, recompensas))
            continue

        # Consecuencias del nodo
        if mapa[nodo_actual]["consecuencia"] == "muerte":
            continue
        if mapa[nodo_actual]["consecuencia"] == "recurso":
            recursos.append(nodo_actual)
        if mapa[nodo_actual]["consecuencia"] == "energía limitada":
            energia -= 10
        if mapa[nodo_actual]["consecuencia"] == "recompensa":
            recompensas += 20

        # Si energía es insuficiente, detener el camino
        if energia <= 0:
            continue

        # Explorar vecinos
        for vecino, _ in mapa[nodo_actual]["vecinos"]:
            if vecino not in camino:  # Evitar ciclos
                cola.append((vecino, camino + [vecino], list(recursos), energia, recompensas))

    return rutas

# 4. Calcular la ruta óptima considerando consecuencias y costos
def calcular_ruta_optima(rutas):
    # Maximizar recursos y recompensas, minimizar longitud
    rutas_ordenadas = sorted(rutas, key=lambda x: (-len(x[1]), -x[3], len(x[0])))
    return rutas_ordenadas[0] if rutas_ordenadas else None

# Ejecución del programa
print("1. Verificar conectividad del grafo:")
conexo = es_conexo(mapa_intrincado)
print("Conexo" if conexo else "No conexo")

if conexo:
    print("\n2. Camino mínimo desde Arrakeen a la Montaña de la Especia:")
    camino_minimo, costo_minimo = dijkstra_camino_minimo(mapa_intrincado, "Arrakeen", "Montaña de la Especia")
    print(f"Camino mínimo: {camino_minimo}, Costo: {costo_minimo}")

    print("\n3. Análisis de rutas alternativas (considerando consecuencias):")
    rutas_alternativas = bfs_rutas_alternativas(mapa_intrincado, "Arrakeen", "Montaña de la Especia")
    for i, (ruta, recursos, energia, recompensas) in enumerate(rutas_alternativas):
        print(f"Ruta {i + 1}: {ruta}, Recursos: {recursos}, Energía restante: {energia}, Recompensas: {recompensas}")

    print("\n4. Calcular ruta óptima:")
    ruta_optima = calcular_ruta_optima(rutas_alternativas)
    if ruta_optima:
        camino, recursos, energia, recompensas = ruta_optima
        print(f"Ruta óptima: {camino}, Recursos: {recursos}, Energía restante: {energia}, Recompensas: {recompensas}")
    else:
        print("No hay rutas disponibles.")
else:
    print("\nEl grafo no es conexo, no es posible realizar las tareas.")
import networkx as nx
import matplotlib.pyplot as plt

# Mapa del desierto con consecuencias variadas y pesos en las rutas
mapa_intrincado = {
    "Arrakeen": {"vecinos": [("Sietch Tabr", 3), ("Oasis del Norte", 2), ("Campamento Fremen", 4)], "consecuencia": "neutral"},
    "Sietch Tabr": {"vecinos": [("Arrakeen", 3), ("Oasis del Este", 5), ("Montaña de la Especia", 6)], "consecuencia": "neutral"},
    "Oasis del Norte": {"vecinos": [("Arrakeen", 2), ("Campamento Fremen", 1)], "consecuencia": "recompensa"},
    "Campamento Fremen": {"vecinos": [("Arrakeen", 4), ("Oasis del Norte", 1), ("Oasis del Este", 3)], "consecuencia": "energía limitada"},
    "Oasis del Este": {"vecinos": [("Sietch Tabr", 5), ("Campamento Fremen", 3), ("Zona Peligrosa", 7)], "consecuencia": "recurso"},
    "Montaña de la Especia": {"vecinos": [("Sietch Tabr", 6), ("Zona Peligrosa", 8)], "consecuencia": "recurso"},
    "Zona Peligrosa": {"vecinos": [("Oasis del Este", 7), ("Montaña de la Especia", 8)], "consecuencia": "muerte"},
}

# Crear el grafo
G = nx.DiGraph()

# Añadir nodos con atributos de consecuencias
for nodo, data in mapa_intrincado.items():
    G.add_node(nodo, consecuencia=data["consecuencia"])

# Añadir aristas con pesos
for nodo, data in mapa_intrincado.items():
    for vecino, peso in data["vecinos"]:
        G.add_edge(nodo, vecino, weight=peso)

# Colorear nodos según sus consecuencias
color_map = {
    "neutral": "white",
    "recurso": "green",
    "energía limitada": "orange",
    "recompensa": "blue",
    "muerte": "red"
}

node_colors = [color_map[G.nodes[node]["consecuencia"]] for node in G.nodes()]

# Visualización del grafo
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, seed=42)  # Layout del grafo
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color=node_colors,
    node_size=1500,
    font_size=10,
    font_color="black",
    edge_color="black",
)

# Añadir etiquetas de pesos a las aristas
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Mostrar el grafo
plt.title("Mapa del Desierto de Arrakis con Consecuencias")
plt.show()

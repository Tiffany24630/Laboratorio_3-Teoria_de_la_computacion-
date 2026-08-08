from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx
from arbol_sintactico import NodoSintactico

def _agregar_nodos(grafo, nodo, profundidad=0, posiciones=None, hojas=None): #Convierte recursivamente el árbol en un grafo y calcula posiciones.
    if posiciones is None:
        posiciones = {}
    if hojas is None:
        hojas = [0]

    if nodo is None:
        return posiciones, hojas

    grafo.add_node(nodo.id, label=nodo.token, profundidad=profundidad)

    hijos = [hijo for hijo in (nodo.izquierdo, nodo.derecho) if hijo is not None]

    for hijo in hijos:
        grafo.add_edge(nodo.id, hijo.id)
        _agregar_nodos(
            grafo,
            hijo,
            profundidad + 1,
            posiciones,
            hojas
        )

    if nodo.es_hoja():
        posiciones[nodo.id] = (hojas[0], -profundidad)
        hojas[0] += 1
    else:
        coordenadas_hijos = [
            posiciones[hijo.id]
            for hijo in hijos
            if hijo.id in posiciones
        ]
        if coordenadas_hijos:
            x = sum(punto[0] for punto in coordenadas_hijos) / len(coordenadas_hijos)
            posiciones[nodo.id] = (x, -profundidad)

    return posiciones, hojas

def dibujar_arbol(arbol, expresion, numero=None, mostrar=True, guardar=True): #Dibuja el árbol sintáctico usando NetworkX + Matplotlib
    if arbol is None or arbol.raiz is None:
        raise ValueError("No se puede dibujar un árbol vacío.")

    grafo = nx.DiGraph()
    posiciones, _ = _agregar_nodos(grafo, arbol.raiz)

    etiquetas = nx.get_node_attributes(grafo, "label")

    ancho = max(10, len(grafo.nodes) * 0.8)
    alto = max(5, arbol.altura() * 1.3)

    figura, eje = plt.subplots(figsize=(ancho, alto))

    nx.draw_networkx_edges(
        grafo,
        posiciones,
        ax=eje,
        arrows=False,
        width=1.5
    )

    nx.draw_networkx_nodes(
        grafo,
        posiciones,
        ax=eje,
        node_size=1700,
        node_color="white",
        edgecolors="black",
        linewidths=1.5
    )

    nx.draw_networkx_labels(
        grafo,
        posiciones,
        labels=etiquetas,
        ax=eje,
        font_size=11
    )

    titulo = "Árbol sintáctico"
    if numero is not None:
        titulo += f" - Expresión {numero}"

    eje.set_title(titulo)
    eje.axis("off")
    figura.tight_layout()

    if guardar:
        carpeta = Path("arboles")
        carpeta.mkdir(exist_ok=True)

        nombre = f"arbol_{numero}.png" if numero is not None else "arbol.png"
        ruta = carpeta / nombre
        figura.savefig(ruta, dpi=160, bbox_inches="tight")
        print(f"\nÁrbol guardado en: {ruta}")

    if mostrar:
        plt.show()
    else:
        plt.close(figura)

    return figura

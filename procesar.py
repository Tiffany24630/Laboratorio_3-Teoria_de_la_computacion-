from utils import tokenizar, expandir_plus, expandir_question, insertar_concatenacion
from shunting_yard import shunting_yard
from balanceador import balanceada
from arbol_sintactico import construir_arbol_sintactico
from visualizador import dibujar_arbol

def procesar(expresion, numero=None, mostrar_arbol=True):
    print("=" * 70)
    print("Expresión original:")
    print(expresion)

    if not balanceada(expresion):
        print("\nERROR: expresión no balanceada.")
        return None

    tokens = tokenizar(expresion)

    print("\nTokens:")
    print(tokens)

    try:
        tokens = expandir_plus(tokens)
        print("\nDespués de expandir +:")
        print(tokens)

        tokens = expandir_question(tokens)
        print("\nDespués de expandir ?:")
        print(tokens)

        tokens = insertar_concatenacion(tokens)
        print("\nDespués de insertar concatenación:")
        print(tokens)

        postfix = shunting_yard(tokens)

        print("\nPostfix:")
        print(" ".join(postfix))

        arbol = construir_arbol_sintactico(postfix)

        print("\nÁrbol sintáctico:")
        print("Preorden:", " -> ".join(arbol.preorden()))
        print("Altura:", arbol.altura())

        dibujar_arbol(
            arbol,
            expresion,
            numero=numero,
            mostrar=mostrar_arbol,
            guardar=True
        )

        return arbol

    except ValueError as e:
        print("\nERROR:", e)
        return None

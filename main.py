from procesar import procesar

print("(Cierre la ventana de cada árbol para continuar con la siguiente expresión)\n")

numero = 0

with open("expresiones.txt", "r", encoding="utf-8") as archivo:
    for linea in archivo:
        linea = linea.strip()

        if linea == "":
            continue

        numero += 1
        procesar(
            linea,
            numero=numero,
            mostrar_arbol=True
        )
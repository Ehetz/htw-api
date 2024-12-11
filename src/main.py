from parts import search_findchips  # Importar la función desde parts.py

def main():
    # Paso 1: Preguntar el tipo de producto
    print("Was möchten Sie suchen?")  # Pregunta en alemán
    print("1. Elektronische Teile")  # Opción 1
    print("2. Allgemeines Produkt")  # Opción 2
    option = input("Bitte wählen Sie 1 oder 2: ").strip()

    if option == "1":
        # Paso 2: Preguntar el número de parte
        part_number = input("Bitte geben Sie die Teilenummer ein: ").strip()
        
        # Paso 3: Llamar a la función para buscar la parte
        try:
            resultados = search_findchips(part_number)
            if resultados:
                print("\nErgebnisse:")
                for resultado in resultados:
                    print(f"- {resultado}")
            else:
                print("Keine Ergebnisse gefunden.")
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
    elif option == "2":
        print("Allgemeine Produkte werden noch nicht unterstützt.")
    else:
        print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")

if __name__ == "__main__":
    main()

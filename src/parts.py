from playwright.sync_api import sync_playwright
import time

def search_findchips(part_number):
    with sync_playwright() as p:
        # Configuración inicial
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        browser = p.chromium.launch(headless=False)  # Cambia a True para modo headless
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()

        # Navegar a FindChips
        page.goto("https://www.findchips.com/")
        print("Página cargada.")

        # Buscar el componente
        try:
            search_box_selector = 'input[placeholder="Enter a part number"]'
            page.wait_for_selector(search_box_selector, timeout=5000)
            page.click(search_box_selector)
            page.fill(search_box_selector, part_number)
            page.keyboard.press("Enter")
            print(f"Buscando: {part_number}")
        except Exception as e:
            print(f"Error al buscar el número de parte: {e}")
            browser.close()
            return

        # Esperar resultados
        try:
            time.sleep(4)  # Esperar carga de resultados

            # Seleccionar todas las filas con datos
            rows = page.query_selector_all('tr.row[data-instock]')
            seen_distributors = set()  # Rastrear distribuidores ya procesados
            offers = []

            for row in rows:
                distributor = row.get_attribute("data-distino")  # Identificador único del distribuidor
                if distributor in seen_distributors:
                    continue  # Saltar si ya procesamos este distribuidor
                seen_distributors.add(distributor)

                # Extraer información de la fila
                part_number_element = row.query_selector('a[data-click-name="part number"]')
                manufacturer_element = row.query_selector('td.td-mfg span')
                description_element = row.query_selector('td.td-desc span.td-description')
                stock_element = row.query_selector('td.td-stock')
                price_element = row.query_selector('td.td-price ul.price-list li span.value')
                buy_link_element = row.query_selector('a.buy-button')

                # Procesar cada campo
                part_number_text = part_number_element.inner_text().strip() if part_number_element else "No disponible"
                manufacturer = manufacturer_element.inner_text().strip() if manufacturer_element else "No disponible"
                description = description_element.inner_text().strip() if description_element else "No disponible"
                stock = stock_element.inner_text().strip() if stock_element else "No disponible"
                price = price_element.inner_text().strip() if price_element else "No disponible"
                buy_link = buy_link_element.get_attribute("href") if buy_link_element else "No disponible"
                if buy_link and buy_link.startswith("//"):
                    buy_link = "https:" + buy_link

                # Agregar oferta a la lista
                offers.append({
                    "distributor": distributor,
                    "part_number": part_number_text,
                    "manufacturer": manufacturer,
                    "description": description,
                    "stock": stock,
                    "price": price,
                    "link": buy_link
                })

                # Limitar a los primeros 3 distribuidores procesados
                if len(offers) == 3:
                    break

            # Mostrar resultados
            for idx, offer in enumerate(offers, start=1):
                print(f"Oferta {idx}:")
                print(f"  Distribuidor: {offer['distributor']}")
                print(f"  Número de Parte: {offer['part_number']}")
                print(f"  Fabricante: {offer['manufacturer']}")
                print(f"  Descripción: {offer['description']}")
                print(f"  Stock: {offer['stock']}")
                print(f"  Precio: {offer['price']}")
                print(f"  Enlace: {offer['link']}")
                print()

        except Exception as e:
            print(f"Error capturando resultados: {e}")

        # Cerrar navegador
        browser.close()

# Ejecutar la aplicación
if __name__ == "__main__":
    part_number_query = input("Introduce el número de parte que deseas buscar: ")
    search_findchips(part_number_query)

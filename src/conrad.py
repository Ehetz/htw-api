from playwright.sync_api import sync_playwright


def search_conrad(query):
    with sync_playwright() as p:
        # Configurar User-Agent
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"

        # Abrir el navegador
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()

        # Navegar a Conrad.de
        page.goto("https://www.conrad.de/")

        # Aceptar cookies si aparecen
        try:
            page.locator('button[data-testid="uc-accept-all-button"]').click()
        except:
            print("No apareció el aviso de cookies.")

        # Hacer clic en la barra de búsqueda y buscar
        search_box_selector = "input#header-search"
        page.click(search_box_selector)
        page.fill(search_box_selector, query)
        page.keyboard.press("Enter")

        # Esperar a que carguen los resultados
        page.wait_for_selector('a.product__title')  # Esperar hasta que el selector principal esté presente

        # Capturar los productos visibles
        name_elements = page.query_selector_all('a.product__title')
        price_elements = page.query_selector_all('p.product__currentPrice')

        print(f"Productos encontrados: {len(name_elements)}")
        print(f"Precios encontrados: {len(price_elements)}")

        # Verificar si hay datos suficientes
        if not name_elements or not price_elements:
            print("No se encontraron productos o precios.")
            browser.close()
            return

        # Limitar a los primeros 5 resultados
        products = []
        for i in range(min(len(name_elements), len(price_elements), 5)):
            # Extraer nombre del producto
            name = name_elements[i].inner_text() if name_elements[i] else "Nombre no disponible"

            # Extraer precio del producto
            price = price_elements[i].inner_text() if price_elements[i] else "Precio no disponible"

            # Extraer enlace del producto
            link = "https://www.conrad.de" + name_elements[i].get_attribute('href') if name_elements[i] else "Enlace no disponible"

            products.append({"name": name, "price": price, "link": link})

        # Mostrar los resultados
        if products:
            for i, product in enumerate(products):
                print(f"Producto {i+1}:")
                print(f"  Nombre: {product['name']}")
                print(f"  Precio: {product['price']}")
                print(f"  Enlace: {product['link']}\n")
        else:
            print("No se encontraron productos válidos.")

        # Cerrar el navegador
        browser.close()

# Ejecutar el script
if __name__ == "__main__":
    query = input("¿Qué quieres buscar en Conrad.de?: ")
    search_conrad(query)


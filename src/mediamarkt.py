from playwright.sync_api import sync_playwright
import time

def search_and_scrape_mediamarkt(query):
    with sync_playwright() as p:
        # Configurar User-Agent
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"

        # Abrir el navegador
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()

        # Navegar a MediaMarkt.de
        page.goto("https://www.mediamarkt.de/")

        # Aceptar cookies
        try:
            cookie_button_xpath = '//*[@id="pwa-consent-layer-accept-all-button"]/span'
            page.locator(cookie_button_xpath).click()
            print("Cookies aceptadas.")
        except Exception as e:
            print(f"No se encontró el botón de cookies o ya se aceptaron. Error: {e}")

        # Hacer clic en la barra de búsqueda y buscar el producto
        try:
            search_box_selector = 'input#search-form'
            page.wait_for_selector(search_box_selector, timeout=3000)  # Esperar a que aparezca el campo de búsqueda
            page.click(search_box_selector)
            page.fill(search_box_selector, query)
            page.keyboard.press("Enter")
            print(f"Buscando producto: {query}")
            page.wait_for_load_state("domcontentloaded")  # Esperar estabilidad tras la navegación
        except Exception as e:
            print(f"Error al buscar el producto: {e}")

        # Esperar y verificar productos
        try:
            max_attempts = 5
            for attempt in range(max_attempts):
                try:
                    product_locator = page.locator('p[data-test="product-title"]')
                    if product_locator.count() > 0:
                        break
                except Exception:
                    print(f"Intento {attempt + 1} de {max_attempts}: Los productos aún no están disponibles.")
                    time.sleep(1)
            else:
                raise Exception("No se encontraron productos después de varios intentos.")
            
            time.sleep(1)
            # Capturar los nombres y precios
            name_elements = page.query_selector_all('p[data-test="product-title"]')
            price_elements = page.query_selector_all('span.sc-dd1a61d2-2.efAprc')

            print(f"Productos encontrados: {len(name_elements)}")
            print(f"Precios encontrados: {len(price_elements)}")

            # Limitar a los primeros 3 resultados
            products = []
            for i in range(min(len(name_elements), len(price_elements), 3)):
                # Extraer nombre del producto
                name = name_elements[i].inner_text() if name_elements[i] else "Nombre no disponible"

                # Extraer precio del producto
                price = price_elements[i].inner_text() if price_elements[i] else "Precio no disponible"

                products.append({"name": name, "price": price})

            # Mostrar los resultados
            if products:
                for i, product in enumerate(products):
                    print(f"Producto {i+1}:")
                    print(f"  Nombre: {product['name']}")
                    print(f"  Precio: {product['price']}\n")
            else:
                print("No se encontraron productos válidos.")
        except Exception as e:
            print(f"Error capturando productos: {e}")

        # Cerrar el navegador
        browser.close()

# Ejecutar el script
if __name__ == "__main__":
    product_query = input("¿Qué producto deseas buscar en MediaMarkt.de?: ")
    search_and_scrape_mediamarkt(product_query)

from playwright.sync_api import sync_playwright
import time

def main():
    with sync_playwright() as p:
        # Configurar User-Agent
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"

        # Abrir el navegador
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()

        # Navegar a Amazon.de
        page.goto("https://www.amazon.de")

        # Esperar a que cargue la página
        page.wait_for_load_state("domcontentloaded")

        # Preguntar qué buscar
        query = input("¿Qué quieres buscar?: ")

        # Hacer clic en la barra de búsqueda y buscar
        search_box_selector = "input#twotabsearchtextbox"
        page.click(search_box_selector)
        page.fill(search_box_selector, query)
        page.keyboard.press("Enter")

        # Esperar a que carguen los resultados
        page.wait_for_selector('div.s-main-slot div[data-component-type="s-search-result"]')

        # Obtener los primeros 5 productos
        products = []
        product_elements = page.query_selector_all('div.s-main-slot div[data-component-type="s-search-result"]')[:5]

        for product in product_elements:
            name_element = product.query_selector('span.a-size-medium.a-color-base.a-text-normal')
            name = name_element.inner_text() if name_element else "Nombre no disponible"

            price_element = product.query_selector('span.a-price-whole')
            price = price_element.inner_text() if price_element else "Precio no disponible"

            link_element = product.query_selector('a.a-link-normal')
            link = "https://www.amazon.de" + link_element.get_attribute('href') if link_element else "Enlace no disponible"

            products.append({"name": name, "price": price, "link": link})

        # Mostrar los resultados
        for i, product in enumerate(products):
            print(f"Producto {i+1}:")
            print(f"  Nombre: {product['name']}")
            print(f"  Precio: {product['price']}")
            print(f"  Enlace: {product['link']}\n")

        # Cerrar el navegador
        browser.close()

# Ejecutar el script
if __name__ == "__main__":
    main()

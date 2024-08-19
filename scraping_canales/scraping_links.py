
from collections import defaultdict
from selenium.webdriver.common.by import By
from scraping_peliculas_series.config.driver import get_driver
from scraping_peliculas_series.utils.scraping_utils import click_button, find_element_with_retries
from scraping_peliculas_series.utils.utils_json import save_to_json

CONFIGURATIONS_BUTTONS = {
        'guide_button': "//div/button/span/span",
        'section_scroll': "//section/div[3]/div/div[2]/div/div[1]/div/h3",
        'categories_file': "resultados.json",
}

def main():
    driver = get_driver()
    driver.get('https://pluto.tv')

    click_button(driver, "XPATH", CONFIGURATIONS_BUTTONS['guide_button'])
    click_button(driver, "XPATH", CONFIGURATIONS_BUTTONS['section_scroll'])

    results = defaultdict(list)
    current_tematica = None

    for i in range(1, 300):
        xpath = f'//div[@aria-rowindex="{i}"]'
        element_to_click = find_element_with_retries(driver, xpath, retries=3)

        if element_to_click:
            try:
                link_element = element_to_click.find_element(By.TAG_NAME, 'a')
                href_value = link_element.get_attribute('href')
                timeline_links = element_to_click.find_elements(By.CSS_SELECTOR, '.timelines a')

                resultado = []
                for index,link in enumerate(timeline_links):
                    href_value2 = link.get_attribute('href')
                    datos = {
                        f"programa {index}": link.text.split('\n'),
                        "link": href_value2
                    }
                    resultado.append(datos)

                href_value = href_value.replace("https://pluto.tv/live-tv/", "https://pluto.tv/latam/live-tv/") + "?lang=en"
                if current_tematica:
                    results[current_tematica].append({
                        'canal':"...",
                        'descripcion': "...",
                        'link': href_value,
                        'programas': resultado
                        })
            except Exception:
                try:
                    h3_element = element_to_click.find_element(By.TAG_NAME, 'h3')
                    h3_value = h3_element.text
                    current_tematica = h3_value
                    results[current_tematica] = []
                except Exception as e:
                    print(f"Error al encontrar <a> o <h3> en aria-rowindex='{i}': {e}")
                    continue
        else:
            print(f"Después de 3 intentos, no se pudo encontrar el elemento con aria-rowindex='{i}'.")
            break

    save_to_json(results, CONFIGURATIONS_BUTTONS['categories_file'])
    driver.quit()

if __name__ == "__main__":
    main()

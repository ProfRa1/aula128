from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"
# Configuração do webdriver
browser = webdriver.Chrome(
    "C:/Users/raiss/Desktop/code_gamesss/PRO_1-1_C128_AtividadeDaProfessora3-main/chromedriver.exe"
)
browser.get(START_URL)
# Tempo para permitir o carregamento da página (pode ser ajustado conforme necessário)
time.sleep(10)
planets_data = []


def scrape():
    page_count = 0
    while page_count < 10:
        print(f"Coletando dados da página {page_count + 1} ...")
        # Objeto BeautifulSoup
        soup = BeautifulSoup(browser.page_source, "html.parser")
        # Loop para encontrar o elemento dentro das tags ul e li
        for ul_tag in soup.find_all("ul", attrs={"class": "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            # Verifique se a lista temp_list possui 5 elementos antes de adicioná-la
            if len(temp_list) == 5:
                planets_data.append(temp_list)
        # Verifica se existe o link para a próxima página
        next_page_link = browser.find_element(
            By.XPATH, '//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a'
        )
        if next_page_link.get_attribute("class") == "inactive":
            # Se não houver link para a próxima página, termina o scraping
            break
        else:
            # Caso contrário, clique no link para ir para a próxima página
            next_page_link.click()
            # Adicione um pequeno tempo de espera para o carregamento da próxima página
            time.sleep(5)
        page_count += 1


# Chamando o método
scrape()
# Criar um DataFrame a partir dos dados coletados
df = pd.DataFrame(
    planets_data,
    columns=["Planet Name", "Column 1", "Column 2", "Column 3", "Column 4"],
)
# Salvar o DataFrame em um arquivo CSV
df.to_csv("exoplanets_data.csv", sep=";", index=False, encoding="utf-8")

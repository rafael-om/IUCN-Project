from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scroll_to_bottom(driver):
    # Obter a altura atual da página
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Rolar até o final da página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Aguardar para que a página carregue o novo conteúdo
        time.sleep(2)  # Ajuste o tempo conforme necessário

        # Calcular nova altura da página e comparar com a altura anterior
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break  # Se a altura não mudou, estamos no final da página
        last_height = new_height

# Chamar a função para rolar até o final da página

links = None
species = set()

service = Service('/snap/bin/firefox.geckodriver')  # Substitua pelo caminho do seu ChromeDriver

urls = ["https://www.iucnredlist.org/search?permalink=48c936e1-7ce8-4481-bdca-3c5079b9b20a",
        "https://www.iucnredlist.org/search?permalink=76dcb48a-8ad1-4aa2-b73c-1dbed44d227a",
        "https://www.iucnredlist.org/search?permalink=cc256527-4f8c-4879-8bbe-e37705c611f0"]

for url in urls:
    driver = webdriver.Firefox(service=service)
    driver.get(url)
    number_of_results = 0
    count = 0
    while number_of_results == 0 and count < 10:  
        try:   
            time.sleep(3)
            number_of_results = int(driver.find_element(By.CSS_SELECTOR, "h1[class='heading heading--list']").find_element(By.XPATH, ".//span").text[1:-1])
        except: 
            count += 1
    if number_of_results == 0:
        print("nao conseguiu carregar pagina")
        break
    driver.quit()

    url_species = set()
    print(number_of_results)
    for i in range(5):
        driver = webdriver.Firefox(service=service)
        driver.get(url)
        try:
            # Esperar até que o elemento <a> esteja presente e clicável
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class='nav-page__item nav-page__item--list']"))
            )
            element.click()
            time.sleep(5)     
        except:
            print("nao conseguiu clickar na lista")
        
        cont = 0
        while True:
            try:  
                # Esperar até que o botão "Show more" esteja presente e visível
                show_more_button = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.section__link-out[role='link']"))
                )
                #driver.execute_script("arguments[0].scrollIntoView();", show_more_button)
                scroll_to_bottom(driver)
                # Clicar no botão "Show more"
                #show_more_button.click()
                driver.execute_script("arguments[0].click();", show_more_button)

                # Aguarde um pouco para permitir que o conteúdo carregue
                time.sleep(1)
                scroll_to_bottom(driver)
                cont = 0
                #cont += 1
                #if cont % 100 == 0:
                    #links = driver.find_elements(By.TAG_NAME, 'a')
                    # Extrair e imprimir os atributos 'href' de cada link
                    #hrefs = []
                    #for link in links:
                        #href = link.get_attribute('href')
                        #if href:  # Verifica se o href não é None
                            #hrefs.append(href)
                #driver.execute_script("arguments[0].scrollIntoView();", show_more_button)
            except Exception as e:
                # Se não encontrar o botão, saímos do loop
                cont += 1
                if cont == 10:
                    break
                print(e)
                print("Todos os elementos foram carregados ou ocorreu um erro.")
                #break
        
        links = driver.find_elements(By.TAG_NAME, 'a')
        # Extrair e imprimir os atributos 'href' de cada link
        for link in links:
            href = link.get_attribute('href')
            if href:  # Verifica se o href não é None
                s = href.strip().split("/")
                if len(s) > 3 and s[-3] == "species":
                    url_species.add(int(s[-2]))
        driver.quit()

        print(url_species)
        if len(url_species) == number_of_results:
            break

        time.sleep(60)
    
    species = species.union(url_species)
    if len(url_species) != number_of_results:
        with open("dividir.txt", "a+") as f:
            f.write(f"{url} precisa ser dividida, nao conseguiu pegar todos ids\n")

with open("id2.txt", "w") as file:
    for i in species:
        file.write(f"{i}\n")

    
        

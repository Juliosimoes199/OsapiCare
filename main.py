import spacy
from fuzzywuzzy import fuzz
from flask import Flask, jsonify, request
import sys
import re
import cv2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time


def filto_exames_confirmado(email, password):
    # Configura o modo headless no Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executa sem interface gráfica
    chrome_options.add_argument("--no-sandbox")  # Recomendado para ambientes como VMs
    chrome_options.add_argument("--disable-dev-shm-usage")  # Evita problemas de memória compartilhada
    chrome_options.add_argument("--disable-gpu")  # Desativa GPU (apenas para precaução em alguns sistemas)

    # Inicializa o driver com as opções configuradas
    navegador = webdriver.Chrome(options=chrome_options)
    
    try:
        # Abre a página de login
        navegador.get('https://akin-lis-app-web.vercel.app/')

        # Preenche as abas de login
        navegador.find_element("id", "email").send_keys(email)
        navegador.find_element("id", "password").send_keys(password)

        # Clica no botão de login
        wait = WebDriverWait(navegador, 30)
        element = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/section/div/div/div[2]/form/button')))
        element.click()

        # Espera até que o botão "Agendamentos" esteja presente
        agendamentos_button = WebDriverWait(navegador, 10000).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[2]/div/div[2]/div/ul/li[1]/button"))
    )
    # Clique no botão "Agendamentos" ou faça outra ação necessária
        print("Apareceu")
        # Captura uma captura de tela da página
        navegador.save_screenshot('screenshot.png')

        # Carrega a captura de tela e a imagem do elemento
        screenshot = cv2.imread('screenshot.png')
        element_image = cv2.imread('ct.png')

        # Usa OpenCV para localizar a posição do elemento na captura de tela
        result = cv2.matchTemplate(screenshot, element_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Desenha um retângulo ao redor do elemento encontrado
        top_left = max_loc
        bottom_right = (top_left[0] + element_image.shape[1], top_left[1] + element_image.shape[0])
        cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
        click_script = f"document.elementFromPoint({bottom_right[0]}, {bottom_right[1]}).click();"
        navegador.execute_script(click_script)
        #time.sleep(20)
        #navegador.find_element(By.XPATH, '//*[@id="radix-:ri:"]/ul/li[3]/a/span').click()

        navegador.save_screenshot('screenshot.png')

        # Carrega a captura de tela e a imagem do elemento
        screenshot = cv2.imread('screenshot.png')
        element_image = cv2.imread('confirmados.png')

        # Usa OpenCV para localizar a posição do elemento na captura de tela
        result = cv2.matchTemplate(screenshot, element_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Desenha um retângulo ao redor do elemento encontrado
        top_left = max_loc
        bottom_right = (top_left[0] + element_image.shape[1], top_left[1] + element_image.shape[0])
        cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
        click_script = f"document.elementFromPoint({bottom_right[0]}, {bottom_right[1]}).click();"
        navegador.execute_script(click_script)

        # Salva a imagem resultante
        cv2.imwrite('resultado.png', screenshot)
        time.sleep(1)
        # Retorna a URL atual como resposta
        current_url = navegador.current_url
        print("URL atual da aba:", current_url)
        return current_url

    except TimeoutException:
        print("O botão 'Agendamentos' não apareceu a tempo.")
        return jsonify({"status": "erro", "mensagem": "O botão não apareceu a tempo"})

    finally:
        # Garante que o navegador seja fechado
        navegador.quit()



def proximos_exames(nome, email, password):    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executa sem interface gráfica
    chrome_options.add_argument("--no-sandbox")  # Recomendado para ambientes como VMs
    chrome_options.add_argument("--disable-dev-shm-usage")  # Evita problemas de memória compartilhada
    chrome_options.add_argument("--disable-gpu")  # Desativa GPU (apenas para precaução em alguns sistemas)
    navegador = webdriver.Chrome(options=chrome_options)
        # Inicializa o driver com as opções configuradas
    navegador.get('https://akin-lis-app-web.vercel.app/')
        #navegador.maximize_window()
        # Preenche as abas de login (substitua 'username_field', 'password_field' e 'login_button' pelos seletores corretos)
    navegador.find_element("id", "email").send_keys(email)
    navegador.find_element("id", "password").send_keys(password)

    wait = WebDriverWait(navegador, 30)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/section/div/div/div[2]/form/button')))
    element.click()

    wait = WebDriverWait(navegador, 30000)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div/div[2]/div/ul/li[2]/button/a[2]/span')))
    element.click()

    wait = WebDriverWait(navegador, 30000)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/main/div/div/div[1]/div/div/div[1]/div[2]/input')))
    element.send_keys(nome)

    wait = WebDriverWait(navegador, 30000)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/main/div/div/div[1]/div/div/div[2]/table/tbody/tr/td[6]/a')))
    element.click()

    wait = WebDriverWait(navegador, 30000)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/main/div/div/div/div[2]/div[2]/div[3]/a/button')))
    element.click()

    time.sleep(3)
    # Obter a URL da aba atual
    current_url = navegador.current_url

    return current_url



def filtro_pacientes(nome, email, password):
    # Configura o modo headless no Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executa sem interface gráfica
    chrome_options.add_argument("--no-sandbox")  # Recomendado para ambientes como VMs
    chrome_options.add_argument("--disable-dev-shm-usage")  # Evita problemas de memória compartilhada
    chrome_options.add_argument("--disable-gpu")  # Desativa GPU (apenas para precaução em alguns sistemas)
    navegador = webdriver.Chrome(options=chrome_options)
    # Inicializa o driver com as opções configuradas
    navegador.get('https://akin-lis-app-web.vercel.app/')
    #navegador.maximize_window()
    # Preenche as abas de login (substitua 'username_field', 'password_field' e 'login_button' pelos seletores corretos)
    navegador.find_element("id", "email").send_keys(email)
    navegador.find_element("id", "password").send_keys(password)
    # Identificar o botão usando uma parte da classe e o tipo
    #navegador.find_element(By.CSS_SELECTOR, 'button.bg-blue-600[type="submit"]').click()
    wait = WebDriverWait(navegador, 30)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/section/div/div/div[2]/form/button')))
    element.click()

    wait = WebDriverWait(navegador, 30000)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div/div[2]/div/ul/li[2]/button/a[2]/span')))
    element.click()

    wait = WebDriverWait(navegador, 30000)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/main/div/div/div[1]/div/div/div[1]/div[2]/input')))
    element.send_keys(nome)

    wait = WebDriverWait(navegador, 30000)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/main/div/div/div[1]/div/div/div[2]/table/tbody/tr/td[6]/a')))
    element.click()

    time.sleep(2)
    # Obter a URL da aba atual
    current_url = navegador.current_url

    return current_url



app = Flask(__name__)
nlp = spacy.load("pt_core_news_md")  # Carrega o modelo Spacy uma vez

def extrair_nomes_spacy(texto):
    doc = nlp(texto)
    nomes = [ent.text for ent in doc.ents if ent.label_ == "PER"]
    return nomes

@app.route('/')
def hello_world():
    return 'Olá do Flask!'

@app.route('/chefe_laboratorio', methods=['POST'])
def tecnico_laboratorio():
    if request.method == 'POST':
        texto = str(request.form['texto'])
        email = request.form['email']

        password = request.form['password']
        def analisar_texto(texto, palavras_chave):
            resultados = []
            doc = nlp(texto)

            for palavra in palavras_chave:
                palavra_doc = nlp(palavra)
                for token in doc:
                    similaridade_semantica = token.similarity(palavra_doc) >= 0.75
                    similaridade_textual = fuzz.ratio(token.text.lower(), palavra.lower()) >= 75

                    if similaridade_semantica or similaridade_textual:
                        resultados.append(palavra)
            return list(set(resultados)) # Retorna apenas palavras-chave únicas encontradas

        palavras_chave = ["filtro", "Filtrar", "exames", "confirmados",
                            "alocação", "técnico", "laboratório", "Aloque",
                            "perfis", "Perfil", "pacientes",
                            "editar", "edição", "dados", "informação",
                            "histórico", "próximos" ,"Próximo", "Futuros", "A seguir",
                            "inicializar", "análise", "imagens",
                            "microscópica", "automatizada", "manual",
                            "manualmente",
                            "geração", "gerar", "laudo",
                            "envio", "remover", "eliminar",
                            "monitorar", "monitoramento", "actividades",
                            "Acção", "movimento", "trabalho", "faça"]

        #texto = "Analise manual mais exames e exames laboratorias tambem"
        resultados = analisar_texto(texto, palavras_chave)
        if (("filtro" in resultados) or ("Filtrar" in resultados)) & ("exames" in resultados):
            url = filto_exames_confirmado(email, password)
            return jsonify({"status": resultados, "url": url})

        elif (("filtro" in resultados) or ("Filtrar" in resultados)) & (("perfis" in resultados) or ("Perfil" in resultados) or ("pacientes" in resultados)):

            nomes = extrair_nomes_spacy(texto)
            nomes = nomes[0]
            print(nomes)
            url = filtro_pacientes(nomes, email, password)
              
            return jsonify({"status": resultados, "url": url})
        
        elif ((("Próximos" in resultados) or ("Próximo" in resultados) or ("Futuros" in resultados) or ("A seguir" in resultados)) & ("exames" in resultados)):
            while True:
                nomes = extrair_nomes_spacy(texto)
                nomes = nomes[0]
                print(f"históricos de exames {nomes}")
                print(f"históricos de email {email}")
                print(f"históricos de password {password}")
                url = proximos_exames(nomes, email, password)
                if url:
                    break
                n += 1
                if n == 3:
                    break
            return jsonify({"status": resultados, "url": url})

        else:
            return "Não tem"

    #return jsonify({"status": resultados})
@app.route('/ver', methods=['GET'])
def ver_rota():
    # s = func.ola1()  # Remova se não estiver usando func
    return "Rota /ver" # Adicione um retorno padrão

# Executa o servidor Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Permite acesso externo
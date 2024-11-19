# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# URL do sistema Vendus (substituir pelo domínio correto)
URL_LOGIN = "https://SEU_DOMINIO.vendus.pt/login/?app"
URL_POS = "https://SEU_DOMINIO.vendus.pt/app/pos/"

# Credenciais de login (substituir pelas credenciais reais)
CREDENCIAIS = {
    "email": "O_SEU_EMAIL",
    "password": "A_SUA_PASSWORD"
}

# Serviços disponíveis na aplicação (com preços e localizações via XPath) (substituir pelos corretos)
SERVICOS = {
    "Aparar a barba": {"xpath": "//button[contains(text(), 'Aparar a barba')]", "preco": 5.00},
    "Barba completa": {"xpath": "//button[contains(text(), 'Barba completa')]", "preco": 6.00},
    "Barba personalizada": {"xpath": "//button[contains(text(), 'Barba personalizada')]", "preco": 7.00},
    "Corte de cabelo simples": {"xpath": "//button[contains(text(), 'Corte de cabelo simples')]", "preco": 9.50},
    "Corte de cabelo completo": {"xpath": "//button[contains(text(), 'Corte de cabelo completo')]", "preco": 11.50},
    "Corte de cabelo Degradê": {"xpath": "//button[contains(text(), 'Corte de cabelo Degradê')]", "preco": 10.50},
    "Pentear + Lavar": {"xpath": "//button[contains(text(), 'Pentear + Lavar')]", "preco": 7.50},
}

def perguntar_servicos():
    """
    Pergunta ao utilizador quais serviços deseja emitir e as respetivas quantidades.
    Retorna um dicionário com os serviços selecionados e as suas quantidades.
    """
    print("\n--- Seleção de Serviços ---")
    servicos_escolhidos = {}
    for servico, detalhes in SERVICOS.items():
        while True:
            try:
                quantidade = int(input(f"Quantos '{servico}' deseja emitir? (Preço: {detalhes['preco']} EUR): "))
                if quantidade < 0:
                    raise ValueError("A quantidade deve ser um número positivo.")
                if quantidade > 0:
                    servicos_escolhidos[servico] = quantidade
                break
            except ValueError as e:
                print(f"Erro: {e}. Por favor, insira um número válido.")
    return servicos_escolhidos

def iniciar_driver():
    """
    Configura e inicia o driver do Chrome com as opções desejadas.
    Neste caso, ativamos a impressão automática sem diálogo.
    Retorna o objeto do driver.
    """
    chrome_options = Options()
    chrome_options.add_argument('--kiosk-printing')  # Impede a caixa de diálogo de impressão
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def autenticar(driver):
    """
    Realiza o login no sistema Vendus utilizando as credenciais fornecidas.
    Em caso de erro, o programa será encerrado.
    """
    print("Autenticando no sistema Vendus...")
    driver.get(URL_LOGIN)

    try:
        # Aguarda que os campos de login estejam visíveis
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "email")))

        # Insere o e-mail
        email_field = driver.find_element(By.NAME, "email")
        email_field.clear()
        email_field.send_keys(CREDENCIAIS["email"])
        print("E-mail inserido com sucesso.")

        # Insere a palavra-passe
        password_field = driver.find_element(By.NAME, "password")
        password_field.clear()
        password_field.send_keys(CREDENCIAIS["password"])
        print("Palavra-passe inserida com sucesso.")

        # Clica no botão de login
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        print("Botão de login clicado com sucesso.")

        print("Autenticação concluída com sucesso!")

    except Exception as e:
        print(f"Erro ao autenticar no sistema: {e}")
        driver.quit()
        raise

def emitir_documentos(driver, servicos):
    """
    Emite documentos com base nos serviços selecionados pelo utilizador.
    Acede ao sistema POS e processa os serviços e respetivas quantidades.
    """
    print("Abrindo o sistema POS...")
    driver.get(URL_POS)

    try:
        # Aguarda até que o carregamento inicial desapareça
        WebDriverWait(driver, 20).until(EC.invisibility_of_element((By.ID, "loading")))
        print("Carregamento inicial concluído com sucesso.")

        # Localiza e clica no link do serviço 'Corte de cabelo'
        corte_cabelo_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='box-menu-item-191252660']/a[contains(text(), 'Corte de cabelo')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", corte_cabelo_link)  # Garante visibilidade
        corte_cabelo_link.click()
        print("Link 'Corte de cabelo' clicado com sucesso.")

        # Processa os serviços selecionados
        for servico, quantidade in servicos.items():
            print(f"Selecionando o serviço: {servico} (Quantidade: {quantidade})")
            for _ in range(quantidade):
                botao_servico = driver.find_element(By.XPATH, SERVICOS[servico]["xpath"])
                botao_servico.click()
                time.sleep(1)  # Intervalo entre cliques

        print("Todos os serviços selecionados foram processados com sucesso.")

    except Exception as e:
        print(f"Erro ao emitir documentos: {e}")
        driver.quit()
        raise

if __name__ == "__main__":
    print("Bem-vindo ao Sistema de Automação de Faturação com Vendus!")
    
    # Pergunta ao utilizador quais serviços deseja emitir
    servicos_escolhidos = perguntar_servicos()

    # Inicia o driver do Chrome
    driver = iniciar_driver()

    try:
        # Realiza autenticação e emite os documentos
        autenticar(driver)
        emitir_documentos(driver, servicos_escolhidos)
    finally:
        # Encerra o driver ao final do processo
        driver.quit()
        print("Processo concluído e driver encerrado com sucesso.")

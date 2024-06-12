import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

servico = Service(ChromeDriverManager().install())
nav = webdriver.Chrome(service=servico)


with open('vendas.json') as j:
    dados = json.load(j)

for venda in dados['vendas']:
    for data, detalhes in venda.items():
        valor = detalhes['valor']
        cpf = detalhes['cpf']
        itens = detalhes['itens']

def login():
    nav.get("https://sso.iob.com.br/signin/?response_type=code&scope=&client_id=c17d4225-9d57-401b-b4fd-32503121f55b&redirect_uri=https://emissor.iob.com.br&lblcontinue=Acessar%20Emissor")

    nav.find_element(By.XPATH, '//*[@id="username"]').send_keys("")
    nav.find_element(By.XPATH, '//*[@id="password"]').send_keys("")

    # Aqui está a pausa. O script vai parar aqui até que você pressione Enter no terminal
    input("Por favor, complete o captcha e depois pressione Enter para continuar...")
    nav.implicitly_wait(5)

def nf(cpf, itens):
    nav.get("https://emissor2.iob.com.br/notafiscal/pdv")
    nav.implicitly_wait(4)

    nav.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div/div/div[2]/button').click()
    nav.implicitly_wait(3)
    nav.find_element(By.XPATH, '//*[@id="adf61b55-ecca-064d-b7b7-3f6c45eb77ea"]').send_keys(cpf)
    
    for id_item, detalhes_item in itens.items():
        nome_produto = detalhes_item['nome']
        peso_produto = detalhes_item['peso']

        nav.find_element(By.XPATH, '//*[@id="47735c87-645c-ca08-5e94-ec9d41ded04b"]').send_keys(nome_produto)
        nav.find_element(By.XPATH, '//*[@id="product_quantity"]').send_keys(peso_produto)

login()

for venda in dados['vendas']:
    for data, detalhes in venda.items():
        valor = detalhes['valor']
        cpf = detalhes['cpf']
        itens = detalhes['itens']
        nf(cpf, itens)

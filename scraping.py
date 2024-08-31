from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from order_prod import OrdensDeProducao as Ops
import time
import json

# Configuração do Selenium
class Scraping:
  def __init__(self) -> None:
    chrome_options = webdriver.ChromeOptions()
    download_directory: str = "C:/Users/Rafaeros/Downloads"
    prefs: dict = {
        "download.default_directory": download_directory,  # Define o diretório de download
        "download.prompt_for_download": False,             # Desativa a confirmação de download
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True                       # Habilita download seguro
    }
    chrome_options.add_experimental_option("prefs", prefs)
    servico = Service(ChromeDriverManager().install())
    self.navegador = webdriver.Chrome(service=servico, options=chrome_options)

  def set_user(self, username: str, password: str) -> None:   
     self.username = username
     self.password = password
    
  def init_scraping(self) -> json.dumps:
    try:
      # Simulando Login
      self.navegador.get('https://web.cargamaquina.com.br/site/login?c=31.1~78%2C8%5E56%2C8')
      userform = self.navegador.find_element(By.ID, 'LoginForm_username')
      pwdform = self.navegador.find_element(By.ID, 'LoginForm_password')
      userform.send_keys(self.username)
      pwdform.send_keys(self.password)
      pwdform.send_keys(Keys.RETURN)

      # Aguarda o login ser concluído
      time.sleep(5)

      self.navegador.get("https://web.cargamaquina.com.br/ordemProducao/exportarOrdens?OrdemProducao%5Bcodigo%5D=&OrdemProducao%5B_nomeCliente%5D=&OrdemProducao%5B_nomeMaterial%5D=&OrdemProducao%5Bstatus_op_id%5D=Todos&OrdemProducao%5B_etapasPlanejadas%5D=&OrdemProducao%5Bforecast%5D=0&OrdemProducao%5B_inicioCriacao%5D=&OrdemProducao%5B_fimCriacao%5D=&OrdemProducao%5B_inicioEntrega%5D=01%2F07%2F2024&OrdemProducao%5B_fimEntrega%5D=31%2F07%2F2024&OrdemProducao%5B_limparFiltro%5D=0&pageSize=20")
      time.sleep(35)

      # Elemento HTML
      trs = self.navegador.find_elements(By.TAG_NAME, "tr")[1:]

      # Iterando a pagina para coleta dos dados das Ordens de Produção e passando para uma classe
      for tr in trs:
        entrega: str = tr.find_elements(By.TAG_NAME, "td")[1].text
        codigo: str = tr.find_elements(By.TAG_NAME, "td")[2].text
        cliente: str = tr.find_elements(By.TAG_NAME, "td")[3].text
        cod_material: str = tr.find_elements(By.TAG_NAME, "td")[4].text
        material: str = tr.find_elements(By.TAG_NAME, "td")[5].text
        quantidade: int = int(tr.find_elements(By.TAG_NAME, "td")[6].text)
        Ops.create(entrega, codigo, cliente, cod_material, material, quantidade)

        with open("ordens_producao.json", "w", encoding="utf-8") as f:
          json.dump(Ops.get_instances(), f, indent=2)
    except Exception as e:
      print("Error: ", e)
    finally:
      self.navegador.quit()
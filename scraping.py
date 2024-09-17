import requests
from order_prod import OrdensDeProducao as Ops
from bs4 import BeautifulSoup
import json
import time

# Configuração do Selenium
class Scraping:
  def init_scraping(self) -> str:
    try:
      cookies: dict = {
         
      }

      headers: dict = {
         
      }

      params: dict = {
          'OrdemProducao[codigo]': '',
          'OrdemProducao[_nomeCliente]': '',
          'OrdemProducao[_nomeMaterial]': '',
          'OrdemProducao[status_op_id]': 'Todos',
          'OrdemProducao[_etapasPlanejadas]': '',
          'OrdemProducao[forecast]': '0',
          'OrdemProducao[_inicioCriacao]': '',
          'OrdemProducao[_fimCriacao]': '',
          'OrdemProducao[_inicioEntrega]': '09/09/2024',
          'OrdemProducao[_fimEntrega]': '09/09/2024',
          'OrdemProducao[_limparFiltro]': '0',
          'pageSize': '20',
      }

      response = requests.get(
          url='https://app.cargamaquina.com.br/ordemProducao/exportarOrdens',
          params=params,
          cookies=cookies,
          headers=headers,
      )

      if response.ok:

        soup = BeautifulSoup(response.content, 'html.parser')

        trs = soup.find_all('tr')[1:]

        # Iterando a pagina para coleta dos dados das Ordens de Produção e passando para uma classe
        for tr in trs:
          entrega: str = tr.find_all("td")[1].get_text(separator='', strip=True).split(" ")[0]
          codigo: str = tr.find_all("td")[2].get_text(separator='', strip=True)
          cliente: str = tr.find_all("td")[3].get_text(separator='', strip=True)
          cod_material: str = tr.find_all("td")[4].get_text(separator='', strip=True)
          material: str = tr.find_all("td")[5].get_text(separator='', strip=True)
          quantidade: int = int(tr.find_all("td")[6].get_text(separator='', strip=True))
          nfes: list[int] = [int(nfe) for nfe in tr.find_all("td")[10].get_text(separator='', strip=True).split("-") if nfe.isdigit()]

          Ops.create(entrega, codigo, cliente, cod_material, material, quantidade, nfes)

        # Formatando as ordens de produção para formato JSON decofidicado para UTF-8
        json_string: str = json.dumps(Ops.get_instances(), indent=2, ensure_ascii=False)
        json_string.encode("utf-8")

        with open("ordens_producao.json", "w", encoding='utf-8') as f:
          json.dump(Ops.get_instances(), f, indent=2, ensure_ascii=False)

        time.sleep(0.5)

        return json_string
      else:
        print("Não foi possivel fazer a requisição:", response.status_code)
        return

    except requests.exceptions.RequestException as e:
      print("error: %s" % e)
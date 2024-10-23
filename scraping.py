import requests
from order_prod import OrdensDeProducao as Ops
from bs4 import BeautifulSoup

# Configuração do Selenium
class Scraping:
    def init_scraping(self) -> str:
        try:
            login_payload = {
              "LoginForm[username]": "rafael.costa",
              "LoginForm[password]": "R869200.14e",
              "LoginForm[codigoConexao]": "31.1~78,8^56,8",
              "yt0": "Entrar"
            }
            params = {
                'OrdemProducao[codigo]': '',
                'OrdemProducao[_nomeCliente]': '',
                'OrdemProducao[_nomeMaterial]': '',
                'OrdemProducao[status_op_id]': 'Todos',
                'OrdemProducao[_etapasPlanejadas]': '',
                'OrdemProducao[forecast]': '0',
                'OrdemProducao[_inicioCriacao]': '',
                'OrdemProducao[_fimCriacao]': '',
                'OrdemProducao[_inicioEntrega]': '10/10/2024',
                'OrdemProducao[_fimEntrega]': '20/10/2024',
                'OrdemProducao[_limparFiltro]': '0',
                'pageSize': '20',
            }

            with requests.Session() as s:
                s.post('https://app.cargamaquina.com.br/site/login?c=31.1~78%2C8%5E56%2C8', data=login_payload)
                response = s.get('https://app.cargamaquina.com.br/ordemProducao/exportarOrdens', params=params)

            if response.ok:

                # Convertendo get do scraping para html
                soup = BeautifulSoup(response.content, 'html.parser')

                # Pegando todos table rows da tabela a partir do 1°
                trs = soup.find_all('tr')[1:]

                # Iterando a pagina para coleta dos dados das Ordens de Produção e passando para uma classe
                for tr in trs:
                    dataEntrega: str = tr.find_all("td")[1].get_text(separator='', strip=True).split(" ")[0]
                    codigoOrdemProducao: int = int(tr.find_all("td")[2].get_text(separator='', strip=True).split('-')[-1])
                    cliente: str = tr.find_all("td")[3].get_text(separator='', strip=True)
                    codigoMaterial: str = tr.find_all("td")[4].get_text(separator='', strip=True)
                    descricaoMaterial: str = tr.find_all("td")[5].get_text(separator='', strip=True)
                    quantidade: int = int(tr.find_all("td")[6].get_text(separator='', strip=True))
                    status: str = (tr.find_all("td")[7].get_text(separator='', strip=True))
                    nfes: list[int] = [int(nfe) for nfe in tr.find_all("td")[10].get_text(separator='', strip=True).split("-") if nfe.isdigit()]

                    Ops.create(dataEntrega, codigoOrdemProducao, cliente, codigoMaterial, descricaoMaterial, quantidade, status, nfes)

                # Formatando as ordens de produção para formato JSON decofidicado para UTF-8
                json_string: str = Ops.to_json()
                json_string.encode("utf-8")

                # Salvando as ordens de produção no arquivo JSON
                Ops.save_json_file()
                return json_string
            else:
                print("Não foi possivel fazer a requisição:", response.status_code)
                return

        except requests.exceptions.RequestException as e:
            print(f"error: {e}")


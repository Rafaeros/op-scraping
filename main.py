from scraping import Scraping
import requests

if __name__ == '__main__':
    URL: str = "http://localhost:8090/api/v1/ordem_producao"
    S = Scraping()
    json_request: str = S.init_scraping()

    headers: dict = {
        'Content-Type': 'application/json'
    }   

    response = requests.post(URL, data=json_request, headers=headers)
    if response.ok:
        print(json_request)
        print("Requisição post concluida, status code: ", response.status_code)
    else:
        print("Falha na requisição status code:  ", response.status_code)
from scraping import Scraping
import requests

if __name__ == '__main__':
  S = Scraping()
  S.set_user("username", "password")
  json = S.init_scraping()
  requests.post("api_url", data=json)
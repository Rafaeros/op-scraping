from scraping import Scraping

if __name__ == '__main__':
  S = Scraping()
  S.set_user("username", "password")
  S.init_scraping()
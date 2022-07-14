import requests
from bs4 import BeautifulSoup

class Parsing(): 
    base_url = 'https://habr.com'
    url = base_url + '/ru/all'
    HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }


    def __init__(self, key_hub):
        self.key_hub = key_hub


    def parsing_text(self, url_text):
        respons = requests.get(url_text, headers=self.HEADERS)
        soup = BeautifulSoup(respons.text, 'html.parser')
        
        text = soup.find(class_='article-formatted-body article-formatted-body article-formatted-body_version-2').find_all('p')
        text_all = [text_iter.text for text_iter in text]

        for key in self.key_hub:
            for text in text_all:
                if key in text:
                    # print('yes')
                    return True
            
        return False



    def parsing(self):

        respons = requests.get(self.url, headers=self.HEADERS)
        soup = BeautifulSoup(respons.text, 'html.parser')

        keys = ', '.join(self.key_hub)
        print (f'Найденые статьи по ключевым статьям {keys}:')
        print()

        articles = soup.find_all('article')
        for article in articles:
            hubs = article.find_all(class_='tm-article-snippet__hubs-item')
            hubs_span = [hub.find('span').text for hub in hubs]

            for hub in hubs_span:
                if hub in self.key_hub:

                    href = article.find(class_='tm-article-snippet__title-link').attrs['href']

                    url_text = self.base_url + href

                    self.parsing_text(url_text)
                    if self.parsing_text(url_text) == True:


                        title = article.find('h2').find('span').text
                        time_hub = article.find('time').attrs['title']
                        print(f'{title}, дата создания {time_hub}: {self.base_url}{href}')
                    else:
                        print('Ничего не найдено')


def main():
    key_hub = ['Занимательные задачки', 'Не буду томить ожиданием и сразу выложу код алгоритма']

    Parsing(key_hub).parsing()

if __name__ == '__main__':
    main()
    
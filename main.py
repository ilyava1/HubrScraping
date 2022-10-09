import service
import requests
from bs4 import BeautifulSoup


preview_URL = 'https://habr.com/ru/all/'
main_URL = 'https://habr.com'

# определяем список ключевых слов
KEYWORDS = ['Эрзянский', 'IT-инфраструктура', 'Криптография', '37 900'
            ]


if __name__ == '__main__':

    page = requests.get(preview_URL, headers=service.make_my_header())
    soup = BeautifulSoup(page.text, features='html.parser')
    articles = soup.find_all('article')
    count = 0
    print()
    for article in articles:

        # Ищем ключевые слова в заголовке
        title = article.find(class_='tm-article-snippet__title-link').text
        if service.check_for_exist(KEYWORDS, title) is True:
            service.print_article(article, main_URL)
            count += 1
            continue

        # Ищем ключевые слова в хабах
        hubs = article.find_all(class_='tm-article-snippet__hubs-item-link')
        hubs = [hub.text.strip() for hub in hubs]

        flag = 0
        for hub in hubs:
            for keyword in KEYWORDS:
                if keyword in hub and flag == 0:
                    service.print_article(article, main_URL)
                    count += 1
                    flag = 1
                    break
        if flag == 1:
            continue

        # Ищем ключевые слова в тексте preview
        try:
            text = article.find_all(class_='article-formatted-body '
                                           'article-formatted-body '
                                           'article-formatted-body_version-2'
                                    )[0].text
        except IndexError:
            text = article.find_all(class_='article-formatted-body '
                                           'article-formatted-body '
                                           'article-formatted-body_version-1'
                                    )[0].text

        if service.check_for_exist(KEYWORDS, text) is True:
            service.print_article(article, main_URL)
            count += 1
            continue

        # Ищем ключевые слова в полном тексте статьи
        full_text_short_href = article.find('h2').find('a').attrs['href']
        full_text_full_href = main_URL + full_text_short_href
        page = requests.get(full_text_full_href,
                            headers=service.make_my_header())
        soup = BeautifulSoup(page.text, features='html.parser')
        try:
            full_article = soup.find_all(class_='article-formatted-body '
                                         'article-formatted-body '
                                         'article-formatted-body_version-2'
                                         )[0].text
        except IndexError:
            full_article = soup.find_all(class_='article-formatted-body '
                                         'article-formatted-body '
                                         'article-formatted-body_version-1'
                                         )[0].text

        if service.check_for_exist(KEYWORDS, full_article) is True:
            service.print_article(article, main_URL)
            count += 1

    if count == 0:
        print('Нет статей содержащих ключевые слова:')
        for keyword in KEYWORDS:
            print(' - ', keyword)

from fake_headers import Headers


def make_my_header():
    """
    Функция формирования заголовков.

    Позволяет преодолеть работу блокировок безопастности сервиса-получателя
    запросов при периодических запросах
    :return: заголовок для передачи веб-сервису
    """
    header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )
    my_header = header.generate()

    return my_header


def check_for_exist(keywords, suspect_string):
    """
    Функция проверки вхождения подстроки в строку.

    :param keywords: список подстрок для проверки вхождения
    :param suspect_string: строка в которой ищется вхождение
    :return: True если хотябы одна подстрока из списка входит в строку
    """
    for keyword in keywords:
        if keyword in suspect_string:
            return True
    return False


def print_article(article, main_URL):
    """
    Функция печати статьи согласно формату, данному в ДЗ

    :param article: Статья
    :param main_URL: Ссылка не ресурс со статьями для формирования
    поллной ссылки на статью
    :return: None
    """
    art_date = article.find(class_='tm-article-snippet__datetime-published'
                            ).time.attrs['title']
    art_title = article.find('h2').find('span').text
    art_link = article.find(class_='tm-article-snippet__title-link'
                            ).attrs['href']
    result = f'{art_date} - "{art_title}" - {main_URL}{art_link}'
    print(result)

    return

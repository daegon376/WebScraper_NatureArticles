import os
import requests
import string

from bs4 import BeautifulSoup


def save_article(title, url, directory):
    page = requests.get(url)
    assert page.status_code == 200, 'article page not loaded'
    soup = BeautifulSoup(page.content, 'html.parser')
    text = soup.find('div', {'class': 'c-article-body'}).text
    text_bytes = text.encode('UTF-8')

    replacements = title.maketrans(' ', '_', string.punctuation)
    file_name = title.translate(replacements) + '.txt'
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'wb') as file:
        file.write(text_bytes)

    return file_name


if __name__ == '__main__':
    required_pages_amount = int(input())
    required_article_type = str(input())
    saved_articles = []
    page_num = 0

    while page_num < required_pages_amount:
        page_num += 1
        new_dir_name = 'Page_' + str(page_num)
        os.mkdir(new_dir_name)
        current_dir = os.path.join(os.getcwd(), new_dir_name)
        link = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020' + \
               '&page=' + str(page_num)
        root_page = requests.get(link)
        assert root_page.status_code == 200, 'root_page error'
        soup = BeautifulSoup(root_page.content, 'html.parser')
        articles = soup.find_all('article')

        for content in articles:
            a_type = content.find('span', {'data-test': 'article.type'}).text.strip()
            if a_type == required_article_type:
                title = content.find('h3').text.strip()
                url = 'https://www.nature.com' + content.find('a')['href']
                print(url)
                saved_articles.append(save_article(title, url, current_dir))

    print('Saved articles:', saved_articles, sep='\n')

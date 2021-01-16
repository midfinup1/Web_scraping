from bs4 import BeautifulSoup
import requests

KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'история it']

response = requests.get('https://habr.com/ru/all/')
soup = BeautifulSoup(response.text, 'html.parser')

posts = soup.find_all('article', class_='post')
for post in posts:
    hubs = post.find_all('li', class_='inline-list__item_hub')
    hub_topics = list(map(lambda hub: hub.text.strip().lower(), hubs))
    link = post.find('a', class_='btn').attrs.get('href')
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    full_post_text = soup.find('div', class_='post__text').text.strip().lower()
    if any([desired in full_post_text for desired in KEYWORDS]) or \
            any([desired in hub_topics for desired in KEYWORDS]):
        post_date = post.find('span', class_='post__time').text.strip()
        post_link = post.find('a', class_='post__title_link').attrs.get('href')
        post_header = post.find('a', class_='post__title_link').text.strip()
        print(f'{post_date} - {post_header} - {post_link}')

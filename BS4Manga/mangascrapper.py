import requests
from bs4 import BeautifulSoup

from chrome.chrome_manga_scrapping import ChromeMangaScrapper


class MangaScrapper:

    def __init__(self, base_url):
        self.url = base_url

    def manga_landing_scrapper(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        landing = {'landing': {'trending': [], 'recently_updated': []}}
        landing['landing']['trending'] = self.get_trending_mangas(soup)
        landing['landing']['recently_updated'] = self.get_recent_mangas(soup)
        return landing

    def get_trending_mangas(self, soup):
        result_trending = soup.find_all("div", class_='item')
        trending = []
        for result in result_trending:
            title_wrapper = result.find('h3')
            title = title_wrapper.getText()
            link = title_wrapper.find('a')['href'].split('/')
            img = result.find('img')['src']
            trending.append({'title': title, 'link': link[len(link) - 1], 'img': img})
        return trending

    def get_recent_mangas(self, soup):
        result_rencent = soup.findAll('div', class_='itemupdate')
        recently_updated = []
        for result in result_rencent:
            img = result.find('img')['src']
            title_wrapper = result.find('h3').find('a')
            title = title_wrapper.getText()
            link = title_wrapper['href'].split('/')
            save_manga_link = link[len(link) - 1]
            last_chapters = result.find_all('span')
            chapters = []
            for chapter in last_chapters:
                info = chapter.find('a')
                link = info['href'].split('/')
                save_chapter_link = link[len(link) - 1]
                chapters.append({'chapter_name': info['title'], 'chapter_link': save_chapter_link})
            recently_updated.append(
                {'title': title, 'img': img, 'manga_id': save_manga_link, 'recent_chapters': chapters})
        return recently_updated

    def manga_info_scrapper(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        manga = self.manga_info_builder(soup)

        return manga

    def manga_info_builder(self, soup):
        manga_information = self.manga_information_retriever(soup)
        manga_information['chapter_list'] = self.manga_chapter_list_retriever(soup)

        return manga_information

    def manga_information_retriever(self, soup):
        manga_scrapping = {
            'poster_img': '',
            'title': '',
            'alternative_title': [],
            'author': [],
            'status': '',
            'last_updated': '',
            'views': '',
            'genres': [],
            'rating': '',
            'description': '',
            'chapter_list': []
        }
        manga_info_top = soup.find('div', class_='manga-info-top')
        if manga_info_top is None:
            manga_info_top = soup.find('div', class_='manga-info-top')

        manga_scrapping['poster_img'] = manga_info_top.find('div', class_='manga-info-pic').find('img')['src']
        manga_info = soup.find('ul', class_='manga-info-text').find_all('li')
        manga_scrapping['title'] = manga_info[0].find('h1').getText()
        if manga_info[0].find('h2'):
            manga_scrapping['alternative_title'] = manga_info[0].find('h2').getText().split(' ; ')
        authors_find = manga_info[1].find_all('a')

        for author in authors_find:
            manga_scrapping['author'].append({'name': author.getText(), 'author_link': author['href']})
        manga_scrapping['status'] = manga_info[2].getText().split(' : ')[1]
        manga_scrapping['last_updated'] = manga_info[3].getText().split(' : ')[1]
        manga_scrapping['views'] = manga_info[5].getText().split(' : ')[1]
        genres = manga_info[6].find_all('a')

        for genre in genres:
            manga_scrapping['genres'].append({'genre': genre.getText(), 'link': genre['href']})
        manga_scrapping['rating'] = manga_info[8].find('em').getText().split(' : ')[1].split(' - ')[0].split(' / ')[0]
        manga_scrapping['description'] = soup.find('div', id='noidungm').getText()
        return manga_scrapping

    def manga_chapter_list_retriever(self, soup):
        chapter_list = []
        chapters = soup.find('div', class_='chapter-list').find_all('div', class_='row')
        for chapter in chapters:
            info = chapter.find_all('span')
            chapter_list.append(
                {
                    'title': info[0].find('a')['title'],
                    'link': info[0].find('a')['href'].replace('https://mangakakalot.com/chapter/',''),
                    'views': info[1].getText(),
                    'updated_at': info[2]['title']
                }
            )
        return chapter_list

    def chapter_display_info(self,chapter,manga):
        chrome_scrapper = ChromeMangaScrapper(self.url)
        chapter_imgs = chrome_scrapper.get_images_from_chapter(chapter,manga)
        return chapter_imgs

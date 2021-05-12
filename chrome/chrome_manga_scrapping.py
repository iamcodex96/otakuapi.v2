import json
import os
import time
from pathlib import Path

from selenium import webdriver
from data_models.Manga.simplemanga import SimpleManga


class ChromeMangaScrapper:
    top_mangas = []
    recent_mangas = []

    def __init__(self, root_url):
        self._root_url = root_url
        self._chrome_options = webdriver.ChromeOptions()
        # self._chrome_options.add_argument('headless')
        self._chrome_driver = webdriver.Chrome('./chrome/chromedriver.exe', options=self._chrome_options)
        self._chrome_driver.set_window_size(1000, 2000)
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def get_principal_landing_info(self):
        self._chrome_driver.get(self._root_url)

        # Header Scrapping
        item_top_wrapper = self._chrome_driver.find_element_by_class_name('owl-wrapper')
        items = item_top_wrapper.find_elements_by_class_name('item')
        self._process_top_mangas(items)

        # Recent Scrapping
        item_recent_wrapper = self._chrome_driver.find_element_by_class_name('doreamon')
        recent_items = item_recent_wrapper.find_elements_by_class_name('itemupdate')
        self._process_recent_mangas(recent_items)
        self._chrome_driver.quit()

    def _process_top_mangas(self, items):
        for item in items:
            img = item.find_element_by_tag_name('img').get_property('src')
            title = item.find_element_by_tag_name('h3').find_element_by_tag_name('a').get_property('title')
            chapter = item.find_elements_by_tag_name('a')
            link = item.find_element_by_tag_name('h3').find_element_by_tag_name('a').get_property('href')
            chapter_info = {'name': chapter[1].get_property('title'), 'link': chapter[1].get_property('href')}
            manga = SimpleManga(name=title, img=img, link=link)
            manga.chapters.append(chapter_info)
            jsonified_manga = manga.toJSON()
            self.top_mangas.append(jsonified_manga)

    def _process_recent_mangas(self, items):
        for item in items:
            img = item.find_element_by_tag_name('img').get_property('src')
            title = item.find_element_by_tag_name('h3').find_element_by_tag_name('a').text
            link = item.find_element_by_tag_name('h3').find_element_by_tag_name('a').get_property('href')
            manga = SimpleManga(title, img, link)
            chapters = item.find_elements_by_tag_name('span')
            for chapter in chapters:
                c = chapter.find_element_by_tag_name('a')
                chapter_info = {'name': c.get_property('title'), 'link': c.get_property('href')}
                manga.chapters.append(chapter_info)
            jsonified_manga = manga.toJSON()
            self.recent_mangas.append(jsonified_manga)

    def get_trending_mangas(self):
        return self.top_mangas

    def get_recent_mangas(self):
        return self.recent_mangas

    def get_images_from_chapter(self, chapter, manga):
        links = []

        self._chrome_driver.get(self._root_url)
        images = self._chrome_driver.find_element_by_class_name(
            'container-chapter-reader').find_elements_by_tag_name('img')
        Path(self.BASE_DIR + f'/temp/manga/{manga}/chapters/{chapter}').mkdir(parents=True, exist_ok=True)
        for i in range(len(images)):
            with open(f'{self.BASE_DIR}/temp/manga/{manga}/chapters/{chapter}/{i}.png', 'wb') as file:
                file.write(images[i].screenshot_as_png)
            links.append(f'/temp/manga/{manga}/chapters/{chapter}/{i}.png')
        self._chrome_driver.close()
        self._chrome_driver.quit()
        return links



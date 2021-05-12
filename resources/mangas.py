import os
from pathlib import Path

from BS4Manga.mangascrapper import MangaScrapper
from flask_restful import Resource


class Mangas(Resource):
    def get(self):
        print('''
            ***************************************
                        REQUESTING LANDING
            ***************************************
        ''')
        manga_scrapper = MangaScrapper(base_url='https://mangakakalot.com/')
        return manga_scrapper.manga_landing_scrapper(), 200


class Manga(Resource):
    def get(self, manga):
        print(f'''
            ***************************************
                    REQUESTING MANGA '{manga}'
            ***************************************
        ''')
        if 'read-' not in manga:
            manga_scrapper = MangaScrapper(base_url=f'https://mangakakalot.com/manga/{manga}')
        else:
            manga_scrapper = MangaScrapper(base_url=f'https://mangakakalot.com/{manga}')

        return manga_scrapper.manga_info_scrapper(), 200


class Chapter(Resource):
    def get(self, manga, chapter):
        print(f'''
            ***************************************
         REQUESTING MANGA '{manga}' CHAPTER '{chapter}'
            ***************************************
        ''')
        manga_scrapper = MangaScrapper(base_url=f'https://mangakakalot.com/chapter/{manga}/{chapter}')
        chapter_res = {
            'manga_id': manga,
            'chapter_id': chapter,
            'chapter_imgs': None
        }
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if not Path(base_dir + f'/temp/manga/{manga}/chapters/{chapter}').exists():
            chapter_res['chapter_imgs'] = manga_scrapper.chapter_display_info(chapter,manga)
        else:
            links = []
            list_files = os.listdir(base_dir + f'/temp/manga/{manga}/chapters/{chapter}'.replace('.png',''))
            sorted_files = sorted(list_files,key= lambda x: int(os.path.splitext(x)[0]))
            for file in sorted_files:
                links.append(f'/temp/manga/{manga}/chapters/{chapter}/{file}')
            chapter_res['chapter_imgs'] = links
        return chapter_res, 200

import json


class SimpleManga:

    def __init__(self, name,img,link):
        self.name = name
        self.img = img
        self.link = link
        self.chapters = []

    def toJSON(self):
        return json.dumps({"name":self.name,"img":self.img,"link":self.link,"visible_chapters":self.chapters})

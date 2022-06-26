from numpy import isin
from requests import get
from bs4 import BeautifulSoup
import cloudscraper
import os
def download_it(root, path, filename, content):
    full_path = os.path.join(os.getcwd(), root)
    if not os.path.exists(full_path):
        os.mkdir(full_path)
        print("make available")
        if not os.path.exists(os.path.join(full_path, path)):
            os.mkdir(os.path.join(full_path, path))
        else:
            pass
    else:
        if not os.path.exists(os.path.join(full_path, path)):
            os.mkdir(os.path.join(full_path, path))
        else:
            pass
    real_path = os.path.join(os.path.join(full_path, path))
    with open(os.path.join(real_path, filename), "wb") as file2:
        file2.write(content)
        file2.close()
    return "success"
class MangaHub:
    def __init__(self, manga, limit=10):
        self.manga = manga
        self.scraper = cloudscraper.CloudScraper()
        r = self.scraper.get("https://mangahub.io/search", params= {"q" : manga, "order" : "POPULAR", "genre" : "all"})
        soup = BeautifulSoup(r.text, "html.parser")
        old = [x.find_all("a") for x in soup.find_all("h4", class_ = "media-heading")]
        self.__matches = []
        for x in old:
            for z in x:
                self.__matches.append(z)
        self.matches = [x["href"] for x in self.__matches[:limit]][0] if limit == 1 else [x["href"] for x in self.__matches[:limit]]
        self.selected = None
    def __repr__(self) -> str:
        return str(self.matches)
    def __getitem__(self, x):
        if isinstance(x, int):
            return self.matches[x]
        else:
            return False
    @property
    def select(self):
        return
    @select.setter
    def select(self, val):
        self.selected = val
    def download(self, chapter, page):
        base_url = "https://mangahub.io/chapter/"
        imgbase_url = "https://img.mghubcdn.com/file/imghub/"
        chapter_path = "/chapter-" + str(chapter)
        if self.selected:
            print(self.selected)
        else:
            return False
        info = self.__info()
        full_url = base_url + info["manga"] + chapter_path
        pagelimit = self.get_pagelimit(full_url)
        if int(chapter) > int(info["chapter_limit"]):
            return False
        else:
            pass
        if int(page) > int(pagelimit):
            return False
        else:
            pass
        imgform = ".png"
        img_url = imgbase_url + info["realname"].lower() + "/" + str(chapter) + "/" + str(page) + imgform
        cont = self.scraper.get(img_url)
        if cont.json().get("status") == 404:
            imgform = ".jpg"
            img_url = imgbase_url + info["realname"].lower() + "/" + str(chapter) + "/" + str(page) + imgform
            cont = self.scraper.get(img_url)
        else:
            pass
        root = info["realname"]
        path = str(chapter)
        filename = "db" + str(page) + imgform
        print(img_url)
        print(download_it(root, path, filename, cont.content))
    def matchings(self):
        return self.__info()
    def get_pagelimit(self, url):
        ht = self.scraper.get(url).text
        soup = BeautifulSoup(ht, "html.parser")
        raw = soup.findAll("p", class_="_3w1ww")[0].text
        self.pagelimit = raw.split("/")[1]
        return self.pagelimit
    def __info(self):
        if self.selected:
            info = self.scraper.get(self.selected)
        else:
            return
        soup = BeautifulSoup(info.text, "html.parser")
        info = [x for x in soup.find_all("span", class_ = None)[-4].descendants]
        chapter_limit = info[-1]
        url = info[0]["href"]
        name = self.selected.split("/")[-1].split("_")[0] if "_" in self.selected.split("/")[-1] else self.selected.split("/")[-1]
        return {"chapter_limit" : chapter_limit, "manga" : url.split("/")[4], "realname" : name}


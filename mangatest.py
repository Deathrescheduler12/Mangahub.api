import mangahub

manga = mangahub.MangaHub("Ippo")
manga.select = manga[0]
print(manga.download(12, 12))

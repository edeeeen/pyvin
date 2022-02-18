import datetime
import bs4
import requests
class dictionary():
    def dictionary(self):
        while True:
            url = input("Input url: ")
            if url == "exit":
                break;
            self.bandcampAlbumInfo(url)
            with open('dict.txt', 'r', encoding="utf-8") as f:
                x = f.read()
            x = x[0:-1]+",\n\""+self.artist+"  - "+self.album+"\":["+str(self.tracks)+","+str(self.lengths)+"]}"
            print(x)
            with open('dict.txt', 'w', encoding="utf-8") as f:
                f.write(x)
            #   "": [[""],[""]],


    def bandcampAlbumInfo(self, page_url):
        request_obj = requests.get(page_url)

        html_obj = bs4.BeautifulSoup(request_obj.text, "html5lib")
        title_div = html_obj.find("div", id="name-section")
        release_name = title_div.find("h2", class_="trackTitle")
        self.album = release_name.contents[0].strip()
        release_artist = title_div.find("h3").find("a")
        self.artist = release_artist.contents[0].strip()
        release_date = html_obj.find("div", class_="tralbumData tralbum-credits")
        date_string = release_date.contents[0].strip()[9:]
        date_object = datetime.datetime.strptime(date_string, "%B %d, %Y")
        self.date = str(date_object.strftime("%Y-%m-%d"))
        track_table = html_obj.find("table", id="track_table")
        tracks = track_table.find_all("tr", "track_row_view linked")
        self.lengths = []
        self.tracks = []
        for track_number, track_tr in enumerate(tracks, start=1):
            track_cell = track_tr.find("td", class_="title-col")
            title = track_cell.find("span", class_="track-title")
            length = track_cell.find("span", class_="time secondaryText")
            self.lengths.append(length.contents[0].strip())
            self.tracks.append(title.contents[0])


if __name__ == "__main__":
    dictionary().dictionary()

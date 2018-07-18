from urllib.request import urlopen
from bs4 import BeautifulSoup
import xlsxwriter


i = 1
mn = 1

workbook = xlsxwriter.Workbook('TV.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write(0, 0, "Title")
worksheet.write(0, 1, "Year")
worksheet.write(0, 2, "Certification")
worksheet.write(0, 3, "Runtime")
worksheet.write(0, 4, "Rating")
worksheet.write(0, 5, "Summary")
worksheet.write(0, 6, "No_Of_Votes")
worksheet.write(0, 7, "Runtime_Min")
worksheet.write(0, 8, "Genre")
my_list = [1107, 1216, 1245, 2002, 2006, 2019, 2020, 2021, 2121, 2268, 2427]
my_list.extend([2473, 2640, 2789, 2836, 3054, 3132, 3143, 3145, 3217, 3353, 3416, 3443, 3465])

for pageno in range(1, 2938):
    pg = str(pageno)
    imdb_url = "https://www.imdb.com/search/title?title_type=tv_series&page="+pg
    imdb_page = urlopen(imdb_url)
    soup = BeautifulSoup(imdb_page, "html.parser")
    list_movie = soup.find("div", attrs={"class": "lister-list"})

    for movie in list_movie.findAll("div", attrs={"class": "lister-item mode-advanced"}):
        if mn not in my_list:
            content = movie.find("div", attrs={"class": "lister-item-content"})
            item_header = content.find("h3", attrs={"class": "lister-item-header"})
            item_title = item_header.find("a")
            tv_title = item_title.string.strip()  # Extract the show title
            item_year = item_header.find("span", attrs={"class": "lister-item-year text-muted unbold"})
            tv_year = item_year.string.strip()  # Extract show year

            misc = content.findAll("p", attrs={"class": "text-muted"})
            item_certificate = misc[0].find("span", attrs={"class": "certificate"})
            tv_certificate = "NA"
            if item_certificate:
                 tv_certificate = item_certificate.string.strip()  # Extract show certification
            item_runtime = misc[0].find("span", attrs={"class": "runtime"})
            tv_runtime = "NA"
            if item_runtime:
                tv_runtime = item_runtime.string.strip()  # Extract show runtime
            item_genre = misc[0].find("span", attrs={"class": "genre"})
            tv_genre = "NA"
            if item_genre :
                tv_genre = item_genre.string.strip()  # Extract show genre

            rat = content.find("div", attrs={"class": "ratings-bar"})
            tv_rating = "0"
            if rat:
             rat_imdb = rat.find("div", attrs={"class": "inline-block ratings-imdb-rating"})
             rat_imdb_strong = rat_imdb.find("strong")
             tv_rating = rat_imdb_strong.string.strip()  # Extract show rating

            tv_summary = misc[1].string  # Extract show summary

            item_vote = content.find("p", attrs={"class": "sort-num_votes-visible"})
            tv_nv = "0"
            if item_vote:
                item_nv = item_vote.find("span", attrs={"name": "nv"})
                tv_nv = item_nv.string.strip()  # Extract no of votes
            print(mn, end = '\n')
            worksheet.write(i, 0, tv_title)
            year = ""
            cn = 0
            for char in tv_year:
                if char in "0123456789":
                    if cn < 4:
                        year += char
                        cn += 1
            year = int(year)
            worksheet.write(i, 1, year)
            worksheet.write(i, 2, tv_certificate)
            worksheet.write(i, 3, tv_runtime)
            tv_rating = float(tv_rating)
            worksheet.write(i, 4, tv_rating)
            worksheet.write(i, 5, tv_summary)
            nv_r = ""
            for ind in range(0, len(tv_nv)):
                if tv_nv[ind]!=',':
                     nv_r += tv_nv[ind]
            nv_r = int(nv_r)
            worksheet.write(i, 6, nv_r)
            runtime = ""
            for j in tv_runtime:
                if j in "0123456789":
                    runtime += j
            if len(runtime) > 0:
                runtime = int(runtime)
            else:
                runtime = 0
            worksheet.write(i, 7, runtime)
            worksheet.write(i, 8, tv_genre)
            i += 1
        mn = mn + 1


workbook.close()




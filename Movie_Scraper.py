from urllib.request import urlopen
from bs4 import BeautifulSoup
import xlsxwriter


i = 1

workbook = xlsxwriter.Workbook('Movie.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write(0, 0, "Title")
worksheet.write(0, 1, "Year")
worksheet.write(0, 2, "Certification")
worksheet.write(0, 3, "Runtime")
worksheet.write(0, 4, "Rating")
worksheet.write(0, 5, "Metascore")
worksheet.write(0, 6, "Summary")
worksheet.write(0, 7, "No_Of_Votes")
worksheet.write(0, 8, "Gross")
worksheet.write(0, 9, "Genre")
worksheet.write(0, 10, "Runtime_Min")
my_list = [4701]

for pageno in range(1, 201):
    pg = str(pageno)
    imdb_url = "https://www.imdb.com/search/title?sort=num_votes,desc&start=2&title_type=feature&year=1950,2018&page="+pg
    imdb_page = urlopen(imdb_url)
    soup = BeautifulSoup(imdb_page, "html.parser")
    list_movie = soup.find("div", attrs={"class": "lister-list"})

    for movie in list_movie.findAll("div", attrs={"class": "lister-item mode-advanced"}):
        if i not in my_list:
            content = movie.find("div", attrs={"class": "lister-item-content"})
            item_header = content.find("h3", attrs={"class": "lister-item-header"})
            item_title = item_header.find("a")
            movie_title = item_title.string.strip()  # Extract the movie title
            item_year = item_header.find("span", attrs={"class": "lister-item-year text-muted unbold"})
            movie_year = item_year.string.strip()  # Extract movie year

            misc = content.findAll("p", attrs={"class": "text-muted"})
            item_certificate = misc[0].find("span", attrs={"class": "certificate"})
            movie_certificate = "NA"
            if item_certificate:
                 movie_certificate = item_certificate.string.strip()  # Extract film certification
            item_runtime = misc[0].find("span", attrs={"class": "runtime"})
            movie_runtime = "NA"
            if item_runtime:
                movie_runtime = item_runtime.string.strip()  # Extract movie runtime
            item_genre = misc[0].find("span", attrs={"class": "genre"})
            movie_genre = item_genre.string.strip()

            rat = content.find("div", attrs={"class": "ratings-bar"})
            rat_imdb = rat.find("div", attrs={"class": "inline-block ratings-imdb-rating"})
            rat_imdb_strong = rat_imdb.find("strong")
            movie_rating = rat_imdb_strong.string.strip()  # Extract movie rating
            rat_meta = rat.find("div", attrs={"class": "inline-block ratings-metascore"})
            movie_metascore = "NA"
            if rat_meta:
                rat_meta_fav = rat_meta.find("span", attrs={"class": "metascore favorable"})
                if(rat_meta_fav):
                    movie_metascore = rat_meta_fav.string.strip()  # Extract movie metascore

            movie_summary = misc[1].string  # Extract movie summary

            item_vote = content.find("p", attrs={"class": "sort-num_votes-visible"})
            item_nv = item_vote.findAll("span", attrs={"name": "nv"})
            movie_nv = item_nv[0].string.strip()  # Extract no of votes
            length = len(item_nv)
            movie_gross = "NA"
            if length>1:
                 movie_gross = item_nv[1].string.strip()  # Extract gross amount
            #  print("Title : {0}\nYear : {8}\nCertification : {1}\nRuntime : {2}\nRating : {3}\nMetascore : {4}\nSummary : {5}\nNo. of votes : {6}\nGross : {7}\n".format(movie_title,movie_certificate,movie_runtime,movie_rating,movie_metascore,movie_summary,movie_nv,movie_gross,movie_year))
            print(i,end = '\n')
            worksheet.write(i, 0, movie_title)
            year = ""
            for char in movie_year:
                if char in "0123456789":
                    year += char
            year = int(year)
            worksheet.write(i, 1, year)
            worksheet.write(i, 2, movie_certificate)
            worksheet.write(i, 3, movie_runtime)
            movie_rating = float(movie_rating)
            worksheet.write(i, 4, movie_rating)
            if(movie_metascore!="NA"):
                movie_metascore = int(movie_metascore)
            worksheet.write(i, 5, movie_metascore)
            worksheet.write(i, 6, movie_summary)
            nv_r = ""
            for ind in range(0, len(movie_nv)):
                if movie_nv[ind]!=',':
                     nv_r += movie_nv[ind]
            nv_r = int(nv_r)
            worksheet.write(i, 7, nv_r)
            worksheet.write(i, 8, movie_gross)
            runtime = ""
            for j in movie_runtime:
                if j in "0123456789":
                    runtime += j
            if len(runtime) > 0:
                runtime = int(runtime)
            else:
                runtime = 0
            worksheet.write(i, 9, movie_genre)
            worksheet.write(i, 10, runtime)
        i += 1


workbook.close()




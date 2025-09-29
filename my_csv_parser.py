# 
# parse the CVS file

import csv

def movie_filter(genre):
    filename = "imdb-movie-data.csv"
    if not genre:
        return []
    wanted = genre.strip().lower()
    result =[]
    
    with open(filename) as csvfile:
        csv_content = csv.DictReader(csvfile)
        
        for movie in csv_content:
            genres = [g.strip().lower() for g in movie.get("Genre", "").split(",")]
            if wanted in genres:
               result.append(movie)
            
    
    return (result)
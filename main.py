#!/usr/bin/env python

import sys
import correlation

MOVIE_DB = None
RATINGS_DB = None
USER_DB = None
USER_RATINGS = {
    71: 5,
    72: 4,
    588: 5,
    1014: 4,
    541: 5,
    543: 5,
    42: 4,
    83: 5,
    82: 5,
    88: 2,
    739: 2
        }

def load_movies(filename): #2nd function
    #creates dictionary of file contents: splits into fields, which are keys for the dictionary
    """1|Toy Story (1995)|01-Jan-1995||http://us.imdb.com/M/title-exact?Toy%20Story%20(1995)|0|0|0|1|1|1|0|0|0|0|0|0|0|0|0|0|0|0|0
    
    id, title, release_date, vhs_release_date, imdb_url, """

    movie_dict = {}

    f = open(filename)
    #file open
    for line in f:
        fields = clean_line(line, "|")
        if not fields:
            continue
        movie_id = int(fields[0])
        title = fields[1]
        release_date = fields[2]
        imdb_url = fields[4]
        genre_list = fields[5:]
        
        movie = {
                "id": movie_id,
                "title": title,
                "release_date": release_date,
                "imdb_url": imdb_url,
                "genre_list": genre_list
            }

        movie_dict[movie_id] = movie
    f.close()
    #file closes
    # For loop is ended
    return movie_dict

def load_genres(movie_dict, filename): #4th function called
    genre_dict = {} # makes a dictionary
    f = open(filename) # opens file
    for line in f:
        fields = clean_line(line, "|") # calls clean_line
        if not fields:
            continue
        key = int(fields[1]) # the key is the second field
        genre = fields[0] # genre is the first field
        genre_dict[key] = genre
    f.close() # file closes

    for movie_id, movie in movie_dict.items(): # movie dict from MOVIE_DB
        genre_ids = movie['genre_list']
        genre_list = []

        for i in range(len(genre_ids)): # list of genres based on position
            if genre_ids[i] == "1":
                genre = genre_dict[i] # i == position for both the list and the dictionary
                genre_list.append(genre) 

        # genre list is populated
        movie['genres'] = genre_list # list of all genres 

def clean_line(line, sep=None): #3rd, 5th, 7th, 9th function called
    stripped = line.strip()
    if stripped == "":
        return None
    return stripped.split(sep)
    
def load_users(filename): # 6th function called
    f = open(filename) # opens file
    user_db = {} # user dictionary
    genders = {"M": "Male", "F": "Female"} # gender dictionary
    for line in f:
        fields = clean_line(line, "|") # calls clean_line
        id, age, gender, occupation, zipcode = fields # unpacks fields into id etc
        id = int(id) 
        age = int(age)
        gender = genders[gender] # corresponding gender from genders dict
        user_db[id] = { # using int id for user_dict place
                "id": id,
                "age": age,
                "gender": gender,
                "occupation": occupation
                }

    f.close() # closes file

    return user_db # returns user dict 

def load_ratings(filename): #8th function
    ratings = {} #creates ratings dictionary
    f = open(filename) #opens file
    for line in f:
        fields = clean_line(line) #runs clean_line function
        if not fields:
            continue
        user_id, movie_id, rating, timestamp = fields #unpacks fields into user_id etc
        user_id = int(user_id)
        movie_id = int(movie_id)
        rating = int(rating)
        movie_ratings = ratings.get(movie_id) #creates or updates ratings dict
        if not movie_ratings: # if empty
            ratings[movie_id] = {user_id: rating} # adds user/rating to movie id
        else: 
            movie_ratings[user_id] = rating # updates the user/rating to a particular movie

    f.close() # closes file

    return ratings # returns ratings dictionary {movie id: {user id: rating}}

def movie_details(movie_id): # 10th function 
    movie = MOVIE_DB.get(movie_id) # global MOVIE_DB - retrieves movie id from db dict

    if not movie: # if it doesn't exist, print this message
        print "No movie with id %d"%movie_id
    # if it's found, print this message - also joins with genres    
    print """\
%d: %s
%s"""%(movie['id'], movie['title'], ", ".join(movie['genres']))
    pass

def error(msg = "Unknown command"): # ya done goofed
    print "Error:", msg

def quit(): # 11th -- exits the system on user command
    print "Goodbye!"
    sys.exit(0)

def average_rating(movie_id): # ("12th") when user calls "avg", this function runs
    ratings = RATINGS_DB[movie_id] #variable is value of RATINGS_DB[movie_id]
    print "%.2f"%(float(sum([v for k,v in ratings.items()]))/len(ratings))
    #averages sum of ratings for that movie, divided by #of ratings given & returns
    #number to the nearest 2 decimal points

def user_details(user_id): 
    user = USER_DB[user_id] # pulls user from USER_DB
    print "%s %s, age %d"%(user['gender'], # prints user information
            user['occupation'], user['age'])

def user_rating(movie_id, user_id): # find a users rating of a movie
    rating = RATINGS_DB[movie_id][user_id] # pulls rating w/ movie and user
    movie = MOVIE_DB[movie_id] # pulls movie
    print "User %d rated movie %d (%s) at %d"%(\
            user_id, movie_id, movie['title'],
            rating) # prints rating and movie information, with user id

def rate_movie(movie_id, rating): 
    movie = MOVIE_DB[movie_id] # pulls movie from db
    USER_RATINGS[movie_id] = rating # assigns rating to movie in the USER_RATINGS dict
    print "You rated movie %d: %s at %d stars."%(\
            movie_id, movie['title'],
            rating) # this is what you just did, gosh

def predict(movie_id):
    ratings = RATINGS_DB[movie_id] #assigns variable 'ratings' to value of RATINGS_DB[movie_id]
    movie = MOVIE_DB[movie_id] #assigns variable 'movie' to MOVIE_DB[movie_id]
    movies = [ m for k, m in USER_RATINGS.iteritems() ] # THIS LINE IS DUM - christian zeb f
    similarities = [ (correlation.pearson_similarity(RATINGS_DB, movie_id, k), m) for k, m in USER_RATINGS.iteritems() ]
    # comparing your rating to all other ratings for these movies, and compares similarity 
    # tuple for movie id and similarity score
    top_five = sorted(similarities) # all similar movies, sorted
    top_five.reverse() # highest to lowest
    top_five = top_five[:5] # actual top 5
    num = 0.0
    den = 0.0
    # Use a weighted mean rather than a strict top similarity
    for sim, m in top_five:
        num += (float(sim) * m) # sim
        den += sim

    rating = num/den # calculated based on top5 -- the closer to 5, the more likely the movie ratings are similar to your own

    print "Best guess for movie %d: %s is %.2f stars"%\
            (movie_id, movie['title'], rating)


def parse(line, dispatch):
    tokens = line.split()
    if not tokens:
        return error()

    cmd = tokens[0]
    command = dispatch.get(cmd)

    if not command:
        return error()
     
    if len(tokens) != len(command):
        return error("Invalid number of arguments")

    function = command[0]

    if len(command) == 1:
        return function()

    try:
        type_tuples = zip(command[1:], tokens[1:])
        typed_arguments = [ _type(arg) for _type, arg in type_tuples ]
        return function(*typed_arguments)

    except Exception, e:
        print e
        return error("Invalid argument to %s"%(cmd))


def main(): #1st function
    global MOVIE_DB, USER_DB, RATINGS_DB #initalize global variables
    MOVIE_DB = load_movies("ml-100k/u.item")
    load_genres(MOVIE_DB, "ml-100k/u.genre")
    USER_DB = load_users("ml-100k/u.user")
    RATINGS_DB = load_ratings("ml-100k/u.data")

    dispatch = { #these are the commands, defined by functions above
            "movie": (movie_details, int),
            "q": (quit,),
            "avg": (average_rating, int),
            "user": (user_details, int),
            "rating": (user_rating, int, int),
            "rate": (rate_movie, int, int),
            "predict": (predict, int)
            }

    while True:
        line = raw_input("> ")
        parse(line, dispatch) # parses user input
   
if __name__ == "__main__":
    main()

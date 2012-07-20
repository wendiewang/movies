db = None

# HOW TO TEST THIS FILE
# comment out the command line prompt 3 lines in the movies.py file
# run in command line "python -i movies.py" 
# print Movie.get(1)

class User(object):
    def __init__(self, age, occupation, gender):
        self.age = age
        self.occupation = occupation
        self.gender = gender

    @staticmethod
    def get(user_id):
        user = db.users.find_one({"_id": user_id})
        return User(user['age'], user['occupation'],
                user['gender'])

    def __str__(self):
        return "%s %s, age %d"%(self.gender,
                self.occupation, self.age)

class Movie(object): 
    def __init__(self, movie_id, title, url, genres):
        self.movie_id = movie_id 
        self.title = title
        self.url = url
        self.genres = genres 

    @staticmethod
    def get(movie_id):
        movie = db.movies.find_one({"_id": movie_id})
        return Movie(movie['_id'], movie['title'], movie['imdb_url'], movie['genres'])

    def __str__(self):
        return "Movie %d: %s \n%s" % (self.movie_id, self.title, self.genres_as_string())
        
    def genres_as_string(self):
        # .join replaces the following 3 lines
        # ret = ""
        # for g in self.genres:
        #    ret += g 
        return ", ".join(self.genres)

#class Rating(object):
#     def __init__():
        
        
        

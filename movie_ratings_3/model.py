db = None

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

        # M Student Age: 27

class Movies(object): 
    def __init__(self, movie_id, title, url, genres):
        self.movie_id = movie_id 
        self.title = title
        self.url = url
        self.genres = genres 

    @staticmethod
    def get(movie_id):
        movie = db.movies.find_one({"_id": movie_id})
        return movie

    def __str__(self):
        return "Movie %d: %s \n %s" % (self.movie_id, self.title, self.genres)

# class Genres(Movies):
#     def __init__(self, name):
#         self.name

#     def __str__(self):
#         return "%s" % (", ".join(movie['genres']))


# class Ratings(object):
#     def __init__():
#         
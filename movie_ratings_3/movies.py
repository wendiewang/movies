#!/usr/bin/env python

import sys
from correlation import pearson_similarity as pearson
import pymongo
from collections import defaultdict
import traceback
import model
from model import User, Movie

db = None

#1
def movie_details(movie_id):
    movie = db.movies.find_one({"_id": movie_id})

    if not movie:
        print "No movie with id %d"%movie_id

    
    print """\
%d: %s
%s"""%(movie['_id'], movie['title'], ", ".join(movie['genres']))


def error(msg = "Unknown command"):
    print "Error:", msg

def quit():
    print "Goodbye!"
    sys.exit(0)
#2
def average_rating(movie_id):
    rating_records = get_ratings(movie_id=movie_id)
    ratings = [ rec['rating'] for rec in rating_records ]
    avg = float(sum(ratings))/len(ratings)
    return "%.2f"%(avg)
    
#3
def user_details(user_id):
    user = User.get(user_id)
    return user
#4
def user_rating(movie_id, user_id):
    rating = get_rating(movie_id, user_id)
    if not rating:
        print "Sorry, user %d has not rated movie %d"%(user_id, movie_id)
        return
    movie = get_movie(movie_id)
    return "User %d rated movie %d (%s) at %d stars"%(\
            user_id, movie_id, movie['title'],
            rating)
#5
def rate_movie(movie_id, rating):
    movie = get_movie(movie_id)
    db.ratings.update({"movie_id": movie_id, "user_id": 0},
            {"$set": {"rating": rating}}, upsert=True)
    return "You rated movie %d: %s at %d stars."%(\
            movie_id, movie['title'],
            rating)

def get_movie(movie_id):
    return db.movies.find_one(movie_id)

def get_ratings(movie_id=None, user_id=None):
    query = {}
    if movie_id is not None:
        query['movie_id'] = movie_id
    if user_id is not None:
        query['user_id'] = user_id

    records = db.ratings.find(query)
    return [ rec for rec in records ]

def get_rating(movie_id, user_id):
    record = db.ratings.find_one({"movie_id": movie_id, "user_id": user_id})
    if record:
        return record['rating']

def movie_ids(user_id): 
    ratings = get_ratings(user_id=0)
    movie_ids = []
    #rates is the item to iterate by
    for rates in ratings:
        movie_ids.append(rates['movie_id'])
    return movie_ids
    
def make_target_ratings(movie_id):
    rated_movies = get_ratings(movie_id)
    ratings_dict = {}
    for each in rated_movies:
        key = each['user_id']
        value = each['rating']
        ratings_dict[key] = value 
    return ratings_dict

# 6 
def predict(movie_id):
    target_movie = Movie.get(movie_id)
    #target_movie = get_movie(movie_id)
    target_ratings = make_target_ratings(movie_id)
    # target_movie_rating = rating
    my_movie_ids = movie_ids(0)

    movies_to_compare = []
    for id in my_movie_ids:
        ratings = make_target_ratings(id)
        movies_to_compare.append(ratings)

    similarities = []

    for ratings in movies_to_compare:
        our_rating = ratings[0] # ratings is not a list, it is a dictionary
        similarity = pearson(target_ratings, ratings)
        tup = (similarity, our_rating)
        similarities.append(tup)

    # (similarity, ranking)

    top_five = sorted(similarities)
    top_five.reverse()
    top_five = top_five[:5]
    num = 0.0
    den = 0.0
    # Use a weighted mean rather than a strict top similarity
    for sim, m in top_five:
        num += (float(sim) * m)
        den += sim

    rating = num/den
    return "Best guess for movie %d: %s is %.2f stars"%\
            (movie_id, target_movie['title'], rating)



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
        traceback.print_exc()
        return error("Invalid argument to %s"%(cmd))

def connect_db(host, port, user, password, db_name):
    connect_string = "mongodb://%s:%s@%s:%d/%s" % \
            (user, password, host, port, db_name)

    c = pymongo.connection.Connection(connect_string)
    return c[db_name]

def main():
    global db
    #db = pymongo.connection.Connection("localhost")
    db = connect_db("dbh36.mongolab.com", 27367, "movie_user", "password", "movies")
    db = db['movies']
    model.db = db

    dispatch = {
            "movie": (movie_details, int),
            "q": (quit,),
            "avg": (average_rating, int),
            "user": (user_details, int),
            "rating": (user_rating, int, int),
            "rate": (rate_movie, int, int),
            "predict": (predict, int)
            }

    #while True:
    #    line = raw_input("> ")
    #    parse(line, dispatch)
   
if __name__ == "__main__":
    main()

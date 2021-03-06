#!/usr/bin/env python

import sys
from correlation import pearson_similarity as pearson
import pymongo
from collections import defaultdict
import traceback

global db

def movie_details(movie_id):
    movie = db.movies.find_one({"_id": movie_id})

    if not movie:
        print "No movie with id %d"%movie_id

    print """\
%d: %s
%s"""%(movie['_id'], movie['title'], ", ".join(movie['genres']))
    pass

def error(msg = "Unknown command"):
    print "Error:", msg

def quit():
    print "Goodbye!"
    sys.exit(0)

def average_rating(movie_id):
    rating_records = get_ratings(movie_id=movie_id)
    ratings = [ rec['rating'] for rec in rating_records ]
    avg = float(sum(ratings))/len(ratings)

    print "%.2f"%(avg)

def user_details(user_id):
    user = get_user(user_id)
    print "%s %s, age %d"%(user['gender'],
            user['occupation'], user['age'])

def user_rating(movie_id, user_id):
    rating = get_rating(movie_id, user_id)
    movie = get_movie(movie_id)
    print "User %d rated movie %d (%s) at %d stars"%(\
            user_id, movie_id, movie['title'],
            rating)

def rate_movie(movie_id, rating):
    movie = get_movie(movie_id)
    db.ratings.update({"movie_id": movie_id, "user_id": 0},
            {"$set": {"rating": rating}}, upsert=True)
    print "You rated movie %d: %s at %d stars."%(\
            movie_id, movie['title'],
            rating)

def get_user(user_id):
    return db.users.find_one({"_id": user_id})

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
    return db.ratings.find_one({"movie_id": movie_id, "user_id": user_id})['rating']

def predict(movie_id):
    movie = get_movie(movie_id=movie_id)
    target_movie = get_movie(movie_id)
    user_ratings = get_ratings(user_id=0) # only for one case scenario

    for rating in user_ratings: 
        rating = {'movie_id': movie_id
                  'rating': rating 
              } 
        # {u'rating': 5, u'_id': ObjectId('5005a5b43c01017d73c3e9e3'), u'movie_id': 71, u'user_id': 0}

    # dictionary = { }

    similarities = [ (correlation.pearson_similarity(user_rating, movie_id, k), m) for k, m in dictionary ]
    
    top_five = sorted(similarities)
    top_five.reverse()
    top_five = top_five[:5]

    num = 0.0
    den = 0.0
    for sim, m in top_five:
        num += (float(sim) * m)
        den += sim

    rating = num/den

    print "Best guess for movie %d: %s is %.2f stars"%\
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

    dispatch = {
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
        parse(line, dispatch)
   
if __name__ == "__main__":
    main()

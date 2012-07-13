#!/usr/bin/env python
from math import sqrt
import correlation

g_crud = {} # current ratings user dictionary

def load_movie_dictionary(filename):
	item_file = open(filename)
	all_movies = {}  #outside for loop but inside function so that for loop can reference it
	for line in item_file.readlines():
		movie_data = {}  #each time it loops, movie_data {} becomes empty 
		stripped = line.strip()
		l = stripped.split("|")
		movie_data['id'] = l[0]
		movie_data['title'] = l[1]
		movie_data['date'] = l[2]
		movie_data['imdb'] = l[4]
		movie_data["Unknown"] = l[5]
		movie_data["Action"] = l[6]
		movie_data["Adventure"] = l[7]
		movie_data["Animation"] = l[8]
		movie_data["Childrens"] = l[9]
		movie_data["Comedy"] = l[10]
		movie_data["Crime"] = l[11]
		movie_data["Documentary"] = l[12]
		movie_data["Drama"] = l[13]
		movie_data["Fantasy"] = l[14]
		movie_data["Film_noir"] = l[15]
		movie_data["Horror"] = l[16]
		movie_data["Musical"] = l[17]
		movie_data["Mystery"] = l[18]
		movie_data["Romance"] = l[19]
		movie_data["Sci_fi"] = l[20]
		movie_data["Thriller"] = l[21]
		movie_data["War"] = l[22]
		movie_data["Western"] = l[23]
		all_movies[movie_data['id']] = movie_data
	item_file.close()
	return all_movies

def movie_details(id, all_movies):
	movie_lookup = all_movies[id]
	title = movie_lookup['title']
	#print "%s" % #genres that have a value of 1
	genre_list = []
	for key, value in movie_lookup.items():
		if value == '1' and key != movie_lookup['id']: 
			genre_list.append(key)
	genres = (", ").join(genre_list)
	print "Movie %s: %s\n%s" %(id, title, genres)
	

def load_rating_dictionary(filename):
	ratings = open(filename)
	all_ratings = {}
	for line in ratings:
		stripped = line.strip()
		l = stripped.split("\t")
		# if movie not in all_ratings:
		if l[1] not in all_ratings:
		# 	make values into rating_data dictionary, add movie as new key w/ rating_data
			rating_data = {}
			rating_data[l[0]] = int(l[2])
			all_ratings[l[1]] = rating_data
		else: # if movie is in all_ratings:
			moviekey = all_ratings[l[1]] # 	pull out rating_data dict from that key/movie
			moviekey[l[0]] = int(l[2]) #	add current values (l[0], l[2]) to rating_data dictionary
			all_ratings[l[1]] = moviekey # 	put back in db under correct key/movie
	ratings.close()
	return all_ratings

def average_movie_rating(id, all_ratings):
	moviekey = all_ratings[id]
	rating_list = []
	for key, value in moviekey.items():
		rating_list.append(int(value))
	denominator = len(rating_list)
	numerator = 0.0
	for item in rating_list:
		numerator += item
	rating = numerator / denominator
	print "%.1f" %rating

def load_user_dictionary(filename):
	users = open(filename)
	all_users = {}
	for line in users:
		if line == None:
			pass
		stripped = line.strip()
		l = stripped.split("|")
		all_users[l[0]] = l[1:4]
	users.close()
	return all_users

def get_user(id, all_users):
	user_lookup = all_users[id]
	if user_lookup[1] == "M":
		gender = "Male"
	else:
		gender = "Female"
	print "%s %s, age %s" % (gender, user_lookup[2], user_lookup[0])

def user_rating(user_id, movie_id, all_ratings): 
	movie_lookup = all_ratings.get(movie_id)
	user_rating = movie_lookup.get(user_id)
	print "User %s rated movie %s at %d stars" %(user_id, movie_id, user_rating)

def rate(movie_id, rating, movie_dictionary):
	movie = movie_dictionary.get(movie_id)
	title = movie['title']
	g_crud[movie_id] = rating 
	print "You have rated movie %s: %s at %d stars" % (movie_id, title, rating)


def predict(target_movie_id, rating_dictionary, movie_dictionary):
	movie = movie_dictionary.get(target_movie_id)
	title = movie['title']

	best_key = None
	best_correlation = -9

	for movie_id, rating in g_crud.items():
		similarity = correlation.pearson_similarity(rating_dictionary, target_movie_id, movie_id)
		if similarity > best_correlation:
			best_key = movie_id
			best_correlation = similarity
			predicted_rating = similarity * rating

	print "Best guess for movie %s: %s is %.1f stars" %(movie_id, title, predicted_rating)

def main():
	ratings = load_rating_dictionary("../ml-100k/u.data")
	movie_db = load_movie_dictionary("../ml-100k/u.item")
	users = load_user_dictionary("../ml-100k/u.user")
	movie_details('43', movie_db)
	average_movie_rating('42', ratings)
	get_user('483', users)
	user_rating('42', '845', ratings)
	rate('42', 3, movie_db)
	rate('588', 5, movie_db)
	rate('71', 5, movie_db)
	rate('890', 2, movie_db)
	predict('1', ratings, movie_db)

if __name__ == '__main__':
	main()





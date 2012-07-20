

def movie_dictionary():
	item_file = open("u.item")
	all_movies = {}  #outside for loop but inside function so that for loop can reference it
	for line in item_file.readlines():
		movie_data = {}  #each time it loops, movie_data {} becomes empty 
		l = line.split("|")
		movie_data['id'] = l[0]
		movie_data['title'] = l[1]
		movie_data['date'] = l[2]
		movie_data['imdb'] = l[4]
		movie_data["unknown"] = l[5]
		movie_data["action"] = l[6]
		movie_data["adventure"] = l[7]
		movie_data["animation"] = l[8]
		movie_data["childrens"] = l[9]
		movie_data["comedy"] = l[10]
		movie_data["crime"] = l[11]
		movie_data["documentary"] = l[12]
		movie_data["drama"] = l[13]
		movie_data["fantasy"] = l[14]
		movie_data["film_noir"] = l[15]
		movie_data["horror"] = l[16]
		movie_data["musical"] = l[17]
		movie_data["mystery"] = l[18]
		movie_data["romance"] = l[19]
		movie_data["sci_fi"] = l[20]
		movie_data["thriller"] = l[21]
		movie_data["war"] = l[22]
		movie_data["western"] = l[23]
		all_movies[int(movie_data['id'])] = movie_data
	return all_movies

def movie_details(id, all_movies):
	lookup_hash = all_movies[id]
	title = lookup_hash['title']
	print "Movie: %d %s" %(id, title) #could be lookup_hash['id']
	for key,value in lookup_hash.items():
	    if key != "id" and key != "title" and key != "date" and key != "imdb" and value == "1" :
	        print key
	
all_movies = movie_dictionary()
movie_details(41, all_movies)
	
	

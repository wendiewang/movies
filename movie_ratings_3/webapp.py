from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
import movies
import model

app = Flask(__name__)
app.config.from_object(__name__)

@app.before_request
def before_request():
    g.db = movies.connect_db("dbh36.mongolab.com", 27367, "movie_user", "password", "movies")
    db = g.db['movies']
    model.db = db
    movies.db = db

#mongodb automatically knows to close 
#@app.teardown_request
#def teardown_request(exception):
#    g.db.close()
     #g is a special object provided by Flask


# post and get relies on forms 

@app.route('/', methods=['GET'])
def dispatch():
    return render_template('index.html')

@app.route('/movie_details', methods=['POST'])
def movie_details():
    #movie = movies.get_movie_details(int(request.form['movie_id']))
    movie = model.Movie.get(int(request.form['movie_id']))
    return render_template('movie.html', movie=movie)
    
@app.route('/avg', methods=['POST'])
def avg(): #url_for
    movie = model.Movie.get(int(request.form['movie_id']))
    avg = movies.average_rating(int(request.form['movie_id']))
    return render_template('avg.html', movie=movie, avg=avg)
    
@app.route('/user_details', methods=['POST'])
def user():
    user = movies.user_details(int(request.form['user_id']))
    return render_template('user.html', user=user)
    
@app.route('/user_rating', methods=['POST']) 
def user_rating():
    user_rating = movies.user_rating(int(request.form['movie_id']), int(request.form['user_id']))
    return render_template('user_rating.html', user_rating=user_rating)

@app.route('/rate_movie', methods=['POST'])
def rate_movie():
    rate_movie = movies.rate_movie(int(request.form['movie_id']), int(request.form['rating']))
    return render_template('rate_movie.html', rate_movie=rate_movie)

@app.route('/predict', methods=['POST'])
def predict():
    movie_id = request.form['movie_id']
    #print movie_id
    rating = movies.predict(int(movie_id))
    #print predict
    title = movies.movie_title(int(movie_id))
    return render_template('predict.html', title=title, movie_id=movie_id, rating=rating)
    
if __name__ == '__main__':
    app.run(debug=True)

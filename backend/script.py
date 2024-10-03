from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.devOps_bdd
collection = db.sons

@app.route('/', methods=['GET', 'POST'])
def index():
    sons = []  
    error = None  

    if request.method == 'POST':
        artist_name = request.form.get('artist_name')  
        if artist_name:
            songs = collection.find({'artistName': {'$regex': artist_name, '$options': 'i'}})  
            sons = list(songs)
            if not sons:
                error = f"Aucun artiste trouvé avec le nom: '{artist_name}'"
        else:
            error = "Veuillez entrer un nom d'artiste."

    return render_template('index.html', sons=sons, error=error)

if __name__ == '__main__':
    app.run(debug=True)

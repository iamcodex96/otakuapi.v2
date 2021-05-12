from flask import Flask, render_template
from flask_restful import Api
from werkzeug.serving import WSGIRequestHandler
from resources.mangas import Mangas, Manga, Chapter
from jobs.directory_manager import DirectoryManager

app = Flask(__name__)
app.secret_key = 'scrapping_master'
api = Api(app)


@app.route('/')
def home():
    return render_template('index.html')


api.add_resource(Mangas, '/mangas')
api.add_resource(Manga, '/manga/<manga>')
api.add_resource(Chapter, '/chapter/<manga>/<chapter>')

dir_manager = DirectoryManager(600, 'Manga directory', 60)
dir_manager.start()

WSGIRequestHandler.protocol_version = "HTTP/1.1"
if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=False)


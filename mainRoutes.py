from flask import render_template
from models import db


def main_data(app):
    
    @app.route('/partials/<page>')
    def load_partial(page):
        try:
            return render_template(f'partials/{page}')
        except:
            return "<p>Error: Página no encontrada.</p>", 404
        
    



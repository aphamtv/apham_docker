import time
import redis
import pandas as pd
from flask import Flask, render_template, url_for

app = Flask(__name__)
app.config['IMAGE_FOLDER'] = 'static/images'

cache = redis.Redis(host='redis', port=6379)
app.use_static = True

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    image_url = url_for('static', filename='docker_image.jpg')
    return render_template('hello.html', name='BIPM', count=count, image_url=image_url)

@app.route('/titanic')
def titanic():
    # Load the Titanic dataset using Pandas
    df = pd.read_csv('templates/titanic.csv')
    
    # Convert the first 5 rows of the DataFrame to an HTML table
    table_html = df.head().to_html()
    
    # Render the template with the table data
    return render_template('titanic.html', table_data=table_html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)

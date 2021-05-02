from flask import Flask, render_template, request, redirect, url_for, flash
import sys
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)

class City(db.Model):
    #__tablename__ = 'city'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100), unique=True, nullable=False)


def __init__(self, name):
    self.name = name


db.create_all()


@app.route('/')
def index():
    dict_with_weather_info = {}
    try:
        data = City.query.all()
        for i in data:
            print(i.name)
        API_KEY = 'e989ba91534d8556f407600379d65fdd'
        for i in data:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={i.name}&APPID={API_KEY}'

            r = requests.get(url).json()
            print(r)
            if r['cod'] == '404':
                pass
            else:
                dict_with_weather_info[i.name] = {'id': i.id,
                                                  'state': r['weather'][0]['main'],
                                                  'degrees': int(r['main']['temp'] - 273.15)}
    finally:
        print(dict_with_weather_info)
        return render_template('index.html', weather=dict_with_weather_info)


@app.route('/add', methods=['GET', 'POST'])
def add_city():
    city = request.form['city_name'].lower()
    if len(city) == 0:
        flash("The city doesn't exist!")
        return redirect('/')
    try:
        city = int(city)
        flash("The city doesn't exist!")
        return redirect('/')
    except Exception:
        try:
            name = City.query.filter_by(name=city).first()
            if city == name.name:
                flash("The city has already been added to the list!")
                return redirect('/')
        except Exception:
            API_KEY = 'e989ba91534d8556f407600379d65fdd'
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'

            r = requests.get(url).json()
            print('a')
            print(r)
            if r['cod'] == '404':
                flash("The city doesn't exist!")
                return redirect('/')
            print(city)
            city = City(name=city)
            print('b')
            print(city)
            db.session.add(city)
            db.session.commit()
            return redirect(url_for('index'))


@app.route('/delete/<city_id>', methods=['GET', 'POST'])
def delete(city_id):
    city = City.query.filter_by(id=city_id).first()
    db.session.delete(city)
    db.session.commit()
    return redirect('/')


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
        db.create_all()

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Creando una base de datos
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///taller.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Base de datos
class Conservacion(db.Model):
    Punto = db.Column(db.Integer, primary_key=True)
    Latitud = db.Column(db.Float,unique=True, nullable=False)
    Longitud = db.Column(db.Float, nullable=False)
    Dimension = db.Column(db.String(250), nullable=False)
    Descripcion = db.Column(db.String(250), nullable=False)
    Link = db.Column(db.Text(50), nullable=False)
    Coordenada = db.Column(db.Text(50), nullable=False)
db.create_all()

#Extrayendo el link con Selenium
chrome_driver_path = "C:\Portafolio\chromedriver_win32\chromedriver.exe"

#Función para extraer link de cada punto
def final(latitud, longitud):
    driver = webdriver.Chrome(chrome_driver_path)
    driver.get('https://www.google.com/maps/@-33.569697,-70.62996,17z?hl=es-ES')
    search_bar = driver.find_element_by_xpath('//*[@id="searchboxinput"]')
    search_bar.click()
    search_bar.send_keys(str(latitud) + " " + str(longitud))
    search_bar.send_keys(Keys.ENTER)
    time.sleep(3)
    coordenada = driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1/span[1]')
    coor = coordenada.text
    link = driver.current_url
    driver.close()
    return link, coor


@app.route('/')
def home():
    points = db.session.query(Conservacion).all()
    return render_template('index.html', puntos = points)

@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        final_link = final(latitud=request.form['lat'], longitud=request.form['long'])
        point = Conservacion(Latitud=request.form['lat'], 
        Longitud=request.form['long'],
        Dimension=request.form['dim'],
        Descripcion=request.form['desc'],
        Link = final_link[0],
        Coordenada = final_link[1])
        db.session.add(point)
        db.session.commit()
        return redirect(url_for('home'))
    
@app.route('/modify/<num>')
def modify(num):
    modificar = Conservacion.query.get(num)
    return render_template('modify.html',modify = modificar)

@app.route('/change/<num>', methods=["GET", "POST"])
def change(num):
    if request.method == "POST":
        point_to_update = Conservacion.query.get(num)
        # point_to_update.Latitud = request.form['lat']
        # point_to_update.Longitud = request.form['long']
        # point_to_update.Dimension = request.form['dim']
        point_to_update.Descripcion = request.form['desc']
        db.session.commit()
        return redirect(url_for('home'))

@app.route('/delete/<id>', methods=["GET", "POST"])
def delete(id):
    delete_id = id
    point_to_delete = Conservacion.query.get(delete_id)
    db.session.delete(point_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

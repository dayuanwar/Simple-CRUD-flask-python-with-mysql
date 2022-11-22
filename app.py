import os, csv, xmltodict
from flask import Flask, json, render_template, request, flash, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'imno'
app.config['MYSQL_DB'] = 'pabw_uts'
 
mysql = MySQL(app)


@app.route("/")
def index():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "CarsData", "Cars.json")
    data = json.load(open(json_url))
    title = "Show Data JSON"
    return render_template('read_file.html', data=data, title=title)

@app.route("/csv")
def page_csv():
    data = []
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    filepath = os.path.join(SITE_ROOT, "CarsData", "Cars.csv")
    with open(filepath) as file_data:
        csv_file = csv.reader(file_data)
        for index, row in enumerate(csv_file):
            if int(index) >= 1:
                object = {"Id": row[0], "Name": row[1], "Price": row[2]}
                data.append(object)

    title = "Show Data CSV"
    return render_template('read_file.html', data=data, title=title)

@app.route("/xml")
def page_xml():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    filepath = os.path.join(SITE_ROOT, "CarsData", "Cars.xml")
    with open(filepath) as file_data:
         json_data = xmltodict.parse(file_data.read())
    title = "Show Data XML"
    row_data = json_data['root']['row']
    row_data.remove(row_data[0])
    return render_template('read_file.html', data=row_data, title=title)

@app.route("/list")
def page_list():
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM cars''')
    cars = cursor.fetchall()
    cursor.close()
    return render_template('list.html', data=cars)

@app.route("/add", methods=['GET', 'POST'])
def page_add():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        brand = request.form['brand']
        model = request.form['model']
        price = request.form['price']

        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO cars(brand,model,price) VALUES(%s,%s,%s)''',(brand,model,price))
        mysql.connection.commit()
        cursor.close()
        flash('Add data success')
        return redirect(url_for('page_list'))

@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def page_edit(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute(''' SELECT * FROM cars WHERE id=%s ''', (id, ))
        data = cursor.fetchone()
        cursor.close()

        return render_template('edit.html', data=data)
    else:
        brand = request.form['brand']
        model = request.form['model']
        price = request.form['price']

        cursor = mysql.connection.cursor()
        cursor.execute(''' UPDATE cars SET brand = %s,model = %s,price = %s WHERE id = %s;''', (brand,model,price,id))
        mysql.connection.commit()
        cursor.close()
        flash('Update data success')
        return redirect(url_for('page_list'))

@app.route('/delete/<int:id>', methods=['GET'])
def page_delete(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute(''' DELETE FROM cars WHERE id=%s''', (id, ))
        mysql.connection.commit()
        cursor.close()
        flash('Delete data success')
        return redirect(url_for('page_list'))
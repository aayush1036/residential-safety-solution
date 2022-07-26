from flask import Flask, render_template, request
from objects import Person, Vehicle
from project_utils import create_connection
import mysql.connector
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/person', methods=['GET','POST'])
def register_person():
    statusCode = 'None'
    if request.method == 'POST':
        try:
            person = Person()
            person.name = request.form['name']
            person.age = int(request.form['age'])
            person.gender = request.form['gender']
            person.contact_no = '+91 '+request.form['contact']
            person.society = request.form['society']
            person.flat_no = request.form['flat']
            person.aadhar_no = request.form['aadhar']
            if not carrier._is_mobile(number_type(phonenumbers.parse(person.contact_no))):
                statusCode = 'InvalidPhoneNumber'
            if not len(person.aadhar_no) == 12 or not person.aadhar_no.isnumeric():
                statusCode = 'InvalidAadharNumber'
            else: 
                statusCode == 'Success'
                connection = create_connection()
                person.make_entry(connection=connection)
                connection.close()
            return render_template('register_person.html',statusCode=statusCode)
        except mysql.connector.errors.IntegrityError:
            statusCode = 'Exists'
            return render_template('register_person.html', statusCode=statusCode)
    return render_template('register_person.html',statusCode='StatusCode')
@app.route('/vehicle', methods=['GET','POST'])
def register_vehicle():
    statusCode = 'None'
    if request.method == 'POST':
        try:
            vehicle = Vehicle()
            vehicle.manufacturer = request.form['manufacturer']
            vehicle.model = request.form['model']
            vehicle.license_no = request.form['license']
            vehicle.society = request.form['society']
            vehicle.parking_lot_number = request.form['parking_lot']
            connection = create_connection()
            vehicle.make_entry(connection=connection)
            connection.close()
            statusCode = 'Success'
            return render_template('register_vehicle.html',statusCode=statusCode)
        except mysql.connector.errors.IntegrityError:
            statusCode = 'Exists'
            return render_template('register_vehicle.html', statusCode=statusCode)
    return render_template('register_vehicle.html',statusCode=statusCode)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request
from compute import *
import sqlite3
import re

# Create the application object
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home_page():   
    return render_template('index.html')

@app.route('/output', methods=["GET", "POST"])
def tag_output():
#       
       # Pull input
       city = request.form["city"]        
       postal_code1 = request.form["postal_code"]
       province = request.form["province"]
       size_kw = request.form["size"]
       tilt = request.form["tilt"]
       azimuth = request.form["azimuth"]
     
       city_str = '"' + city + '"'
       
       conn = sqlite3.Connection("./models/nrel_data.db")

       # clean possible whitespaces
       postal_code1 = postal_code1.strip()

       # test if the postal code with data exists in the db 
       if postal_code1 != '':
           postal_code = process_postal_code(postal_code1)
           try:
               latitude = pd.read_sql("SELECT * FROM postal_codes_on2 WHERE fsa = " + postal_code, con=conn)[['Latitude']].values[0][0]
           except IndexError:
               latitude = '' 
           try:
               nrel_data_point = pd.read_sql("SELECT * FROM nrel_data WHERE Zipcode = " + postal_code, con=conn)
           except IndexError:
               latitude = ''
       elif city != '':
            # if no postal code is provided get one by using the city info 
            try:
               postal_code1 = pd.read_sql("SELECT * FROM postal_codes_on2 WHERE place_name = " + city_str, con=conn)[['fsa']].values[0][0]
               postal_code = process_postal_code(postal_code1)
               latitude = pd.read_sql("SELECT * FROM postal_codes_on2 WHERE fsa = " + postal_code, con=conn)[['Latitude']].values[0][0]
            except IndexError:
                latitude = ''
    
       if (city != '' and postal_code != ''):
               print(city_str, postal_code)
               try:
                   latitude = pd.read_sql("SELECT * FROM postal_codes_on2 WHERE fsa = " + postal_code + " OR place_name = " + city_str, con=conn)[['Latitude']].values[0][0]
               except IndexError:
                  latitude  = ''       
               
           
       # Case if empty
       if size_kw == '' or tilt == '' or azimuth == '' or latitude  == '':
           return render_template("index.html",
                                  my_input = postal_code,
                                  my_form_result="Empty")
       else:           
           sol_energy, cost, savings, be1, be2, optimum_tilt = get_prediction(postal_code, size_kw, tilt, azimuth, latitude)
           return render_template("index.html",
                              sol_energy=round(sol_energy[0], 0),
                              savings = round(savings[0], 0),
                              cost=round(cost[0], 1),
                              #cost_ci=round(cost[0]*0.25, 0),
                              be1=round(be1[0], 0),
                              be2=round(be2[0], 0),
                              optimum_tilt=round(optimum_tilt, 0),
                              my_form_result="NotEmpty")


# start the server with the 'run()' method
if __name__ == "__main__":
    app.run(host='3.229.207.53', debug=True) #will run locally http://127.0.0.1:5000/

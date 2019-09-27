from flask import Flask, render_template, request
from compute import *

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

       print(type(size_kw))
       print(type(tilt))
       
       # Case if empty
       if postal_code1 == '':
           return render_template("index.html",
                                  my_input = postal_code,
                                  my_form_result="Empty")
       
       else:           
           postal_code = process_postal_code(postal_code1)
           sol_energy, cost, savings, be1, be2, optimum_tilt = get_prediction(postal_code, size_kw, tilt, azimuth)
           #some_output = 'yes'
           print(sol_energy)
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
    app.run(debug=True) #will run locally http://127.0.0.1:5000/


# importing the necessary dependencies
from flask import Flask, render_template, request
from flask_cors import CORS,cross_origin
import pickle

app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("Index.html")

@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
           # reading the inputs given by the user
           rate_marriage = (request.form['rate_marriage'])
           count = {'Very Poor' : 1 , 'Poor' : 2 , '50-50' : 3 , 'Good' : 4 , 'Very Good' : 5}
           key_list = list(count.keys())
           val_list = list(count.values())
           val = key_list.index(rate_marriage)
           rate = val_list[val]
           age = float(request.form['age'])
           yrs_married = float(request.form['yrs_married'])
           children = float(request.form['children'])
           religious = (request.form['religious'])
           count = {'Not Religious' : 1 , 'Weak Religious' : 2 , 'Religious' : 3 , 'Strongly Religious' : 4}
           key_list = list(count.keys())
           val_list = list(count.values())
           val = key_list.index(religious)
           Religious = val_list[val]
           educ = (request.form['educ'])
           count = {'grade school': 9 ,'high school' : 12 ,'some college' : 14,'college graduate' : 16,'some graduate school' : 17,'advanced degree' : 20}
           key_list = list(count.keys())
           val_list = list(count.values())
           val = key_list.index(educ)
           Education = val_list[val]
           affairs = float(request.form['affairs'])
           filename = 'modelForPrediction.sav'
           model = pickle.load(open(filename, 'rb'))
           scalefile = 'sandardScalar.sav'
           scalar = pickle.load(open(scalefile, 'rb'))
           scaled_data = scalar.transform([[rate,age,yrs_married,children,Religious,Education,affairs]])
           prediction = model.predict(scaled_data)
           print('prediction value is ', prediction)
           # showing the prediction results in a UI
           return render_template('predict.html', prediction = prediction)

        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)


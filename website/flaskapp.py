from flask import Flask, render_template, request, jsonify, json
import sys
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prediction/')
def prediction():
    keys = ['Johnny Depp', 'Meryl Streep', 'Leonardo DiCaprio', 'Matt Damon', 'Benedict Cumberbatch', 'Anne Hathaway', 'Christian Bale',
    'Scarlett Johansson', 'Hugh Jackman', 'Michael Caine']
    values = [1,2,3,4,5,6,7,8,9,10]

    data = []
    for i in range(len(keys)):
        tmp={}
        tmp["id"] = values[i]
        tmp["text"] = keys[i]
        data.append(tmp)
    print(json.dumps(data))

    return render_template('prediction.html', data=json.dumps(data))

@app.route('/chart/')
def chart():
    return render_template('chart.html')

@app.route('/table/')
def table():
    return render_template('table.html')

@app.route('/_return_revenue')
def return_revenue():
    moviename = request.args.get('f_moviename', 'N/A')
    budget = request.args.get('f_budget', 0, type=int)
    production = request.args.get('f_production', 'N/A')
    actors = request.args.getlist('f_actors[]')
    actors = [int(i) for i in actors]
    print('actors are', actors)

    rev = 0 
    if budget < 1000: 
    	rev+=-2000
    else: rev+=5000
    if production == 'Disney': rev+=5
    rev+=sum(actors)

    return jsonify(result=rev, mname=moviename, bdgt=budget, act=actors)

if __name__ == "__main__":
    app.run(host="127.0.0.1",
        port=int("5000"),
        debug=True)
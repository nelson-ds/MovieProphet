from flask import Flask, render_template, request, jsonify, json
import sys, pymysql
app = Flask(__name__)


connection = pymysql.connect(host='localhost', user='root', password='toor', db='movies',charset='utf8')
cur = connection.cursor()

cur.execute("select * FROM scores_act")
act_sql = []
for row in cur: act_sql.append(list(row))

cur.execute("select * FROM scores_dir")
dir_sql = []
for row in cur: dir_sql.append(list(row))

cur.execute("select * FROM scores_pro")
pro_sql = []
for row in cur: pro_sql.append(list(row))

cur.execute("select * FROM scores_wri")
wri_sql = []
for row in cur: wri_sql.append(list(row))

cur.execute("select * FROM scores_cin")
cin_sql = []
for row in cur: cin_sql.append(list(row))

cur.execute("select * FROM scores_com")
com_sql = []
for row in cur: com_sql.append(list(row))

cur.execute("select * FROM scores_dis")
dis_sql = []
for row in cur: dis_sql.append(list(row))

cur.close()
connection.close()

k_act = [item[0] for item in act_sql]
v_act = [item[1] for item in act_sql]

k_dir = [item[0] for item in dir_sql]
v_dir = [item[1] for item in dir_sql]

k_pro = [item[0] for item in pro_sql]
v_pro = [item[1] for item in pro_sql]

k_wri = [item[0] for item in wri_sql]
v_wri = [item[1] for item in wri_sql]

k_cin = [item[0] for item in cin_sql]
v_cin = [item[1] for item in cin_sql]

k_com = [item[0] for item in com_sql]
v_com = [item[1] for item in com_sql]

k_dis = [item[0] for item in dis_sql]
v_dis = [item[1] for item in dis_sql]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prediction/')
def prediction():
    data_act = []
    for i in range(len(k_act)):
        tmp={}
        tmp["id"] = v_act[i]
        tmp["text"] = k_act[i]
        data_act.append(tmp)
        # print(json.dumps(data_dir))

    data_dir = []
    for i in range(len(k_dir)):
        tmp={}
        tmp["id"] = v_dir[i]
        tmp["text"] = k_dir[i]
        data_dir.append(tmp)

    data_pro = []
    for i in range(len(k_pro)):
        tmp={}
        tmp["id"] = v_pro[i]
        tmp["text"] = k_pro[i]
        data_pro.append(tmp)

    data_wri = []
    for i in range(len(k_wri)):
        tmp={}
        tmp["id"] = v_wri[i]
        tmp["text"] = k_wri[i]
        data_wri.append(tmp)

    data_cin = []
    for i in range(len(k_cin)):
        tmp={}
        tmp["id"] = v_cin[i]
        tmp["text"] = k_cin[i]
        data_cin.append(tmp)

    data_com = []
    for i in range(len(k_com)):
        tmp={}
        tmp["id"] = v_com[i]
        tmp["text"] = k_com[i]
        data_com.append(tmp)

    data_dis = []
    for i in range(len(k_dis)):
        tmp={}
        tmp["id"] = v_dis[i]
        tmp["text"] = k_dis[i]
        data_dis.append(tmp)
	
    print('before return')	


    return render_template('prediction.html', data_act=json.dumps(data_act), data_dir=json.dumps(data_dir), 
        data_pro=json.dumps(data_pro), data_wri=json.dumps(data_wri), data_cin=json.dumps(data_cin),
        data_com=json.dumps(data_com), data_dis=json.dumps(data_dis))

    print('after return')

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
    actors = request.args.getlist('f_act[]')
    actors = [float(i) for i in actors]
    date = request.args.get('f_dat', 'N/A')
    mpaa = request.args.get('f_mpa', 'N/A')
    print('MPAA is', mpaa)
   # print('actors are', actors)

    rev = 0 
    if budget < 1000: 
    	rev+=-2000
    else: rev+=710000000
    rev+=sum(actors)

    return jsonify(result=rev, mname=moviename, bdgt=budget, act=actors)

if __name__ == "__main__":
    app.run(host="127.0.0.1",
        port=int("5000"),
        debug=True)

from flask import Flask, render_template, request, jsonify, json
import sys
import pymysql
import pickle
from datetime import datetime, timedelta
import holidays
import numpy as np
import os
from cryptography.fernet import Fernet
app = Flask(__name__)

# External Parameters
loc_dir_cur = os.path.dirname(os.path.realpath(__file__))
path_model_low = os.path.join(loc_dir_cur, "model/low_budget.mprophet")
path_model_med = os.path.join(loc_dir_cur, "model/mid_budget.mprophet")
path_model_hig = os.path.join(loc_dir_cur, "model/high_budget.mprophet")
path_knn = os.path.join(loc_dir_cur, "model/genre.mprophet")


def get_db_pwd(key, path_db_pass):
    cipher_suite = Fernet(key)
    with open(path_db_pass, 'rb') as file_object:
        for line in file_object:
            encrypted_p = line
    uncipher_text = (cipher_suite.decrypt(encrypted_p))
    return bytes(uncipher_text).decode("utf-8")


# Local
# db_host = 'localhost'
# db_user = 'root'
# path_db_pass = os.path.join(loc_dir_cur, "db/mysql_p_lcl.bin")
# db_pass = get_db_pwd(b'i_oPD0alh6eBOFLyHKUzjlhux-p5hERBWvql4SEkTuo=', path_db_pass)
# db_database = 'movies'

# Production
db_host = 'us-cdbr-east-04.cleardb.com'
db_user = 'b84dd8de4cd328'
# path_db_pass = os.path.join(loc_dir_cur, "db/mysql_p_prd.bin")
db_pass = '82b328a3'
db_database = 'heroku_3410b9f22575d67'


siz = 10

connection = pymysql.connect(host=db_host, user=db_user, password=db_pass, db=db_database, charset='utf8')
cur = connection.cursor()

cur.execute("select * FROM scores_act order by score desc")
act_sql = []
for row in cur:
    act_sql.append(list(row))
d_act = tuple(tuple(x) for x in act_sql[0:siz])

cur.execute("select * FROM scores_dir order by score desc")
dir_sql = []
for row in cur:
    dir_sql.append(list(row))
d_dir = tuple(tuple(x) for x in dir_sql[0:siz])

cur.execute("select * FROM scores_pro order by score desc")
pro_sql = []
for row in cur:
    pro_sql.append(list(row))
d_pro = tuple(tuple(x) for x in pro_sql[0:siz])

cur.execute("select * FROM scores_wri order by score desc")
wri_sql = []
for row in cur:
    wri_sql.append(list(row))
d_wri = tuple(tuple(x) for x in wri_sql[0:siz])

cur.execute("select * FROM scores_cin order by score desc")
cin_sql = []
for row in cur:
    cin_sql.append(list(row))
d_cin = tuple(tuple(x) for x in cin_sql[0:siz])

cur.execute("select * FROM scores_com order by score desc")
com_sql = []
for row in cur:
    com_sql.append(list(row))
d_com = tuple(tuple(x) for x in com_sql[0:siz])

cur.execute("select * FROM scores_dis order by score desc")
dis_sql = []
for row in cur:
    dis_sql.append(list(row))
d_dis = tuple(tuple(x) for x in dis_sql[0:siz])

cur.execute(
    "select name, score from best_genre_actors where genre='Drama' order by genre,score desc limit 5;")
gen_act_dra_sql = []
for row in cur:
    gen_act_dra_sql.append(list(row))
d_gen_act_dra = tuple(tuple(x) for x in gen_act_dra_sql)

cur.execute("select name, score from best_genre_actors where genre='Documentary' order by genre,score desc limit 5;")
gen_act_doc_sql = []
for row in cur:
    gen_act_doc_sql.append(list(row))
d_gen_act_doc = tuple(tuple(x) for x in gen_act_doc_sql)

cur.execute("select name, score from best_genre_directors where genre='Western' order by genre,score desc limit 5;")
gen_dir_wes_sql = []
for row in cur:
    gen_dir_wes_sql.append(list(row))
d_gen_dir_wes = tuple(tuple(x) for x in gen_dir_wes_sql)

cur.execute("select name, score from best_genre_directors where genre='Animation' order by genre,score desc limit 5;")
gen_dir_ani_sql = []
for row in cur:
    gen_dir_ani_sql.append(list(row))
d_gen_dir_ani = tuple(tuple(x) for x in gen_dir_ani_sql)

cur.execute(
    "select name, score from best_genre_writers where genre='Western' order by genre,score desc limit 5;")
gen_wri_wes_sql = []
for row in cur:
    gen_wri_wes_sql.append(list(row))
d_gen_wri_wes = tuple(tuple(x) for x in gen_wri_wes_sql)

cur.execute(
    "select name, score from best_genre_writers where genre='Romantic' order by genre,score desc limit 5;")
gen_wri_rom_sql = []
for row in cur:
    gen_wri_rom_sql.append(list(row))
d_gen_wri_rom = tuple(tuple(x) for x in gen_wri_rom_sql)

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
        tmp = {}
        tmp["id"] = v_act[i]
        tmp["text"] = k_act[i]
        data_act.append(tmp)
        # print(json.dumps(data_dir))

    data_dir = []
    for i in range(len(k_dir)):
        tmp = {}
        tmp["id"] = v_dir[i]
        tmp["text"] = k_dir[i]
        data_dir.append(tmp)

    data_pro = []
    for i in range(len(k_pro)):
        tmp = {}
        tmp["id"] = v_pro[i]
        tmp["text"] = k_pro[i]
        data_pro.append(tmp)

    data_wri = []
    for i in range(len(k_wri)):
        tmp = {}
        tmp["id"] = v_wri[i]
        tmp["text"] = k_wri[i]
        data_wri.append(tmp)

    data_cin = []
    for i in range(len(k_cin)):
        tmp = {}
        tmp["id"] = v_cin[i]
        tmp["text"] = k_cin[i]
        data_cin.append(tmp)

    data_com = []
    for i in range(len(k_com)):
        tmp = {}
        tmp["id"] = v_com[i]
        tmp["text"] = k_com[i]
        data_com.append(tmp)

    data_dis = []
    for i in range(len(k_dis)):
        tmp = {}
        tmp["id"] = v_dis[i]
        tmp["text"] = k_dis[i]
        data_dis.append(tmp)

    return render_template('prediction.html', data_act=json.dumps(data_act), data_dir=json.dumps(data_dir),
                           data_pro=json.dumps(data_pro), data_wri=json.dumps(data_wri), data_cin=json.dumps(data_cin),
                           data_com=json.dumps(data_com), data_dis=json.dumps(data_dis))


@app.route('/chart/')
def chart():
    return render_template('chart.html')


@app.route('/table/')
def table():
    return render_template('table.html', d_act=d_act, d_dir=d_dir, d_pro=d_pro, d_wri=d_wri, d_cin=d_cin, d_com=d_com, d_dis=d_dis,
                           d_gen_act_dra=d_gen_act_dra, d_gen_act_doc=d_gen_act_doc, d_gen_dir_wes=d_gen_dir_wes, d_gen_dir_ani=d_gen_dir_ani,
                           d_gen_wri_wes=d_gen_wri_wes, d_gen_wri_rom=d_gen_wri_rom)


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/_return_revenue')
def return_revenue():

    # loc_dir_cur = os.path.dirname(os.path.realpath(__file__))
    # loc_fil_new = os.path.join(loc_dir_cur, "new_file.txt")

    loaded_knn = pickle.load(open(path_knn, 'rb'))

    moviename = request.args.get('f_moviename', 'N/A')
    print("\nMovie Name:", moviename)

    bom_budget = request.args.get('f_budget', 0, type=float) * 1000000
    print("Budget:", bom_budget)

    genre = request.args.getlist('f_gen[]')

    genre_encoding = np.zeros(26)
    genre_dict = {"Action": 0, "Adult": 1, "Adventure": 2, "Animation": 3, "Biography": 4, "Comedy": 5,
                  "Crime": 6, "Documentary": 7, "Drama": 8, "Family": 9, "Fantasy": 10, "Film-Noir": 11, "History": 12,
                  "Horror": 13, "Music": 14, "Musical": 15, "Mystery": 16, "N/A": 17, "News": 18, "Romance": 19,
                  "Sci-Fi": 20, "Short": 21, "Sport": 22, "Thriller": 23, "War": 24, "Western": 25}
    for gen in genre:
        genre_encoding[genre_dict[gen]] = 1
    genre_encoding = genre_encoding.reshape(1, -1)
    genre_cluster = loaded_knn.predict(genre_encoding) + 1
    print(genre, genre_cluster)

    actor_score = request.args.getlist('f_act[]')
    actor_score = sum([float(i) for i in actor_score])
    print('Actor Score:', actor_score)

    director_score = request.args.getlist('f_dir[]')
    director_score = sum([float(i) for i in director_score])
    print('Director Score:', director_score)

    writer_score = request.args.getlist('f_wri[]')
    writer_score = sum([float(i) for i in writer_score])
    print('Writer Score:', writer_score)

    distributor_score = request.args.getlist('f_dis[]')
    distributor_score = sum([float(i) for i in distributor_score])
    print('Disctributor Score:', distributor_score)

    composer_score = request.args.getlist('f_com[]')
    composer_score = sum([float(i) for i in composer_score])
    print('Composer Score:', composer_score)

    cinematographer_score = request.args.getlist('f_cin[]')
    cinematographer_score = sum([float(i) for i in cinematographer_score])
    print('Cinematographer Score:', cinematographer_score)

    producer_score = request.args.getlist('f_pro[]')
    producer_score = sum([float(i) for i in producer_score])
    print('Producer Score:', producer_score)

    mpaa_rating = request.args.get('f_mpa', 'N/A')
    print('MPAA Rating:', mpaa_rating)

    date = request.args.get('f_dat')
    holiday_season = False
    print(date)
    if date != '':
        date = datetime.strptime(date, '%Y-%m-%d')
        release_month = datetime.date(date).month
        release_week_of_the_year = datetime.date(date).isocalendar()[1]
        release_quarter = (release_month-1)//3 + 1
        release_day_of_the_year = datetime.date(date).timetuple().tm_yday

        us_holidays = holidays.UnitedStates()
        for i in range(-7, 8):
            if holiday_season == True:
                break
            else:
                holiday_season = (date - timedelta(days=i)) in us_holidays

        print('Month, Week, Quarter, Day of the Year, Holiday Season:', release_month, release_week_of_the_year, release_quarter,
              release_day_of_the_year, holiday_season)
    else:
        release_month, release_week_of_the_year, release_quarter, release_day_of_the_year = '', '', '', ''
        print('No valid date entered')

    if bom_budget < 47000000:
        with open(path_model_low, 'rb') as f:
            loaded_model = pickle.load(f, encoding='latin1')  # loading python2 pickle in python3
        print('Considering Low Model')
    elif bom_budget < 117000000:
        with open(path_model_med, 'rb') as f:
            loaded_model = pickle.load(f, encoding='latin1')
        print('Considering Mid Model')
    else:
        with open(path_model_hig, 'rb') as f:
            loaded_model = pickle.load(f, encoding='latin1')
        print('Considering High Model')

    X = [bom_budget, release_month, release_week_of_the_year, release_quarter, mpaa_rating,
         holiday_season, release_day_of_the_year, actor_score, director_score, writer_score,
         distributor_score, composer_score, cinematographer_score, producer_score, genre_cluster,
         genre_cluster*actor_score, genre_cluster*writer_score, genre_cluster*director_score, genre_cluster * producer_score]

    roi = loaded_model.predict([X])[0]
    rev = roi*bom_budget
    print(bom_budget, roi, rev)

    return jsonify(result=rev, result_inc=roi, mname=moviename, bdgt=bom_budget)


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=int('8080'), debug=True)
    app.run(debug=True)  # in production environment, this is deployed via web server such as gunicorn or uWSSGI (set in app.yaml)

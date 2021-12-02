# pip install flask
# pip install psycopg2

import psycopg2
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1> Home Page </h1>"


@app.route("/<cpf>/<mes>")
def get_score_cpf(cpf, mes):
    out_score = []
    con = psycopg2.connect(host='localhost', database='sistema-score',
                           user='postgres', password='postgres')
    cur = con.cursor()
    #sql = 'create table usuarios (id serial primary key, cpf varchar(16), score INTEGER NOT NULL, mes varchar(3))'
    # cur.execute(sql)
    #sql = "insert into usuarios values (default,'123.123.123-12', 70, 'AGO' )"
    # cur.execute(sql)
    con.commit()
    cur.execute("SELECT * from usuarios WHERE cpf = '" +
                cpf+"' AND mes = '" + mes+"' ")
    recset = cur.fetchall()
    for rec in recset:
        print(rec)
        return "<h1>" + cpf + "</h1>" + "<h2>" + mes + "</h2>"

    con.close()


if __name__ == "__main__":
    app.run(debug=True)

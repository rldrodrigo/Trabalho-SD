import psycopg2
import requests

con = psycopg2.connect(host='localhost', database='sistema-score',
                       user='postgres', password='postgres')
cur = con.cursor()
#sql = 'create table usuarios (id serial primary key, cpf varchar(16), score INTEGER NOT NULL, mes varchar(3))'
# cur.execute(sql)
#sql = "insert into usuarios values (default,'12312312383', 70, 'AGO' )"
# cur.execute(sql)
con.commit()
cpf = "12312312383"
cur.execute("SELECT score from usuarios WHERE cpf = '"+cpf+"' ")
recset = cur.fetchall()
for rec in recset:
    print(rec)
con.close()

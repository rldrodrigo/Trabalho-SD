# coding: utf-8

import os
import logging
import psycopg2

import grpc
import VerificaScore_pb2
import VerificaScore_pb2_grpc

from concurrent import futures
from dotenv import load_dotenv

load_dotenv()

POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PWD = os.getenv('POSTGRES_PWD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
SERVER_PORT = os.getenv('SERVER_PORT')


class Greeter(VerificaScore_pb2_grpc.GreeterServicer):

    def SearchScore(self, request, context):
        print("[score-server]: SearchScore do CPF " + request.cpf + " via gRPC")

        con = psycopg2.connect(host=POSTGRES_HOST, database=POSTGRES_DB,
                               user=POSTGRES_USER, password=POSTGRES_PWD,
                               port=POSTGRES_PORT)
        cur = con.cursor()

        # Comandos para criação e inserção de dados no Postgres logo na instancia do server
        #sql = 'create table usuarios (id serial primary key, cpf varchar(16), score INTEGER NOT NULL, mes varchar(3))'
        # cur.execute(sql)
        #sql = "insert into usuarios values (default,'12312312383', 70, 'AGO' )"
        # cur.execute(sql)

        con.commit()
        cur.execute("SELECT * from usuarios WHERE cpf = '" +
                    request.cpf+"' AND mes = '" + request.mes+"' ")
        recset = cur.fetchall()
        for rec in recset:
            scoreRetorno = str(rec[2])
            con.close()
            return VerificaScore_pb2.ScoreReply(score=scoreRetorno)

        con.close()
        return VerificaScore_pb2.ScoreReply(score="0")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    VerificaScore_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:' + SERVER_PORT)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()

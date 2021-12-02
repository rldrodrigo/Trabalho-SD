
from concurrent import futures
import logging
import psycopg2

import grpc
import VerificaScore_pb2
import VerificaScore_pb2_grpc


class Greeter(VerificaScore_pb2_grpc.GreeterServicer):

    def SearchScore(self, request, context):
        con = psycopg2.connect(host='localhost', database='sistema-score',
                               user='postgres', password='postgres')
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
            return VerificaScore_pb2.ScoreReply(score="O Score do CPF: " + request.cpf + " é de: "+scoreRetorno)
        con.close()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    VerificaScore_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()

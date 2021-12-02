# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

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
            return VerificaScore_pb2.ScoreReply(score=scoreRetorno)
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

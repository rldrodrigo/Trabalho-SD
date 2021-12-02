
from __future__ import print_function

import logging

import grpc
import VerificaScore_pb2
import VerificaScore_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = VerificaScore_pb2_grpc.GreeterStub(channel)
        response = stub.SearchScore(
            VerificaScore_pb2.ScoreRequest(cpf='321', mes='AGO'))
    print("Greeter client received: " + response.score)


if __name__ == '__main__':
    logging.basicConfig()
    run()

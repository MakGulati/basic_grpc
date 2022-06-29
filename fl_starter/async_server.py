import asyncio
from itertools import accumulate
import logging
from urllib import response
from xmlrpc import server

import grpc
import fl_starter_pb2
import fl_starter_pb2_grpc

SERVER_ID = 1


class Trainer(fl_starter_pb2_grpc.TrainerServicer):
    async def InitialiseWeights(
        self, request: fl_starter_pb2.Request, context: grpc.aio.ServicerContext
    ) -> fl_starter_pb2.Response:
        print(
            f"printing client info inside server:{request.client_id} and {request.request_data} with {request.request_status}"
        )
        return fl_starter_pb2.Response(
            server_id=SERVER_ID, response_data=f"response from server"
        )

    async def TrainedWeights(self, request_iterator, context):
        idx = 0
        async for request in (request_iterator):
            print(
                "recv from client(%d), message= %s"
                % (request.client_id, request.request_data)
            )
            yield fl_starter_pb2.Response(
                server_id=SERVER_ID, response_data=f"response from server:{idx+10}"
            )
            idx += 1

    async def MultiResponse(self, request, context):
        print(
            f"single client request but multiple response:{request.client_id} and {request.request_data} with {request.request_status}"
        )
        for i in range(6):
            yield fl_starter_pb2.Response(
                server_id=SERVER_ID, response_data=f"response from server:{i+100}"
            )

    async def MultiRequest(self, request_iterator, context):
        accumulated_string = ""
        async for request in (request_iterator):
            print(
                "recv from client(%d), message= %s"
                % (request.client_id, request.request_data)
            )
            accumulated_string += request.request_data  # maybe await
        return fl_starter_pb2.Response(
            server_id=SERVER_ID,
            response_data=f"response from server is {accumulated_string}",
        )


async def serve() -> None:
    server = grpc.aio.server()
    fl_starter_pb2_grpc.add_TrainerServicer_to_server(Trainer(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())

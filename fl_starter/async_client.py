import asyncio
import logging
import time
from urllib import response

import grpc
from requests import request
import fl_starter_pb2
import fl_starter_pb2_grpc
import argparse


async def cool_method(stub):
    response = await stub.InitialiseWeights(
        fl_starter_pb2.Request(
            client_id=100, request_data="send model from server", request_status=1
        )
    )
    print(
        f"Greeter client received from server {response.server_id}: "
        + response.response_data
    )


async def cool_method_stream(stub, client_id):
    async def request_messages():
        for i in range(5):
            request = fl_starter_pb2.Request(
                client_id=client_id,
                request_data="send model from server",
                request_status=1,
            )
            yield request
            time.sleep(1)

    response_iterator = stub.TrainedWeights(request_messages())
    async for response in response_iterator:
        print(
            "recv from server(%d), message=%s"
            % (response.server_id, response.response_data)
        )


async def cool_multi_response(stub):
    async for response in stub.MultiResponse(
        fl_starter_pb2.Request(
            client_id=10,
            request_data="send request from MultiResponse function",
            request_status=1,
        )
    ):
        print(response.response_data)


async def cool_multi_request(stub):
    async def request_messages():

        for i in range(3):
            request = fl_starter_pb2.Request(
                client_id=500 * i,
                request_data=(f"called by Python client:{500*i+6}"),
            )
            yield request

    response = await stub.MultiRequest(request_messages())
    print(f"respnse data : {response.response_data}")


async def run(client_id: int) -> None:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = fl_starter_pb2_grpc.TrainerStub(channel)
        # await cool_method(stub)
        await cool_method_stream(stub, client_id)
        # await cool_multi_response(stub)
        # await cool_multi_request(stub)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--part_idx", type=int, help="partition_id", required=True
    )
    args_partition = parser.parse_args()
    logging.basicConfig()
    asyncio.run(run(args_partition.part_idx))

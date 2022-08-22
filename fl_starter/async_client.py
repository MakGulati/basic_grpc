import asyncio
import logging
import time

from SimpleNet import SimpleNet
import grpc
import fl_starter_pb2
import fl_starter_pb2_grpc
import argparse
import dataset
from utils import CifarClient
import torch
from RPTH.encode import json_to_pth
from RPTH.decode import pth_to_json
import json
from aiohttp_sse_client import client as sse_client
import numpy as np
from json_array import NumpyArrayEncoder
from chain_code import *
import os
DEVICE = torch.device("cpu")

ROUND = 1
round_num = 38

from RPTH.encode import json_to_pth
from RPTH.decode import pth_to_json


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
    response = await stub.InitialiseWeights(
        fl_starter_pb2.Request(
            client_id=client_id, request_data="send model from server", request_status=1
        )
    )

    decodedArrays = json.loads(response.response_data)

    finalNumpyArray = np.asarray(decodedArrays["array"],dtype=object)

    async def request_messages():

        for i in range(ROUND):
            trainloader, testloader = dataset.load(2)[client_id]

            fl_client = CifarClient(SimpleNet().to(DEVICE), trainloader, testloader)
            fl_client.set_parameters(finalNumpyArray)
            params, len_trainloader, _ = fl_client.fit(
                finalNumpyArray,
                {},
            )
         
            output_params = params

            numpyData = {"array": output_params}
            encodedLocalParam = json.dumps(numpyData, cls=NumpyArrayEncoder)
            with open(
                f"encodedLocalParam_temp_{client_id}_r_{i}.json", "w"
            ) as write_file:
                json.dump(numpyData, write_file, cls=NumpyArrayEncoder)
            hash_ipfs = add_file_to_ipfs(
                f"encodedLocalParam_temp_{client_id}_r_{i}.json", register_member()
            )
            uploadLocalModelExperimentRelated(
                str(hash_ipfs), str(round_num), str(len_trainloader), register_member(), "combine"
            )
            os.remove(f"encodedLocalParam_temp_{client_id}_r_{i}.json")
            request = fl_starter_pb2.Request(
                client_id=client_id,
                request_data=f"{encodedLocalParam}",
                request_status=len_trainloader,
            )
            yield request
            time.sleep(1)

    response_iterator = stub.TrainedWeights(request_messages())
    async for response in response_iterator:
        # print(
        #     "recv from server(%d), message=%s"
        #     % (response.server_id, response.response_data)
        # )
        print(
            f"server id: {response.server_id} and response status: {response.response_status}"
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
    print(f"response data : {response.response_data}")


async def listener():
    async with sse_client.EventSource(
        "http://34.83.215.154:4000/global-model/event"
    ) as event_source:
        try:
            async for event in event_source:
                if event.data != "":
                    return True
        except ConnectionError:
            pass


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
    # if asyncio.run(listener()):
    asyncio.run(run(args_partition.part_idx))

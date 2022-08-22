import asyncio
import logging
from urllib import response
import torch
from SimpleNet import SimpleNet
from json_array import NumpyArrayEncoder, aggregate
import numpy as np
import json
import grpc
import fl_starter_pb2
import fl_starter_pb2_grpc
from chain_code import *
import sseclient
import os

DEVICE = torch.device("cpu")

SERVER_ID = 1
results = []
round_num = 38


class Trainer(fl_starter_pb2_grpc.TrainerServicer):
    async def InitialiseWeights(
        self, request: fl_starter_pb2.Request, context: grpc.aio.ServicerContext
    ) -> fl_starter_pb2.Response:
        print(
            f"printing client info inside server:{request.client_id} and {request.request_data} with {request.request_status}"
        )
        global_weights = np.array(
            [
                val.cpu().numpy()
                for _, val in SimpleNet().to(DEVICE).state_dict().items()
            ]
        )
        numpyData = {"array": global_weights}
        encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)
        return fl_starter_pb2.Response(
            server_id=SERVER_ID, response_data=f"{encodedNumpyData}"
        )

    async def TrainedWeights(self, request_iterator, context):
        # global_weights = np.array(
        #     [
        #         val.cpu().numpy()
        #         for _, val in SimpleNet().to(DEVICE).state_dict().items()
        #     ]
        # )
        async for request in (request_iterator):
            print(
                "recv from client(%d), request_status= %s"
                % (request.client_id, request.request_status)
            )
            # results.append(
            #     (
            #         np.asarray(json.loads(request.request_data)["array"]),
            #         request.request_status,
            #     )
            # )
        url = "http://34.83.215.154:4000/local-model/event"
        headers = {"Accept": "text/event-stream"}
        client = sseclient.SSEClient(url, headers=headers)
        for msg in client:
            if msg.data != "":
                print("event fired")
                results = [
                    (
                        get_file_from_ipfs(entry["Record"]["CID"], register_member()),
                        int(entry["Record"]["numberOfExamples"]),
                    )
                    for entry in getLocalModelsFilter(
                        "combine", str(round_num), register_member()
                    )
                ]
                # results = [
                #     # get_file_from_ipfs(entry["Record"]["CID"], register_member())
                #     (entry["Record"]["CID"])
                #     for entry in getLocalModelsFilter(
                #         "combine", str(round_num), register_member()
                #     )
                # ]
                numpyAggData = {"array": aggregate(results)}
                encodedNumpyAggData = json.dumps(numpyAggData, cls=NumpyArrayEncoder)
                # print(encodedNumpyAggData)
                # with open(f"encodedNumpyAggData_r_{round_num}.json", "w") as write_file:
                #     json.dump(encodedNumpyAggData, write_file, cls=NumpyArrayEncoder)
                # hash_ipfs = add_file_to_ipfs(
                #     f"encodedNumpyAggData_r_{round_num}.json", register_member()
                # )
                # uploadGlobalModelExperimentRelated(
                #     hash_ipfs, round_num, register_member(), "combine"
                # )
                # os.remove(f"encodedNumpyAggData_r_{round_num}.json")

                yield fl_starter_pb2.Response(
                    server_id=SERVER_ID,
                    response_data=f"{21313123}",
                    response_status=83,
                )

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
            accumulated_string += request.request_data
        return fl_starter_pb2.Response(
            server_id=SERVER_ID,
            response_data=f"response from server is {accumulated_string}",
        )


async def serve() -> None:
    eventUpdate(str(round_num), "2", "combine", register_member())
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

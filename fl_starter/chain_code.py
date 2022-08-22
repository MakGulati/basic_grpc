import requests
import json
import base64
import numpy as np


def add_file_to_ipfs(filename, token):
    url = "http://34.83.215.154:4000/ipfs/add"

    payload = {}
    files = [("file", (filename, open(filename, "rb"), "application/json"))]
    authorization_token = f"Bearer {token}"
    headers = {"Authorization": authorization_token}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    return response.json()["data"]["cid"]


def get_file_from_ipfs(cid, token, file_ext="json"):
    url = "http://34.83.215.154:4000/ipfs/get"

    authorization_token = f"Bearer {token}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": str(authorization_token),
    }

    response = requests.request(
        "POST", url, headers=headers, data=json.dumps({"cid": cid, "ext": file_ext})
    )

    res_ret = response.json()["data"]["file"]
    byte_array = base64.b64decode(res_ret).decode(encoding="utf-8")
    res_dict = json.loads(byte_array)
    finalNumpyArray = np.asarray(res_dict["array"],dtype=object)
    return finalNumpyArray
    # with open(f"{cid}.{file_ext}", "w") as outfile:
    #     json.dump(res_dict, outfile)
    #     print(f"Retrieved file: {cid}.{file_ext}")


def register_member():
    url = "http://34.83.215.154:4000/users/register"

    payload = json.dumps(
        {
            "username": "mayank",
            "orgName": "Retailers",
            "attrs": [{"name": "location", "value": "RS", "ecert": True}],
            "password": "RandomPass123",
        }
    )
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.json())
    return response.json()["token"]


def write_local_model_hash(hash, round, len_data, token):

    url = "http://34.83.215.154:4000/channels/federetedlearning/chaincodes/modelsManagement/localModelInvoke"

    payload = json.dumps({"fcn": "uploadLocalModel", "args": [hash, round, len_data]})
    authorization_token = f"Bearer {token}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": str(authorization_token),
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.json())
    return response.text


def write_global_model_hash(hash, round, token):

    url = "http://34.83.215.154:4000/channels/federetedlearning/chaincodes/modelsManagement/globalmodelinvoke"

    payload = json.dumps({"fcn": "uploadGlobalModel", "args": [hash, round]})
    authorization_token = f"Bearer {token}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": str(authorization_token),
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.json())
    return response.text


def query_local_models(token):

    url = "http://34.83.215.154:4000/channels/federetedlearning/chaincodes/modelsManagement/query"

    payload = json.dumps({"fcn": "getAllLocalModels", "args": []})
    authorization_token = f"Bearer {token}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": str(authorization_token),
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.json())
    return response.text


def query_global_models(token):

    url = "http://34.83.215.154:4000/channels/federetedlearning/chaincodes/modelsManagement/query"

    payload = json.dumps({"fcn": "getAllGlobalModels", "args": []})
    authorization_token = f"Bearer {token}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": str(authorization_token),
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.json())
    return response.text


def uploadLocalModelExperimentRelated(hash, round, len_data, token, exp_id):

    url = "http://34.83.215.154:4000/channels/federetedlearning/chaincodes/modelsManagement/localModelInvoke"

    payload = json.dumps(
        {
            "fcn": "uploadLocalModelExperimentRelated",
            "fcnType": "experiment",
            "args": [hash, round, len_data, exp_id],
        }
    )
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.json())
    return response.text


def uploadGlobalModelExperimentRelated(hash, round, token, exp_id):

    url = "http://34.83.215.154:4000/channels/federetedlearning/chaincodes/modelsManagement/globalmodelinvoke"

    payload = json.dumps(
        {
            "fcn": "uploadGlobalModelExperimentRelated",
            "fcnType": "experiment",
            "args": [hash, round, exp_id],
        }
    )
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.json())
    return response.text


def eventUpdate(round, model_len, exp_id, token):
    url = "http://34.83.215.154:4000/channels/federetedlearning/chaincodes/eventsCC/invoke"

    payload = json.dumps({"fcn": "eventUpdate", "args": [round, exp_id, model_len]})
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.json())
    return response.text


def getLocalModelsFilter(exp_id, round, token):
    url = "http://34.83.215.154:4000/channels/federetedlearning/chaincodes/modelsManagement/query"

    payload = json.dumps({"fcn": "getLocalModelsFilter", "args": [exp_id, round]})
    authorization_token = f"Bearer {token}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": str(authorization_token),
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.json())
    return response.json()["result"]


if __name__ == "__main__":

    # print(
    #     [
    #         (entry["Record"]["CID"], entry["Record"]["numberOfExamples"])
    #         for entry in getLocalModelsFilter("combine", "10", register_member())[
    #             "result"
    #         ]
    #     ]
    # )

    # print(get_file_from_ipfs(
    #     getLocalModelsFilter("combine", "10", register_member())["result"][0]["Record"]["CID"],
    #     register_member(),
    # )["array"])
    print(
        get_file_from_ipfs(
            "QmQxSz3y5hCDvFoJ2oNt7iahpqVvyT7nkWfcAAuZUJyPFC", register_member()
        )
    )

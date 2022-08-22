import json
from json import JSONEncoder
import numpy
from functools import reduce
from typing import List, Optional, Tuple
import numpy as np


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def aggregate(results):
    """Compute weighted average."""
    # Calculate the total number of examples used during training
    num_examples_total = sum([num_examples for _, num_examples in results])

    # Create a list of weights, each multiplied by the related number of examples
    weighted_weights = [
        [layer * num_examples for layer in weights] for weights, num_examples in results
    ]

    # Compute average weights of each layer
    weights_prime = [
        reduce(np.add, layer_updates) / num_examples_total
        for layer_updates in zip(*weighted_weights)
    ]
    return weights_prime


if __name__ == "__main__":

    numpyArrayOne = numpy.array([[11, 22, 33], [44, 55, 66], [77, 88, 99]])

    # Serialization
    numpyData = {"array": numpyArrayOne}
    encodedNumpyData = json.dumps(
        numpyData, cls=NumpyArrayEncoder
    )  # use dump() to write array into file
    print("Printing JSON serialized NumPy array")
    print(encodedNumpyData)

    # Deserialization
    print("Decode JSON serialized NumPy array")
    decodedArrays = json.loads(encodedNumpyData)

    finalNumpyArray = numpy.asarray(decodedArrays["array"])
    print("NumPy Array")
    print(finalNumpyArray)

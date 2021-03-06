# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import fl_starter_pb2 as fl__starter__pb2


class TrainerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.InitialiseWeights = channel.unary_unary(
                '/FederatedLearning.Trainer/InitialiseWeights',
                request_serializer=fl__starter__pb2.Request.SerializeToString,
                response_deserializer=fl__starter__pb2.Response.FromString,
                )
        self.TrainedWeights = channel.stream_stream(
                '/FederatedLearning.Trainer/TrainedWeights',
                request_serializer=fl__starter__pb2.Request.SerializeToString,
                response_deserializer=fl__starter__pb2.Response.FromString,
                )
        self.MultiRequest = channel.stream_unary(
                '/FederatedLearning.Trainer/MultiRequest',
                request_serializer=fl__starter__pb2.Request.SerializeToString,
                response_deserializer=fl__starter__pb2.Response.FromString,
                )
        self.MultiResponse = channel.unary_stream(
                '/FederatedLearning.Trainer/MultiResponse',
                request_serializer=fl__starter__pb2.Request.SerializeToString,
                response_deserializer=fl__starter__pb2.Response.FromString,
                )


class TrainerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def InitialiseWeights(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TrainedWeights(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MultiRequest(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MultiResponse(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TrainerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'InitialiseWeights': grpc.unary_unary_rpc_method_handler(
                    servicer.InitialiseWeights,
                    request_deserializer=fl__starter__pb2.Request.FromString,
                    response_serializer=fl__starter__pb2.Response.SerializeToString,
            ),
            'TrainedWeights': grpc.stream_stream_rpc_method_handler(
                    servicer.TrainedWeights,
                    request_deserializer=fl__starter__pb2.Request.FromString,
                    response_serializer=fl__starter__pb2.Response.SerializeToString,
            ),
            'MultiRequest': grpc.stream_unary_rpc_method_handler(
                    servicer.MultiRequest,
                    request_deserializer=fl__starter__pb2.Request.FromString,
                    response_serializer=fl__starter__pb2.Response.SerializeToString,
            ),
            'MultiResponse': grpc.unary_stream_rpc_method_handler(
                    servicer.MultiResponse,
                    request_deserializer=fl__starter__pb2.Request.FromString,
                    response_serializer=fl__starter__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'FederatedLearning.Trainer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Trainer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def InitialiseWeights(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/FederatedLearning.Trainer/InitialiseWeights',
            fl__starter__pb2.Request.SerializeToString,
            fl__starter__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TrainedWeights(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/FederatedLearning.Trainer/TrainedWeights',
            fl__starter__pb2.Request.SerializeToString,
            fl__starter__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def MultiRequest(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/FederatedLearning.Trainer/MultiRequest',
            fl__starter__pb2.Request.SerializeToString,
            fl__starter__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def MultiResponse(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/FederatedLearning.Trainer/MultiResponse',
            fl__starter__pb2.Request.SerializeToString,
            fl__starter__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

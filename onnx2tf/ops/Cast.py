import random
random.seed(0)
import numpy as np
np.random.seed(0)
import tensorflow as tf
from onnx import TensorProto
import onnx_graphsurgeon as gs
from utils.enums import ONNX_DTYPES_TO_TF_DTYPES


def make_node(
    *,
    graph_node: gs.Node,
    tf_layers_dict: dict,
    **kwargs: dict,
):
    """Cast

    Parameters
    ----------
    graph_node: gs.Node
        graph_surgeon Node

    tf_layers_dict: dict
        optype, shape, dtype, tensorflow graph
    """
    graph_node_input: gs.Variable = graph_node.inputs[0]
    graph_node_output: gs.Variable = graph_node.outputs[0]

    shape = graph_node_output.shape
    dtype = graph_node_output.dtype

    to = graph_node.attrs.get('to', TensorProto.FLOAT)

    # Preserving Graph Structure (Dict)
    tf_layers_dict[graph_node_output.name] = {
        'optype': graph_node.op,
        'shape': shape,
        'dtype': dtype,
    }

    # Generation of TF OP
    tf_layers_dict[graph_node_output.name]['tf_node'] = \
        tf.cast(
            x=tf_layers_dict[graph_node_input.name]['tf_node'],
            dtype=ONNX_DTYPES_TO_TF_DTYPES[to],
            name=graph_node.name,
        )

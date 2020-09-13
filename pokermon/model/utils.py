from typing import Dict

import numpy as np
import tensorflow as tf


def select_proportionally(policy_probabilities: np.array) -> int:
    return np.random.choice(len(policy_probabilities), size=1, p=policy_probabilities)[
        0
    ]


def ensure_dense(t):
    if isinstance(t, tf.sparse.SparseTensor):
        return tf.sparse.to_dense(t)
    else:
        return t


def make_sequence_dict_of_dense(
    tensor_dict: Dict[str, tf.Tensor]
) -> Dict[str, tf.Tensor]:
    """
    All tensors have shape [time, 1 OR num_players]
    """
    updated_dict = {}

    for name, t in tensor_dict.items():
        t = ensure_dense(t)
        if len(t.shape) == 1:
            t = tf.expand_dims(t, -1)

        updated_dict[name] = tf.expand_dims(t, 0)

    return updated_dict


def make_context_dict_of_dense(
    tensor_dict: Dict[str, tf.Tensor]
) -> Dict[str, tf.Tensor]:
    """
    All tensors have shape [1 OR num_players]
    """
    updated_dict = {}

    for name, t in tensor_dict.items():
        t = ensure_dense(t)
        if t.shape == []:
            t = tf.expand_dims(t, 0)

        updated_dict[name] = tf.expand_dims(t, 0)

    return updated_dict


def concat_feature_tensors(tensor_dict):
    tensors = []

    for name, val in tensor_dict.items():
        val = tf.cast(val, dtype=tf.float32)
        tensors.append(val)

    return tf.concat(tensors, axis=-1)

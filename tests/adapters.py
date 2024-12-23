#!/usr/bin/env python3
from __future__ import annotations

import os
from typing import IO, BinaryIO, Iterable, Optional, Type

import numpy.typing as npt
import torch


def run_positionwise_feedforward(
    d_model: int,
    d_ff: int,
    weights: dict[str, torch.FloatTensor],
    in_features: torch.FloatTensor,
) -> torch.FloatTensor:
    """Given the weights of a position-wise feedforward network, return
    the output of your implementation with these weights.

    Args:
        d_model: int
            Dimensionality of the feedforward input and output.
        d_ff: int
            Dimensionality of the feedforward network's inner layer.
        weights: dict[str, torch.FloatTensor]
            State dict of our reference implementation.
            The keys of this dictionary are `w1.weight` and `w2.weight`.
            `w1` is the first linear transformation, and `w2` is the second
            linear transformation (eq. 2 of Vaswani et al., 2017).
            `w1.weight` is of shape (d_ff, d_model).
            `w2.weight` is of shape (d_model, d_ff).
    )
        in_features: torch.FloatTensor
            Tensor to run your implementation on.

    Returns:
        torch.FloatTensor with the output of running your position-wise feedforward network
        with the provided `weights` on the provided `in_features`.
    """
    # Example:
    # If your state dict keys match, you can use `load_state_dict()`
    # my_ffn.load_state_dict(weights)
    # You can also manually assign the weights
    # my_ffn.w1.weight.data = weights["w1.weight"]
    # my_ffn.w2.weight.data = weights["w2.weight"]
    raise NotImplementedError


def run_scaled_dot_product_attention(
    K: torch.FloatTensor,
    Q: torch.FloatTensor,
    V: torch.FloatTensor,
    mask: Optional[torch.BoolTensor] = None,
    pdrop: Optional[float] = None,
) -> torch.FloatTensor:
    """Given key (K), query (Q), and value (V) tensors, return
    the output of your scaled dot product attention implementation.

    Args:
        K: torch.FloatTensor
            Tensor with attention keys. Shape is
            (batch_size, ..., seq_len, key_dimension), where
            "..." is optional and represents any number of other
            batch dimensions (e.g., num_heads).
        Q: torch.FloatTensor
            Tensor with attention queries. Shape is
            (batch_size, ..., seq_len, key_dimension), where
            "..." is optional and represents any number of other
            batch dimensions (e.g., num_heads).
        V: torch.FloatTensor
            Tensor with attention values. Shape is
            (batch_size, ..., seq_len, value_dimension), where
            "..." is optional and represents any number of other
            batch dimensions (e.g., num_heads).
        mask: Optional[torch.BoolTensor]
            An (optional) mask of shape (seq_len, seq_len).
            Attention scores for positions with a mask value of `True` should
            be masked out, i.e., not affect the softmaxed attention probabilities.
        pdrop: Optional[float], default is None.
            If given, drop-out the attention probabilities (the softmax-normalized
            attention scores) with this rate.

    Returns:
        torch.FloatTensor of shape (batch_size, ..., seq_len, value_dimension)
        with the output of running your scaled dot product attention
        implementation with the provided key, query, and value tensors.
    """
    raise NotImplementedError


def run_multihead_self_attention(
    d_model: int,
    num_heads: int,
    attn_pdrop: float,
    weights: dict[str, torch.FloatTensor],
    in_features: torch.FloatTensor,
) -> torch.FloatTensor:
    """Given the key, query, and value projection weights of a naive unbatched
    implementation of multi-head attention, return the output of an optimized batched
    implementation. This implementation should handle the key, query, and value projections
    for all heads in a single matrix multiply.
    See section 3.2.2 of Vaswani et al., 2017.

    Args:
        d_model: int
            Dimensionality of the feedforward input and output.
        num_heads: int
            Number of heads to use in multi-headed attention.
        attn_pdrop: float
            Drop-out the attention probabilities (the softmax-normalized
            attention scores) with this rate.
        weights: dict[str, torch.FloatTensor]
            State dict of our reference implementation.
            The keys of this dictionary are:
            - `q_heads.{N}.weight`, `q_heads.{N}.weight`:
                Weights for the query projection heads.
                N is an integer from 0 to `num_heads - 1`.
                Shape of each tensor is (d_key, d_model).
            - `k_heads.{N}.weight`, `k_heads.{N}.weight`:
                Weights for the key projection heads.
                N is an integer from 0 to `num_heads - 1`.
                Shape of each tensor is (d_key, d_model).
            - `v_heads.{N}.weight`, `v_heads.{N}.weight`:
                Weights for the value projection heads.
                N is an integer from 0 to `num_heads - 1`.
                Shape of each tensor is (d_value, d_model).
            - `output_proj.weight`:
                Weight of the output projection
                (W^{O} in the original Transformer paper)
                Shape of (d_model, d_value * num_heads).
        in_features: torch.FloatTensor
            Tensor to run your implementation on.

    Returns:
        torch.FloatTensor with the output of running your optimized, batched multi-headed attention
        implementation with the given QKV projection weights and input features.
    """
    raise NotImplementedError


def run_transformer_block(
    d_model: int,
    num_heads: int,
    d_ff: int,
    attn_pdrop: float,
    residual_pdrop: float,
    weights: dict[str, torch.FloatTensor],
    in_features: torch.FloatTensor,
) -> torch.FloatTensor:
    """Given the weights of a pre-norm Transformer block and input features,
    return the output of running the Transformer block on the input features.

    Args:
        d_model: int
            The dimensionality of the Transformer block input.
        num_heads: int
            Number of heads to use in multi-headed attention. `d_model` must be
            evenly divisible by `num_heads`.
        d_ff: int
            Dimensionality of the feed-forward inner layer (section 3.3).
        attn_pdrop: float
            Drop-out the attention probabilities (the softmax-normalized
            attention scores) with this rate.
        residual_pdrop: float
            Apply dropout to the output of each sub-layer, before it
            is added to the sub-layer input and normalized (section 5.4).
        weights: dict[str, torch.FloatTensor]
            State dict of our reference implementation.
            The keys of this dictionary are:
            - `attn.q_proj.weight`
                The query projections for all `num_heads` attention heads.
                Shape is (num_heads * (d_model / num_heads), d_model).
                The rows are ordered by matrices of shape (num_heads, d_k),
                so `attn.q_proj.weight == torch.cat([q_heads.0.weight, ..., q_heads.N.weight], dim=0)`.
            - `attn.k_proj.weight`
                The key projections for all `num_heads` attention heads.
                Shape is (num_heads * (d_model / num_heads), d_model).
                The rows are ordered by matrices of shape (num_heads, d_k),
                so `attn.k_proj.weight == torch.cat([k_heads.0.weight, ..., k_heads.N.weight], dim=0)`.
            - `attn.v_proj.weight`
                The value projections for all `num_heads` attention heads.
                Shape is (num_heads * (d_model / num_heads), d_model).
                The rows are ordered by matrices of shape (num_heads, d_v),
                so `attn.v_proj.weight == torch.cat([v_heads.0.weight, ..., v_heads.N.weight], dim=0)`.
            - `attn.output_proj.weight`
                Weight of the multi-head self-attention output projection
                Shape is (d_model, (d_model / num_heads) * num_heads).
            - `ln1.weight`
                Weights of affine transform for the first RMSNorm
                applied in the transformer block.
                Shape is (d_model,).
            - `ffn.w1.weight`
                Weight of the first linear transformation in the FFN.
                Shape is (d_ff, d_model).
            - `ffn.w2.weight`
                Weight of the second linear transformation in the FFN.
                Shape is (d_model, d_ff).
            - `ln2.weight`
                Weights of affine transform for the second RMSNorm
                applied in the transformer block.
                Shape is (d_model,).
        in_features: torch.FloatTensor
            Tensor to run your implementation on.
            Shape is (batch_size, sequence_length, d_model).

    Returns:
        FloatTensor of shape (batch_size, sequence_length, d_model) with the output of
        running the Transformer block on the input features.
    """
    raise NotImplementedError


def run_transformer_lm(
    vocab_size: int,
    context_length: int,
    d_model: int,
    num_layers: int,
    num_heads: int,
    d_ff: int,
    attn_pdrop: float,
    residual_pdrop: float,
    weights: dict[str, torch.FloatTensor],
    in_indices: torch.LongTensor,
) -> torch.FloatTensor:
    """Given the weights of a Transformer language model and input indices,
    return the output of running a forward pass on the input indices.

    Args:
        vocab_size: int
            The number of unique items in the output vocabulary to be predicted.
        context_length: int,
            The maximum number of tokens to process at once.
        d_model: int
            The dimensionality of the model embeddings and sublayer outputs.
        num_layers: int
            The number of Transformer layers to use.
        num_heads: int
            Number of heads to use in multi-headed attention. `d_model` must be
            evenly divisible by `num_heads`.
        d_ff: int
            Dimensionality of the feed-forward inner layer (section 3.3).
        attn_pdrop: float
            Drop-out the attention probabilities (the softmax-normalized
            attention scores) with this rate.
        residual_pdrop: float
            Apply dropout to the sum of the token and position embeddings
            as well as the output of each sub-layer, before it is added to the
            sub-layer input and normalized (section 5.4).
        weights: dict[str, torch.FloatTensor]
            State dict of our reference implementation. {num_layers} refers to an
            integer between `0` and `num_layers - 1` (the layer index).
            The keys of this dictionary are:
            - `token_embeddings.weight`
                Token embedding matrix. Shape is (vocab_size, d_model).
            - `position_embeddings.weight`
                Positional embedding matrix. Shape is (context_length, d_model).
            - `layers.{num_layers}.attn.q_proj.weight`
                The query projections for all `num_heads` attention heads.
                Shape is (num_heads * (d_model / num_heads), d_model).
                The rows are ordered by matrices of shape (num_heads, d_k),
                so `attn.q_proj.weight == torch.cat([q_heads.0.weight, ..., q_heads.N.weight], dim=0)`.
            - `layers.{num_layers}.attn.k_proj.weight`
                The key projections for all `num_heads` attention heads.
                Shape is (num_heads * (d_model / num_heads), d_model).
                The rows are ordered by matrices of shape (num_heads, d_k),
                so `attn.k_proj.weight == torch.cat([k_heads.0.weight, ..., k_heads.N.weight], dim=0)`.
            - `layers.{num_layers}.attn.v_proj.weight`
                The value projections for all `num_heads` attention heads.
                Shape is (num_heads * (d_model / num_heads), d_model).
                The rows are ordered by matrices of shape (num_heads, d_v),
                so `attn.v_proj.weight == torch.cat([v_heads.0.weight, ..., v_heads.N.weight], dim=0)`.
            - `layers.{num_layers}.attn.output_proj.weight`
                Weight of the multi-head self-attention output projection
                Shape is ((d_model / num_heads) * num_heads, d_model).
            - `layers.{num_layers}.ln1.weight`
                Weights of affine transform for the first RMSNorm
                applied in the transformer block.
                Shape is (d_model,).
            - `layers.{num_layers}.ffn.w1.weight`
                Weight of the first linear transformation in the FFN.
                Shape is (d_ff, d_model).
            - `layers.{num_layers}.ffn.w2.weight`
                Weight of the second linear transformation in the FFN.
                Shape is (d_model, d_ff).
            - `layers.{num_layers}.ln2.weight`
                Weights of affine transform for the second RMSNorm
                applied in the transformer block.
                Shape is (d_model,).
            - `ln_final.weight`
                Weights of affine transform for RMSNorm applied to the output of the final transformer block.
                Shape is (d_model, ).
            - `lm_head.weight`
                Weights of the language model output embedding.
                Shape is (vocab_size, d_model).
        in_indices: torch.LongTensor
            Tensor with input indices to run the language model on. Shape is (batch_size, sequence_length), where
            `sequence_length` is at most `context_length`.

    Returns:
        FloatTensor of shape (batch size, sequence_length, vocab_size) with the predicted unnormalized
        next-word distribution for each token.
    """
    raise NotImplementedError


def run_rmsnorm(
    d_model: int,
    eps: float,
    weights: dict[str, torch.FloatTensor],
    in_features: torch.FloatTensor,
) -> torch.FloatTensor:
    """Given the weights of a RMSNorm affine transform,
    return the output of running RMSNorm on the input features.

    Args:
        d_model: int
            The dimensionality of the RMSNorm input.
        eps: float, default is 1e-5
            A value added to the denominator for numerical stability.
        weights: dict[str, torch.FloatTensor]
            State dict of our reference implementation.
            The keys of this dictionary are:
            - `weight`
                Weights of the RMSNorm affine transform.
                Shape is (d_model,).
        in_features: torch.FloatTensor
            Input features to run RMSNorm on. Tensor of (*, d_model), where *
            can be an arbitrary number of dimensions with arbitrary values.

    Returns:
        FloatTensor of with the same shape as `in_features` with the output of running
        RMSNorm of the `in_features`.
    """
    raise NotImplementedError


def run_gelu(in_features: torch.FloatTensor) -> torch.FloatTensor:
    """Given a tensor of inputs, return the output of applying GELU
    to each element.

    Args:
        in_features: torch.FloatTensor
            Input features to run GELU on. Shape is arbitrary.

    Returns:
        FloatTensor of with the same shape as `in_features` with the output of applying
        GELU to each element.
    """
    raise NotImplementedError


def run_get_batch(
    dataset: npt.NDArray, batch_size: int, context_length: int, device: str
) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Given a dataset (a 1D numpy array of integers) and a desired batch size and
    context length, sample language modeling input sequences and their corresponding
    labels from the dataset.

    Args:
        dataset: np.array
            1D numpy array of integer token IDs in the dataset.
        batch_size: int
            Desired batch size to sample.
        context_length: int
            Desired context length of each sampled example.
        device: str
            PyTorch device string (e.g., 'cpu' or 'cuda:0') indicating the device
            to place the sampled input sequences and labels on.

    Returns:
        Tuple of torch.LongTensors of shape (batch_size, context_length). The first tuple item
        is the sampled input sequences, and the second tuple item is the corresponding
        language modeling labels.
    """
    raise NotImplementedError


def run_softmax(in_features: torch.FloatTensor, dim: int) -> torch.FloatTensor:
    """Given a tensor of inputs, return the output of softmaxing the given `dim`
    of the input.

    Args:
        in_features: torch.FloatTensor
            Input features to softmax. Shape is arbitrary.
        dim: int
            Dimension of the `in_features` to apply softmax to.

    Returns:
        FloatTensor of with the same shape as `in_features` with the output of
        softmax normalizing the specified `dim`.
    """
    raise NotImplementedError


def run_cross_entropy(inputs: torch.FloatTensor, targets: torch.LongTensor):
    """Given a tensor of inputs and targets, compute the average cross-entropy
    loss across examples.

    Args:
        inputs: torch.FloatTensor
            FloatTensor of shape (batch_size, num_classes). inputs[i][j] is the
            unnormalized logit of jth class for the ith example.
        targets: torch.LongTensor
            LongTensor of shape (batch_size, ) with the index of the correct class.
            Each value must be between 0 and `num_classes - 1`.

    Returns:
        Tensor of shape () with the average cross-entropy loss across examples.
    """
    raise NotImplementedError


def run_gradient_clipping(parameters: Iterable[torch.nn.Parameter], max_l2_norm: float):
    """Given a set of parameters, clip their combined gradients to have l2 norm at most max_l2_norm.

    Args:
        parameters: collection of trainable parameters.
        max_l2_norm: a positive value containing the maximum l2-norm.

    The gradients of the parameters (parameter.grad) should be modified in-place.

    Returns:
        None
    """
    raise NotImplementedError


def get_adamw_cls() -> Type[torch.optim.Optimizer]:
    """
    Returns a torch.optim.Optimizer that implements AdamW.
    """
    raise NotImplementedError


def run_get_lr_cosine_schedule(
    it: int,
    max_learning_rate: float,
    min_learning_rate: float,
    warmup_iters: int,
    cosine_cycle_iters: int,
):
    """
    Given the parameters of a cosine learning rate decay schedule (with linear
    warmup) and an iteration number, return the learning rate at the given
    iteration under the specified schedule.

    Args:
        it: int
            Iteration number to get learning rate for.
        max_learning_rate: float
            alpha_max, the maximum learning rate for
            cosine learning rate schedule (with warmup).
        min_learning_rate: float
            alpha_min, the minimum / final learning rate for
            the cosine learning rate schedule (with warmup).
        warmup_iters: int
            T_w, the number of iterations to linearly warm-up
            the learning rate.
        cosine_cycle_iters: int
            T_c, the number of cosine annealing iterations.

    Returns:
        Learning rate at the given iteration under the specified schedule.
    """
    raise NotImplementedError


def run_save_checkpoint(
    model: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    iteration: int,
    out: str | os.PathLike | BinaryIO | IO[bytes],
):
    """
    Given a model, optimizer, and an iteration number, serialize them to disk.

    Args:
        model: torch.nn.Module
            Serialize the state of this model.
        optimizer: torch.optim.Optimizer,
            Serialize the state of this optimizer.
        iteration: int
            Serialize this value, which represents the number of training iterations
            we've completed.
        out: str | os.PathLike | BinaryIO | IO[bytes]
            Path or file-like object to serialize the model, optimizer, and iteration to.
    """
    raise NotImplementedError


def run_load_checkpoint(
    src: str | os.PathLike | BinaryIO | IO[bytes],
    model: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
):
    """
    Given a serialized checkpoint (path or file-like object), restore the
    serialized state to the given model and optimizer.
    Return the number of iterations that we previously serialized in
    the checkpoint.

    Args:
        src: str | os.PathLike | BinaryIO | IO[bytes]
            Path or file-like object to serialized checkpoint.
        model: torch.nn.Module
            Restore the state of this model.
        optimizer: torch.optim.Optimizer,
            Restore the state of this optimizer.
    Returns:
        int, the previously-serialized number of iterations.
    """
    raise NotImplementedError


import os
import re
from typing import Dict, List, Tuple, Optional, Iterable, Iterator

class Tokenizer:
    """
    A BPE Tokenizer that:
    1) Loads a vocabulary (int -> bytes).
    2) Loads a list of merges (pairs of bytes).
    3) Supports adding and recognizing special tokens.
    4) Can encode text to token IDs, preserving special tokens.
    5) Can decode token IDs back into text.
    6) Offers an iterative interface for encoding large streams.
    """

    def __init__(
        self,
        vocab: Dict[int, bytes],
        merges: List[Tuple[bytes, bytes]],
        special_tokens: Optional[List[str]] = None
    ):
        """
        Construct a tokenizer from a given vocabulary, list of merges, and (optionally)
        a list of special tokens.
        
        :param vocab: A dict mapping token ID (int) -> token string (as bytes).
        :param merges: A list of merges, each a tuple of (b1, b2), where b1 and b2 are bytes.
        :param special_tokens: Optional list of special tokens (strings). 
        """

        # Store the original vocab and merges
        self.id_to_token = dict(vocab)  # int -> bytes
        self.token_to_id = {v: k for k, v in self.id_to_token.items()}  # bytes -> int

        # Build a ranking dictionary from merges for quick lookup
        # merges[0] is the highest priority; merges[-1] is the lowest.
        self.bpe_ranks = {
            (pair[0], pair[1]): i for i, pair in enumerate(merges)
        }

        # Next available token ID (i.e., if we add special tokens not present in vocab)
        self.next_id = max(self.id_to_token.keys()) + 1 if self.id_to_token else 0

        # Initialize special tokens
        self.special_tokens = special_tokens or []
        self.special_tokens_bytes = [token.encode("utf-8") for token in self.special_tokens]

        # Add special tokens to the vocabulary if needed
        if self.special_tokens:
            for token_str, token_bytes in zip(self.special_tokens, self.special_tokens_bytes):
                if token_bytes not in self.token_to_id:
                    # Assign a new ID, update both dicts
                    self.id_to_token[self.next_id] = token_bytes
                    self.token_to_id[token_bytes] = self.next_id
                    self.next_id += 1

        # Compile regex pattern for special tokens
        if self.special_tokens_bytes:
            # Sort special tokens by length in descending order to handle overlapping tokens
            sorted_tokens = sorted(
                self.special_tokens_bytes, key=lambda x: len(x), reverse=True
            )
            # Escape special characters in tokens for regex
            escaped_tokens = [re.escape(token.decode("utf-8")) for token in sorted_tokens]
            pattern = "(" + "|".join(escaped_tokens) + ")"
            self.special_tokens_pattern = re.compile(pattern)
        else:
            self.special_tokens_pattern = None

    @classmethod
    def from_files(
        cls,
        vocab_filepath: str,
        merges_filepath: str,
        special_tokens: Optional[List[str]] = None
    ):
        """
        Class method that constructs and returns a Tokenizer from a serialized vocabulary and
        list of merges (in the same format that your BPE training code output),
        optionally with a list of special tokens.

        :param vocab_filepath: Path to the file containing serialized vocabulary.
        :param merges_filepath: Path to the file containing serialized merges.
        :param special_tokens: Optional list of special tokens.
        """
        # Load vocab from file
        # Here, we expect a file format where each line is "<token_id>\t<token_bytes>"
        vocab = {}
        with open(vocab_filepath, "r", encoding="utf-8") as vf:
            for line in vf:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("\t")
                if len(parts) != 2:
                    raise ValueError(
                        f"Invalid vocab line format: {line}. Expected <id>\\t<token_bytes>."
                    )
                token_id_str, token_str = parts
                token_id = int(token_id_str)
                # The token in file might be saved as a string; we convert it back to bytes
                # Assuming the tokens are stored as their literal string representations
                vocab[token_id] = token_str.encode("utf-8")

        # Load merges from file
        # We expect each line to contain "<b1> <b2>", separated by space
        merges = []
        with open(merges_filepath, "r", encoding="utf-8") as mf:
            for line in mf:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) != 2:
                    raise ValueError(
                        f"Invalid merges line format: {line}. Expected two tokens."
                    )
                b1, b2 = parts
                merges.append((b1.encode("utf-8"), b2.encode("utf-8")))

        return cls(vocab, merges, special_tokens)

    def encode(self, text: str) -> List[int]:
        """
        Encode an input string into a list of token IDs using BPE merges, preserving special tokens.

        :param text: Input string to encode.
        :return: A list of token IDs.
        """
        if self.special_tokens_pattern:
            # Split text into segments: special tokens and regular text
            segments = self.special_tokens_pattern.split(text)
        else:
            segments = [text]

        token_ids = []
        for segment in segments:
            if segment in self.special_tokens:
                # It's a special token
                token_bytes = segment.encode("utf-8")
                if token_bytes in self.token_to_id:
                    token_id = self.token_to_id[token_bytes]
                    token_ids.append(token_id)
                else:
                    raise ValueError(f"Special token not found in vocab: {segment}")
            else:
                # Regular text: apply BPE encoding
                # Basic pre-tokenization: split into bytes
                tokens = list(segment.encode("utf-8"))  # e.g., "Hello" -> [72, 101, 108, 108, 111]
                tokens = [bytes([t]) for t in tokens]

                # Now repeatedly apply BPE merges until no more merges can be applied
                merges_applied = True
                while merges_applied and len(tokens) > 1:
                    merges_applied = False
                    # We need to find all possible pairs and select the one with the highest priority (lowest rank)
                    pairs = [(tokens[i], tokens[i+1]) for i in range(len(tokens) - 1)]
                    # Find all pairs that are in the BPE ranks
                    candidate_pairs = {pair: self.bpe_ranks[pair] for pair in pairs if pair in self.bpe_ranks}
                    if not candidate_pairs:
                        break
                    # Select the pair with the lowest rank (highest priority)
                    best_pair = min(candidate_pairs, key=candidate_pairs.get)
                    best_pair_rank = candidate_pairs[best_pair]

                    # Find the first occurrence of the best pair
                    for i, pair in enumerate(pairs):
                        if pair == best_pair:
                            best_pair_index = i
                            break

                    # Merge the best pair
                    merged_token = tokens[best_pair_index] + tokens[best_pair_index + 1]
                    tokens = tokens[:best_pair_index] + [merged_token] + tokens[best_pair_index + 2:]
                    merges_applied = True

                # Convert tokens to IDs
                for t in tokens:
                    if t in self.token_to_id:
                        token_ids.append(self.token_to_id[t])
                    else:
                        # Handle unknown tokens if needed (e.g., add to vocab or fallback)
                        # For now, raise an error or use a designated <UNK> token
                        raise ValueError(f"Unknown token encountered: {t}")

        return token_ids

    def encode_iterable(self, iterable: Iterable[str]) -> Iterator[int]:
        """
        Given an iterable of strings (e.g., lines from a file), yield token IDs
        in a streaming fashion. Useful for memory-efficient tokenization of large files.

        :param iterable: An iterable of strings.
        :return: A generator of token IDs.
        """
        for text in iterable:
            # For each text, encode to a list of IDs, then yield them
            ids = self.encode(text)
            for tid in ids:
                yield tid

    def decode(self, ids: List[int]) -> str:
        """
        Decode a list of token IDs into a string.

        :param ids: A list of token IDs.
        :return: The decoded string.
        """
        # Convert each ID to bytes
        token_bytes_list = []
        for tid in ids:
            if tid not in self.id_to_token:
                # Handle unknown IDs if needed
                # For now, raise an error or use a placeholder
                raise ValueError(f"Unknown token id encountered: {tid}")
            token_bytes_list.append(self.id_to_token[tid])

        # Concatenate them and decode to string
        text = b"".join(token_bytes_list).decode("utf-8", errors="replace")
        return text


def get_tokenizer(
    vocab: dict[int, bytes],
    merges: list[tuple[bytes, bytes]],
    special_tokens: Optional[list[str]] = None,
):
    """Given a vocabulary, a list of merges, and a list of special tokens,
    return a BPE tokenizer that uses the provided vocab, merges, and special tokens.

    Args:
        vocab: dict[int, bytes]
            The tokenizer vocabulary, a mapping from int (token ID in the vocabulary)
            to bytes (token bytes)
        merges: list[tuple[bytes, bytes]]
            BPE merges. Each list item is a tuple of bytes (<token1>, <token2>),
            representing that <token1> was merged with <token2>.
            Merges are ordered by order of creation.
        special_tokens: Optional[list[str]]
            A list of string special tokens for the tokenizer. These strings will never
            be split into multiple tokens, and will always be kept as a single token.

    Returns:
        A BPE tokenizer that uses the provided vocab, merges, and special tokens.
    """
    tokenizer = Tokenizer(vocab=vocab, merges=merges, special_tokens=special_tokens)
    return tokenizer

import os
import collections
import regex as re

# A (very simple) GPT-2–style pre-tokenization regex; you can also adapt it
# if you want to mimic the exact behavior from tiktoken/pull/234:
GPT2_PAT = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""

def run_train_bpe(
    input_path: str | os.PathLike,
    vocab_size: int,
    special_tokens: list[str] = None,
    use_gpt2_pretokenizer: bool = True,
    **kwargs,
):
    """
    Given the path to an input corpus, train a BPE tokenizer and
    output its vocabulary and merges.

    This version is optimized to avoid re-counting the entire dataset
    after each merge; it incrementally updates pair frequencies.
    """
    if special_tokens is None:
        special_tokens = []

    # ----------------------------------------------------------------
    # 1. Read training data
    # ----------------------------------------------------------------
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    # ----------------------------------------------------------------
    # 2. Pre-tokenization
    # ----------------------------------------------------------------
    if use_gpt2_pretokenizer:
        pre_tokens = re.findall(GPT2_PAT, text)
    else:
        pre_tokens = text.split()

    # Filter out empty tokens
    pre_tokens = [pt for pt in pre_tokens if pt.strip()]

    # Convert each pre-token to a tuple of its bytes
    # Example: "hello" -> (b'h', b'e', b'l', b'l', b'o')
    token_sequences = []
    for pt in pre_tokens:
        pt_bytes = pt.encode("utf-8", errors="replace")
        token_sequences.append(
            tuple(bytes([b]) for b in pt_bytes)
        )

    # ----------------------------------------------------------------
    # 3. Build initial frequency table (Counter) of these byte sequences
    # ----------------------------------------------------------------
    freq = collections.Counter(token_sequences)

    # ----------------------------------------------------------------
    # 4. Initialize the base vocabulary
    # ----------------------------------------------------------------
    vocab = {}
    current_id = 0

    # Add special tokens to vocab
    for sptok in special_tokens:
        vocab[current_id] = sptok.encode("utf-8")
        current_id += 1

    # Add 256 possible single-byte tokens
    for b in range(256):
        vocab[current_id] = bytes([b])
        current_id += 1

    # The final vocabulary size = #special_tokens + 256 + #merges
    max_num_merges = vocab_size - (len(special_tokens) + 256)
    if max_num_merges < 0:
        max_num_merges = 0  # Edge case: no merges if vocab_size is too small

    merges = []

    # ----------------------------------------------------------------
    # 5. Prepare for incremental BPE training
    # ----------------------------------------------------------------
    list_of_lists = []

    # convert each unique token_tuple -> a list, keep track of freq
    unique_sequences = sorted(freq.keys())  # just to have a stable ordering
    for seq_id, token_tuple in enumerate(unique_sequences):
        # convert the tuple into a list
        list_of_lists.append(list(token_tuple))

    # pair_counts: how many times does each pair appear across all sequences,
    # weighted by freq[that sequence].
    pair_counts = collections.Counter()

    # pair_positions: maps (pair) -> list of (seq_id, position)
    # position means index in the list_of_lists[seq_id]
    pair_positions = collections.defaultdict(list)

    def add_pair(pair, seq_id, pos, count=1):
        """
        Increment pair_counts[pair] by (freq of that sequence * count).
        Also append (seq_id, pos) to pair_positions[pair].
        """
        seq_tuple = unique_sequences[seq_id]
        pair_counts[pair] += freq[seq_tuple] * count
        # We only append the position once; no need to multiply by freq
        # because we store positions in a single representative sequence.
        if count > 0:
            pair_positions[pair].append((seq_id, pos))

    # Build pair_counts and pair_positions from scratch
    for seq_id, token_list in enumerate(list_of_lists):
        seq_len = len(token_list)
        for i in range(seq_len - 1):
            pair = (token_list[i], token_list[i+1])
            add_pair(pair, seq_id, i)

    # ----------------------------------------------------------------
    # 6. BPE Training Loop
    # ----------------------------------------------------------------

    def merge_sequence_pair(seq_id, pair, new_symbol):
        """
        In the token list for seq_id, merge consecutive tokens that match `pair`
        into `new_symbol`. Then update pair_counts/pair_positions incrementally.
        """
        old_list = list_of_lists[seq_id]
        p1, p2 = pair
        i = 0
        merged_list = []
        length = len(old_list)

        while i < length:
            if i < length - 1 and (old_list[i], old_list[i+1]) == (p1, p2):
                # We will merge old_list[i] and old_list[i+1]
                merged_list.append(new_symbol)
                i += 2
            else:
                merged_list.append(old_list[i])
                i += 1

        # Now we have the new merged list
        list_of_lists[seq_id] = merged_list

    #   (1) For every sequence, if it has occurrences of `pair`, remove that entire 
    #       sequence's pairs from pair_counts (and pair_positions).
    #   (2) Perform the merges for that sequence. 
    #   (3) Re-add all pairs in the new sequence to pair_counts (and pair_positions).

    def remove_sequence_pairs(seq_id):
        """
        Remove from pair_counts/pair_positions all pair occurrences of list_of_lists[seq_id].
        """
        seq_tuple = unique_sequences[seq_id]
        seq_freq = freq[seq_tuple]
        old_list = list_of_lists[seq_id]
        for i in range(len(old_list) - 1):
            old_pair = (old_list[i], old_list[i+1])
            # Decrement
            pair_counts[old_pair] -= seq_freq
            if pair_counts[old_pair] <= 0:
                del pair_counts[old_pair]
                del pair_positions[old_pair]
            else:
                # we also remove the exact occurrence (seq_id, i) from pair_positions[old_pair]
                positions = pair_positions[old_pair]
                # remove (seq_id, i) from positions
                # typically we do a linear search, which might be slow, but it's simpler
                # and "exactly equivalent"
                # If you'd like faster removal, you can keep a specialized data structure.
                new_positions = []
                removed_once = False
                for (s_id, pos) in positions:
                    if not removed_once and s_id == seq_id and pos == i:
                        removed_once = True
                    else:
                        new_positions.append((s_id, pos))
                pair_positions[old_pair] = new_positions

    def add_sequence_pairs(seq_id):
        """
        Add all pair occurrences of list_of_lists[seq_id] to pair_counts/pair_positions.
        """
        seq_tuple = unique_sequences[seq_id]
        seq_freq = freq[seq_tuple]
        new_list = list_of_lists[seq_id]
        for i in range(len(new_list) - 1):
            new_pair = (new_list[i], new_list[i+1])
            pair_counts[new_pair] += seq_freq
            pair_positions[new_pair].append((seq_id, i))

    # We'll store a copy of the old version of list_of_lists to do removal from pair_counts
    # and pair_positions. Then we re-add for the new version.

    for _ in range(max_num_merges):
        # (a) If no pairs left, break
        if not pair_counts:
            break

        # (b) Pick the most frequent pair (tie => lexicographically largest)
        most_frequent_pair, highest_count = max(
            pair_counts.items(), 
            key=lambda x: (x[1], x[0])
        )
        if highest_count < 1:
            break  # no more merges beneficial

        merges.append(most_frequent_pair)
        new_symbol = most_frequent_pair[0] + most_frequent_pair[1]

        # (c) For every sequence that has this pair, we do a merge
        # We gather a unique set of seq_ids from pair_positions
        affected_positions = pair_positions.get(most_frequent_pair, [])
        if not affected_positions:
            # If no positions exist, just skip
            continue

        affected_seq_ids = set(seq_id for (seq_id, pos) in affected_positions)

        # We'll do removal -> merge -> re-add for each affected seq_id
        for seq_id in affected_seq_ids:
            # remove old pairs from pair_counts
            remove_sequence_pairs(seq_id)

            # merge
            merge_sequence_pair(seq_id, most_frequent_pair, new_symbol)

            # re-add pairs in the updated sequence
            add_sequence_pairs(seq_id)

        # We also add new_symbol to vocab
        vocab[current_id] = new_symbol
        current_id += 1

        # If we've reached max merges, stop
        if len(merges) >= max_num_merges:
            break

    # ----------------------------------------------------------------
    # 7. Return the final vocab and merges
    # ----------------------------------------------------------------
    return vocab, merges
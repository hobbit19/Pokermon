import argparse
import logging
import sys
from random import shuffle
from typing import List

import tensorflow as tf
from tqdm import trange

from pokermon.ai import policies
from pokermon.ai.policy import Policy
from pokermon.features.examples import make_forward_backward_example
from pokermon.poker import dealer
from pokermon.poker.deal import FullDeal
from pokermon.simulate import simulate
from pokermon.simulate.simulate import choose_starting_stacks

logger = logging.getLogger(__name__)


def write_batch(serialized_examples, directory, batch_idx):
    filename = f"{directory}/examples-{batch_idx}"
    with tf.io.TFRecordWriter(filename) as writer:
        for example in serialized_examples:
            writer.write(example)


def simulate_and_write_examples(
    directory: str,
    policies: List[Policy],
    num_hands: int,
    num_examples_per_batch: int,
):

    batch: List[str] = []
    batch_idx = 0

    for _ in trange(num_hands):

        starting_stacks = choose_starting_stacks()

        shuffle(policies)

        deal: FullDeal = dealer.deal_cards(len(policies))

        game, result = simulate.simulate(policies, starting_stacks, deal)

        for player_idx, _ in enumerate(policies):

            policy: Policy = policies[player_idx]

            example = make_forward_backward_example(
                player_idx,
                game.view(),
                deal.hole_cards[player_idx],
                deal.board,
                result,
                player_name=policy.name(),
            )

            batch.append(example.SerializeToString())

            if len(batch) == num_examples_per_batch:
                write_batch(batch, directory, batch_idx)
                batch = []
                batch_idx += 1

    # Write the final batch
    if len(batch):
        write_batch(batch, directory, batch_idx)


def main():
    parser = argparse.ArgumentParser(description="Generate examples by playing hands.")

    parser.add_argument(
        "--output_directory",
        help="Direcory where files should be written",
        type=str,
        required=True,
    )

    parser.add_argument(
        "--num_hands",
        help="Number of examples to create (hands to play)",
        type=int,
        required=True,
    )

    parser.add_argument(
        "--num_examples_per_file",
        help="Number between checkpoints",
        type=int,
        required=True,
    )

    parser.add_argument(
        "--player",
        action="append",
        help="Type of player",
        type=str,
    )

    parser.add_argument(
        "-log",
        "--log",
        help="Provide logging level. Example --log debug'",
        type=str,
        default="INFO",
    )

    args = parser.parse_args()

    # Configure the logger
    format = "[%(asctime)s] %(pathname)s:%(lineno)d %(levelname)s - %(message)s"
    log_level = getattr(logging, args.log)
    logging.basicConfig(level=log_level, format=format)

    players: List[Policy] = [policies.POLICIES[player] for player in args.player]

    simulate_and_write_examples(
        args.output_directory, players, args.num_hands, args.num_examples_per_file
    )
    sys.exit(0)


if __name__ == "__main__":
    main()

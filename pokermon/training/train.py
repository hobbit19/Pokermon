import argparse
import dataclasses
import logging
import random
import sys
from typing import Dict, Optional

from tqdm import trange

from pokermon.ai.policy import Policy
from pokermon.model import heads_up
from pokermon.model.heads_up import HeadsUpModel
from pokermon.poker import dealer
from pokermon.poker.deal import FullDeal
from pokermon.simulate import simulate
from pokermon.simulate.simulate import choose_starting_stacks
from pokermon.training.checkpointer import Checkpointer
from pokermon.training.stats import Stats

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Trainer:

    stats: Stats = dataclasses.field(default_factory=Stats)

    checkpointer: Optional[Checkpointer] = None


def train_heads_up(
    policies: Dict[str, Policy],
    num_hands_to_play: int,
    num_hands_between_checkpoints: Optional[int] = None,
):

    # Initialize the stats per hand
    trainers: Dict[str, Trainer] = {name: Trainer() for name in policies}

    logger.debug("Beginning training with %s players", len(policies))

    for player_name, model in policies.items():
        if num_hands_between_checkpoints and isinstance(model, HeadsUpModel):
            ckpt_path = f"/Users/George/Projects/pokermon/models/{model.name()}"

            trainers[player_name].checkpointer = Checkpointer(
                model=model.model, optimizer=model.optimizer, directory=ckpt_path
            )
            print(
                f"Restoring from {ckpt_path} {trainers[player_name].checkpointer.latest_checkpoint()}"
            )
            trainers[player_name].checkpointer.restore()

    for i in trange(num_hands_to_play):

        hand_index = i + 1

        starting_stacks = choose_starting_stacks()

        ((player1_name, player1_model), (player2_name, player2_model)) = random.sample(
            policies.items(), 2
        )

        deal: FullDeal = dealer.deal_cards(num_players=2)

        game, result = simulate.simulate(
            [player1_model, player2_model], starting_stacks, deal
        )

        for player_idx, player_name in enumerate([player1_name, player2_name]):

            model = policies[player_name]

            trainers[player_name].stats.update_stats(game.view(), result, player_idx)

            if isinstance(model, HeadsUpModel):
                model.train_step(
                    player_idx,
                    game.view(),
                    deal.hole_cards[player_idx],
                    deal.board,
                    result,
                )

            if (
                num_hands_between_checkpoints
                and hand_index % num_hands_between_checkpoints == 0
            ):

                print()
                print(f"Stats for {player_name}")
                trainers[player_name].stats.print_summary()
                print()
                # Reset the stats
                trainers[player_name].stats = Stats()

                if isinstance(model, HeadsUpModel):
                    trainers[player_name].checkpointer.save()


def main():
    parser = argparse.ArgumentParser(description="Play a hand of poker.")

    parser.add_argument(
        "--num_hands",
        help="Number of hands to play",
        type=int,
        default=10000,
    )

    parser.add_argument(
        "--checkpoint_every",
        help="Number between checkpoints",
        type=int,
        default=500,
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

    models = {"foo": heads_up.HeadsUpModel("Foo"), "bar": heads_up.HeadsUpModel("Bar")}

    train_heads_up(models, args.num_hands, args.checkpoint_every)

    sys.exit(0)


if __name__ == "__main__":
    main()

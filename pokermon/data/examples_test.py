from pokermon.data import reenforcement_types
from pokermon.data.examples import make_example, seq_example_to_dict
from pokermon.poker import rules
from pokermon.poker.cards import Board, FullDeal, mkcard, mkflop, mkhand
from pokermon.poker.evaluation import Evaluator
from pokermon.poker.game_runner import GameRunner


def test_fold_preflop() -> None:
    # Player 3 wins with a flopped set of jacks.
    deal = FullDeal(
        hole_cards=[mkhand("AcAd"), mkhand("AsKh"), mkhand("JcJh")],
        board=Board(flop=mkflop("KsJs3d"), turn=mkcard("7s"), river=mkcard("6s")),
    )

    game = GameRunner(starting_stacks=[200, 200, 200])
    game.start_game()
    game.bet_raise(to=10)
    game.fold()
    game.fold()

    evaluator = Evaluator()
    results = rules.get_result(deal, game.game_view(), evaluator)
    context, rows = reenforcement_types.make_rows(game.game, deal, results, evaluator)

    example = make_example(context, rows)

    example_dict = seq_example_to_dict(example)

    # Context Features
    assert example_dict["context"]["num_players"] == [3]
    assert example_dict["context"]["starting_stack_sizes"] == [200, 200, 200]

    # Player 3 (UTG) wins the blinds, the others lose their blinds
    assert example_dict["context"]["total_rewards"] == [-1, -2, 3]

    # Bet, Fold, Fold
    assert example_dict["features"]["action__action_encoded"] == [[5], [3], [3]]

    # Bet 10, fold, fold
    assert example_dict["features"]["action__amount_added"] == [[10], [0], [0]]

    # These are the states before the action (the blinds have already taken place)
    assert example_dict["features"]["state__stack_sizes"] == [
        [199, 198, 200],
        [199, 198, 190],
        [199, 198, 190],
    ]

    # Hole Cards 0: Jc Ac As
    # Hole Cards 1: Jh Ad Kh
    assert example_dict["features"]["state__hole_card_0_rank"] == [[11], [14], [14]]
    assert example_dict["features"]["state__hole_card_0_suit"] == [[2], [2], [1]]
    assert example_dict["features"]["state__hole_card_1_rank"] == [[11], [14], [13]]
    assert example_dict["features"]["state__hole_card_1_suit"] == [[4], [3], [4]]

    # These are the indices of the actions
    assert example_dict["features"]["state__action_index"] == [[3], [4], [5]]


def test_full_hand() -> None:
    # Player 3 wins with a flopped set of jacks.
    deal = FullDeal(
        hole_cards=[mkhand("AhKs"), mkhand("Kc10d"), mkhand("5h5c"), mkhand("7s3d")],
        board=Board(flop=mkflop("KdJs3d"), turn=mkcard("7s"), river=mkcard("6s")),
    )

    game = GameRunner(starting_stacks=[300, 300, 300, 300])
    game.start_game()

    # Preflop
    game.bet_raise(to=10)
    game.fold()
    game.bet_raise(to=25)
    game.call()
    game.call()

    # Flop
    game.bet_raise(to=40)
    game.call()
    game.fold()

    # Turn
    game.check()
    game.bet_raise(to=60)
    game.call()

    # River
    game.check()
    game.bet_raise(to=100)
    game.call()

    evaluator = Evaluator()
    results = rules.get_result(deal, game.game_view(), evaluator)
    context, rows = reenforcement_types.make_rows(game.game, deal, results, evaluator)

    example = make_example(context, rows)

    example_dict = seq_example_to_dict(example)

    # Context Features
    assert example_dict["context"]["num_players"] == [4]
    assert example_dict["context"]["starting_stack_sizes"] == [300, 300, 300, 300]

    # Player 3 (UTG) wins the blinds, the others lose their blinds
    assert example_dict["context"]["total_rewards"] == [250, -225, -25, 0]

    # Bet, Fold, Fold
    assert example_dict["features"]["action__action_encoded"] == [
        [5],
        [3],
        [5],
        [4],
        [4],
        [5],
        [4],
        [3],
        [4],
        [5],
        [4],
        [4],
        [5],
        [4],
    ]

    # Bet 10, fold, fold
    assert example_dict["features"]["action__amount_added"] == [
        [10],
        [0],
        [24],
        [23],
        [15],
        [40],
        [40],
        [0],
        [0],
        [60],
        [60],
        [0],
        [100],
        [100],
    ]

    # These are the states before the action (the blinds have already taken place)
    assert example_dict["features"]["state__stack_sizes"] == [
        [299, 298, 300, 300],
        [299, 298, 290, 300],
        [299, 298, 290, 300],
        [275, 298, 290, 300],
        [275, 275, 290, 300],
        [275, 275, 275, 300],
        [235, 275, 275, 300],
        [235, 235, 275, 300],
        [235, 235, 275, 300],
        [235, 235, 275, 300],
        [235, 175, 275, 300],
        [175, 175, 275, 300],
        [175, 175, 275, 300],
        [175, 75, 275, 300],
    ]

    # Hole Cards 0: Jc Ac As
    # Hole Cards 1: Jh Ad Kh
    assert example_dict["features"]["state__hole_card_0_rank"] == [
        [5],
        [7],
        [14],
        [13],
        [5],
        [14],
        [13],
        [5],
        [14],
        [13],
        [14],
        [14],
        [13],
        [14],
    ]
    assert example_dict["features"]["state__hole_card_0_suit"] == [
        [2],
        [1],
        [4],
        [2],
        [2],
        [4],
        [2],
        [2],
        [4],
        [2],
        [4],
        [4],
        [2],
        [4],
    ]
    assert example_dict["features"]["state__hole_card_1_rank"] == [
        [5],
        [3],
        [13],
        [10],
        [5],
        [13],
        [10],
        [5],
        [13],
        [10],
        [13],
        [13],
        [10],
        [13],
    ]
    assert example_dict["features"]["state__hole_card_1_suit"] == [
        [4],
        [3],
        [1],
        [3],
        [4],
        [1],
        [3],
        [4],
        [1],
        [3],
        [1],
        [1],
        [3],
        [1],
    ]

    # These are the indices of the actions
    assert example_dict["features"]["state__action_index"] == [
        [3],
        [4],
        [5],
        [6],
        [7],
        [9],
        [10],
        [11],
        [13],
        [14],
        [15],
        [17],
        [18],
        [19],
    ]

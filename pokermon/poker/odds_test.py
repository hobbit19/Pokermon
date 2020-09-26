from pokermon.poker.board import mkboard
from pokermon.poker.hands import mkhand
from pokermon.poker.odds import odds_vs_random_hand
from pokermon.poker.odds import simulate_odds


def test_evaluation_vs_random():
    res = odds_vs_random_hand(hand=mkhand("AcAd"))
    assert 0.80 < res.win_rate() < 0.90

    res = odds_vs_random_hand(hand=mkhand("AsKd"))
    assert 0.60 < res.win_rate() < 0.70

    res = odds_vs_random_hand(hand=mkhand("5h5d"))
    assert 0.55 < res.win_rate() < 0.65


def test_evaluation_vs_hand():
    res = odds_vs_random_hand(hand=mkhand("AcAd"), other_hand=mkhand("KdKs"))
    assert 0.78 < res.win_rate() < 0.88

    res = odds_vs_random_hand(hand=mkhand("TcTs"), other_hand=mkhand("8d9h"))
    assert 0.80 < res.win_rate() < 0.90

    res = odds_vs_random_hand(hand=mkhand("9d9s"), other_hand=mkhand("KcQc"))
    assert 0.47 < res.win_rate() < 0.57


def test_evaluation_with_board():
    res = odds_vs_random_hand(hand=mkhand("AcAd"), board=mkboard("3s5dTc9h"))
    assert 0.84 < res.win_rate() < 0.94

    res = odds_vs_random_hand(hand=mkhand("AcAd"), board=mkboard("AsAh3d"))
    assert res.win_rate() > 0.95


def test_evaluation_vs_hand_with_board():
    res = odds_vs_random_hand(
        hand=mkhand("AcAd"), other_hand=mkhand("KcKs"), board=mkboard("3s5s7s")
    )
    assert 0.52 < res.win_rate() < 0.62

    res = odds_vs_random_hand(
        hand=mkhand("5s8s"), other_hand=mkhand("Tc9d"), board=mkboard("6h7cTd")
    )
    assert 0.21 < res.win_rate() < 0.31

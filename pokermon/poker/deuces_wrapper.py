from typing import Tuple

import deuces
from pokermon.poker.cards import Suit, Card, Rank, Board, HoleCards, HandType

DeucesCard = int
DeucesHand = int

_SUIT_TO_DEUCES_INT = {Suit.SPADES: 1,
                       Suit.HEARTS: 2,
                       Suit.DIAMONDS: 4,
                       Suit.CLUBS: 8}

_DEUCES_INT_TO_SUIT = {v: k for k, v in _SUIT_TO_DEUCES_INT.items()}

_DEUCES_RANK_CLASS_TO_HAND = {
  1: HandType.STRAIGHT_FLUSH,  # "Straight Flush",
  2: HandType.QUADS,  # "Four of a Kind",
  3: HandType.FULL_HOUSE,  # "Full House",
  4: HandType.FLUSH,  # "Flush",
  5: HandType.STRAIGHT,  # "Straight",
  6: HandType.TRIPS,  # "Three of a Kind",
  7: HandType.TWO_PAIR,  # "Two Pair",
  8: HandType.PAIR,  # "Pair",
  9: HandType.HIGH,  # "High Card"
}


def to_decues_card(card: Card) -> DeucesCard:
  rank_int = card.rank.value() - 2
  suit_int = _SUIT_TO_DEUCES_INT[card.suit]
  return deuces.card.Card.from_rank_int_and_suit_int(rank_int, suit_int)


def to_deuces_hand(hole_cards: HoleCards) -> Tuple[DeucesCard, DeucesCard]:
  return (to_decues_card(hole_cards.left),
          to_decues_card(hole_cards.right))


def to_deuces_board(board: Board) -> Tuple[int, int, int, int, int]:
  return (to_decues_card(board.flop[0]),
          to_decues_card(board.flop[1]),
          to_decues_card(board.flop[2]),
          to_decues_card(board.turn),
          to_decues_card(board.river))


#  deuces_cards = [None, None, None, None, None]
#  for idx, card in enumerate(board.flop):
#    deuces_cards[idx] = to_decues_card(card)

#  deuces_cards.append(to_decues_card(board.turn))
#  deuces_cards.append(to_decues_card(board.river))

#  return tuple(deuces_cards)


def from_deuces_card(deuces_card: DeucesCard) -> Card:
  rank_int = deuces.Card.get_rank_int(deuces_card)
  suit_int = deuces.Card.get_suit_int(deuces_card)
  rank = Rank(rank_int + 2)
  suit = _DEUCES_INT_TO_SUIT[suit_int]
  return Card(rank=rank, suit=suit)


def from_deuces_hand_type(deuces_hand: DeucesHand) -> HandType:
  return _DEUCES_RANK_CLASS_TO_HAND[deuces_hand]
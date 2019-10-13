import logging
from typing import Optional, Tuple

from pokermon.ai.policy import Policy
from pokermon.poker import rules
from pokermon.poker.cards import HoleCards
from pokermon.poker.game import GameView, Action, Move
import re

logger = logging.getLogger(__name__)


class Human(Policy):
  _parser_call_fold = re.compile("\s*(call|fold)\s*")
  _parser_bet_raise = re.compile("\s*(bet|raise to)\s+([0-9]+)\s*")
  
  def action(self, player_index: int, hand: HoleCards, game: GameView) -> Action:
    amount_to_call = game.amount_to_call()[player_index]
    
    stack_size = game.current_stack_sizes()[player_index]
    
    def parse_action(line: str):
      
      move, amount = self.parse_move(line)
      
      logger.debug("Parsed Action: %s %s", move, amount)
      
      if move is None:
        return None
      elif move == Move.FOLD:
        return game.fold()  # Action(player_index, Move.FOLD, 0)
      elif move == Move.CHECK_CALL:
        # amount_able_to_call = min(amount_to_call, stack_size)
        # return Action(player_index, Move.CHECK_CALL, amount_able_to_call)
        return game.call()
      elif move == Move.BET_RAISE:
        return game.bet_raise(to=int(amount))
      #        amount_to_raise = min(amount, stack_size)
      #        return Action(player_index, Move.BET_RAISE, amount_to_raise)
      else:
        return None
    
    logger.debug("Getting Player Move")
    
    print("Amount to Call {} (Current Stack Size: {})".format(
      amount_to_call, stack_size))
    
    while True:
      s = input('Action> ')
      
      maybe_action = parse_action(s)
      
      if maybe_action is None:
        print("Action Not Parsed")
        continue
      
      logger.debug("Parsed Acton: %s", maybe_action)
      
      validity_result = rules.action_valid(player_index=player_index, action_index=game.timestamp,
                                           action=maybe_action, game=game)
      
      if not validity_result.is_valid():
        print("Action Invalid: %s", validity_result)
        continue
      
      return maybe_action
  
  #      s = input('Action >>')
  #      maybe_action = parse_action(s)
  
  #    return maybe_action
  
  def parse_move(self, line: str) -> Tuple[Optional[Move], Optional[int]]:
    
    # Attempt to parse call/fold
    
    match = self._parser_call_fold.match(line)  # groups(line)
    if match is not None:
      
      action = match.groups()[0]
      
      if action == 'call':
        return Move.CHECK_CALL, None
      elif action == 'fold':
        return Move.FOLD, None
      else:
        raise Exception("Invaid action")
    
    match = self._parser_bet_raise.match(line)
    if match is not None:
      action, amount = match.groups()
      
      return Move.BET_RAISE, amount
    
    return None, None

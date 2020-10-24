//use rand::{rngs::StdRng, Rng, SeedableRng};
use rs_poker::core::{Card, Deck, Flattenable, Hand, Rank, Rankable, Suit, Value};
use std::error::Error;

extern crate rand;
use rand::seq::*;
use rand::thread_rng;

/// The input of a simulation
#[derive(Debug)]
pub struct Game {
    pub hole_cards: Vec<Hand>,
    /// Flatten deck
    pub board: Vec<Card>,
}

pub fn simulate(game: Game, num_to_simulate: i64) -> Result<Vec<i64>, String> {
    // First, create the deck
    let mut deck = Deck::default();

    // Then, remove known cards
    for h in &game.hole_cards {
        if h.len() != 2 {
            return Err(String::from("Hand passed in doesn't have 2 cards."));
        }
        for c in h.iter() {
            if !deck.remove(*c) {
                return Err(format!("Card {} was already removed from the deck.", c));
            }
        }
    }

    for c in &game.board {
        if !deck.remove(*c) {
            return Err(format!("Card {} was already removed from the deck.", c));
        }
    }

    // Create a flattened deck that we can shuffle
    let mut deck: Vec<Card> = deck.into_iter().collect();
    let mut win_counts = vec![0; game.hole_cards.len()];

    // Cards to draw
    let num_cards_to_draw = 5 - game.board.len();

    //let mut rng = SeedableRng::from_seed(12);
    let mut rng = thread_rng();

    let mut deck_idx: usize = 0;

    for _ in 0..num_to_simulate {
        // We only need to re-shuffle when we get to the end of the deck
        // This is because we "Run it N Times".  This ends up having the same
        // expectation value as re-shuffling between each run.
        if deck_idx + num_cards_to_draw >= deck.len() {
            // Shuffle the deck
            deck.shuffle(&mut rng);
            deck_idx = 0;
        }

        let next_cards = &deck[deck_idx..deck_idx + num_cards_to_draw];
        deck_idx += num_cards_to_draw;

        let mut ranks: Vec<Rank> = vec![];

        for (hole_cards) in game.hole_cards.iter() {
            let mut hand: Vec<Card> = hole_cards.iter().map(|c| c.clone()).collect();
            hand.reserve_exact(7);
            for c in &game.board {
                hand.push(*c);
            }
            for c in next_cards {
                hand.push(c.clone());
            }
            ranks.push(hand.rank());
        }

        // TODO: Handle ties
        let winner_idx = ranks
            .iter()
            .enumerate()
            .max_by_key(|&(_, ref rank)| rank.clone())
            .ok_or_else(|| String::from("Unable to determine best rank."))?
            .0;

        win_counts[winner_idx] += 1;
    }
    Ok(win_counts)
}

#[cfg(test)]
mod test {
    use super::*;
    use crate::core::Hand;
    use crate::core::Rank;

    #[test]
    fn test_simulate_pocket_pair() {
        let hands = ["AdAh", "2c2s"]
            .iter()
            .map(|s| Hand::new_from_str(s).unwrap())
            .collect();
        let mut g = Game {
            hole_cards: hands,
            board: vec![],
        };
        let result = simulate(game, 1).unwrap();
        assert!(result.1 >= Rank::OnePair(0));
    }
}

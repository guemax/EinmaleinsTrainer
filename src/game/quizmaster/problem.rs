use std::ops::RangeInclusive;
use rand::Rng;


pub enum Difficulty {
    Easy,
    Medium,
    Difficult
}


pub struct Problem {
    pub factors: (u32, u32),
    pub product: u32,
}

impl Problem {
    pub fn generate(difficulty: Difficulty) -> Self {
        let factors = match difficulty {
            Difficulty::Easy => (random(1..=10), random(1..=10)),
            Difficulty::Medium => {
                // Use complete small multiplication table but only add squares between ten and
                // twenty as well for this level of difficulty
                let first_factor: u32 = random(1..=20);
                let second_factor: u32;
                if let 1..=10 = first_factor {
                    second_factor = random(1..=10);
                } else {
                    second_factor = first_factor;
                }
                (first_factor, second_factor)
            },
            Difficulty::Difficult => (random(1..=20), random(1..=20)),
        };
        let product = factors.0 * factors.1;

        Self {
            factors,
            product,
        }
    }
}

fn random(range: RangeInclusive<u32>) -> u32 {
    rand::thread_rng().gen_range(range)
}
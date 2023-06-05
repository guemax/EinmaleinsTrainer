pub mod quizmaster;
pub mod draw;

use crate::draw::Color;
use quizmaster::problem::{Problem, Difficulty};
use quizmaster::answer;


pub fn start() {
	loop {
		let problem = Problem::generate(Difficulty::Medium);
		draw::question(&problem);

		let answer = answer::get();

		match answer {
			Err(_) => draw::after_answer(format!("✘ (Bitte gib eine Zahl als Antwort ein.) "), Color::Red),
			Ok(answer) => {
				if answer.jump_to_new_round == true {
					draw::newline();
					continue;
				}
				let expected_answer = problem.product;
				if answer.value == expected_answer {
					draw::after_answer("✔".to_string(), Color::Green);
				} else {
					let text = format!("✘ (Richtige Antwort: {})", expected_answer);
					draw::after_answer(text, Color::Red);
				}
			}
		}
    }
}

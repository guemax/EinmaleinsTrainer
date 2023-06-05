use std::io;
use std::num::ParseIntError;

use ctrlc;

pub mod align_equation;
mod draw;
mod problem;

use draw::Color;

use crate::problem::{Problem, Difficulty};


#[derive(PartialEq)]
enum JumpToNewRound {
	Yes,
	No
}

struct Answer {
	jump: JumpToNewRound,
	value: u32
}


fn get_answer() -> Result<Answer, ParseIntError> {
	let mut answer = String::new();

	io::stdin().read_line(&mut answer).expect("Die Anwort konnte nicht gelesen werden.");
	if let "q" = answer.trim().to_lowercase().as_str() {
		draw::text("\nWollen Sie das Training wirklich beenden? [j/N] ".to_string(), Color::Yellow);

		let mut answer = String::new();
		io::stdin().read_line(&mut answer).expect("Die Eingabe konnte nicht gelesen werden.");
		if "j" == answer.trim().to_lowercase().as_str() {
			draw::farewell();
		} else if "n" == answer.trim().to_lowercase().as_str() {
			return Ok(Answer { jump: JumpToNewRound::Yes, value: 0 });
		}
	}

	let answer: u32 = answer.trim().parse()?;
	return Ok(Answer{ jump: JumpToNewRound::No, value: answer});
}


fn game_loop() {
	loop {
		let problem = Problem::generate(Difficulty::Medium);
		draw::question(&problem);

		let answer = get_answer();

		match answer {
			Err(_) => draw::after_answer(format!("✘ (Bitte gib eine Zahl als Antwort ein.) "), Color::Red),
			Ok(answer) => {
				if answer.jump == JumpToNewRound::Yes {
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


fn main() {
	ctrlc::set_handler(move || {
		println!();
		draw::farewell();
	}).expect("Ctrl+C Eventhandler konnte nicht eingerichtet werden.");

	draw::greeting();
	game_loop();
	draw::farewell();
}

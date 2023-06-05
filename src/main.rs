use std::io;
use std::io::Write;
use std::num::ParseIntError;
use std::process::exit;

use ctrlc;

use rand::Rng;

pub mod align_equation;
mod draw;
use draw::Color;

use align_equation::align_equation_at_equal_sign_and_at_multiplication_sign;


fn generate_numbers() -> (u32, u32) {
    (rand::thread_rng().gen_range(1..=10), rand::thread_rng().gen_range(1..=10))
}


pub struct Problem {
	factors: (u32, u32),
	product: u32
}


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
		println!();
		print!("Wollen Sie das Training wirklich beenden? [j/N] ");
		io::stdout().flush().unwrap();

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
		let (first_factor, second_factor) = generate_numbers();
		let product = first_factor * second_factor;

		let problem = Problem{factors: (first_factor, second_factor), product };
		draw::question(problem);

		let answer = get_answer();

		match answer {
			Err(_) => draw::after_answer(format!("✘ (Bitte gib eine Zahl als Antwort ein.) "), Color::Red),
			Ok(answer) => {
				if answer.jump == JumpToNewRound::Yes {
					println!();
					continue;
				}
				let expected_answer = product;
				if answer.value == expected_answer {
					draw::after_answer("✔".to_string(), Color::Green);
				} else {
					let text = format!("✘ (Richtige Antwort: {})", product);
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

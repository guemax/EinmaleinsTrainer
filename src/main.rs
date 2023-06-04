use std::io;
use std::io::Write;
use std::num::ParseIntError;

extern crate termion;
use termion::color;

use rand::Rng;

pub mod align_equation;
use align_equation::align_equation_at_equal_sign_and_at_multiplication_sign;

fn print_after_answer(text: String) {
    println!(
	"{}{}{}{text}",
	termion::cursor::Up(1), termion::cursor::Right(20),
	termion::clear::AfterCursor);
}


fn fg_green(text: String) -> String {
    format!("{}{text}{}", color::Fg(color::Green), color::Fg(color::Reset))
}


fn fg_red(text: String) -> String{
    format!("{}{text}{}", color::Fg(color::Red), color::Fg(color::Reset))
}


fn generate_numbers() -> (u32, u32) {
    (rand::thread_rng().gen_range(1..=10), rand::thread_rng().gen_range(1..=10))
}


fn start_up_message() {
	println!("Dies ist der Einmaleins-Trainer v{}.", env!("CARGO_PKG_VERSION"));
    println!("Das Training wird nun gestartet. (Drücken Sie Ctrl+C zum Beenden.)\n");
}


fn exit_message() {
    println!("\nSie haben 9 von 10 Fragen richtig beanwortet. Dies entspricht einer Erfolgsrate von 90%.");
    println!("Herzlichen Glückwunsch!");
}


fn ask_question(first_factor: u32, second_factor: u32, product: u32) {
	let indentation = "    ";

	print!("{}{}", indentation, align_equation_at_equal_sign_and_at_multiplication_sign(first_factor, second_factor, product));
	io::stdout().flush().unwrap();
}


fn get_answer() -> Result<u32, ParseIntError> {
	let mut answer = String::new();

	io::stdin().read_line(&mut answer).expect("Die Anwort konnte nicht gelesen werden.");
	let answer: u32 = answer.trim().parse()?;
	return Ok(answer);
}


fn main() {
    start_up_message();

    loop {
		let (first_factor, second_factor) = generate_numbers();
		let product = first_factor * second_factor;

		ask_question(first_factor, second_factor, product);
		let answer = get_answer();

		match answer {
			Err(_) => print_after_answer(fg_red(format!("✘ Bitte gib eine Zahl als Antwort ein."))),
			Ok(answer) => {
				let expected_answer = product;
				if answer == expected_answer {
					print_after_answer(fg_green("✔".to_string()));
				} else {
					let text = format!("✘ (Richtige Antwort: {})", product);
					print_after_answer(fg_red(text));
				}
			}
		}
    }

    println!("\nWollen sie das Training wirklich beenden? [j/N]");
	exit_message();
}

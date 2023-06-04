use std::io;
use std::io::Write;

extern crate termion;
use termion::{color, style};


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


fn align_equation_at_equal_and_multiplication_sign(num_1: u32, num_2: u32, result: u32) -> String {
    let mut num_1_string: String = "".to_string();
    let mut num_2_string: String = "".to_string();
    let mut result_string: String = "".to_string();

    num_1_string = match num_1.to_string().len() {
	1 => format!(" {num_1}"),
	2 => format!("{num_1}"),
	_ => todo!()
    };
    num_2_string = match num_2.to_string().len() {
	1 => format!("{num_2} "),
	2 => format!("{num_2}"),
	_ => todo!()
    };
    result_string = match result.to_string().len() {
	1 => format!("  "),
	2 => format!(" "),
	3 => format!(""),
	_ => todo!()
    };
    return format!("{num_1_string} ✕ {num_2_string} = {result_string}");
}


fn main() {
    println!("Dies ist der Einmaleins-Trainer v{}.", env!("CARGO_PKG_VERSION"));
    println!("Das Training wird nun gestartet. (Drücken Sie Ctrl+C zum Beenden.)\n");

    let indentation = "    ";

    loop {
	let num_1 = 7;
	let num_2 = 10;

	print!("{}{}", indentation, align_equation_at_equal_and_multiplication_sign(num_1, num_2, num_1 * num_2));
	std::io::stdout().flush().unwrap();

	let mut answer = String::new();
	io::stdin()
	    .read_line(&mut answer)
	    .expect("Antwort konnte nicht eingelesen werden.");
	
	let answer: u32 = match answer.trim().parse() {
	    Ok(answer) => answer,
	    Err(_) => {
		println!("{}Bitte gib eine Zahl als Antwort ein.{}", color::Fg(color::Red), color::Fg(color::Reset));
		continue;
	    }
	};
	
	if answer == (num_1 * num_2) {
	    print_after_answer(fg_green("✔".to_string()));
	} else {
	    let text = format!("✘ (Richtige Antwort: {})", num_1 * num_2);
	    print_after_answer(fg_red(text));
	}
    }

    println!("\nWollen sie das Training wirklich beenden? [j/N]");
    println!("\nSie haben 9 von 10 Fragen richtig beanwortet. Dies entspricht einer Erfolgsrate von 90%.");
    println!("Herzlichen Glückwunsch!");
}

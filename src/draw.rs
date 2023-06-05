use std::process::exit;

extern crate termion;
use termion::{color, cursor, clear};


pub fn greeting() {
	println!("Dies ist der Einmaleins-Trainer v{}.", env!("CARGO_PKG_VERSION"));
    println!("Das Training wird nun gestartet. (Drücken Sie q zum Beenden.)\n");
}


pub fn farewell() {
    println!("\nSie haben 9 von 10 Fragen richtig beanwortet. Dies entspricht einer Erfolgsrate von 90%.");
    println!("Herzlichen Glückwunsch!");
	exit(0);
}


pub enum Color {
    Green,
    Red,
}


pub fn after_answer(text: String, color: Color) {
    println!("{}{}{}{}", cursor::Up(1), cursor::Right(20), clear::AfterCursor, styled(text, color))
}


fn styled(text: String, color: Color) -> String {
    let fg_color= match color {
        Color::Red => color::Fg(color::Red).to_string(),
        Color::Green => color::Fg(color::Green).to_string()
    };
    let reset_color = color::Fg(color::Reset);
    return format!("{}{}{}", fg_color, text, reset_color);
}

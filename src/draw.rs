extern crate termion;
use termion::{color, cursor, clear};


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

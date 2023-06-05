use std::{io, num::ParseIntError};

use crate::game::draw;
use draw::Color;


pub struct Answer {
	pub jump_to_new_round: bool,
	pub value: u32,
}


pub fn get() -> Result<Answer, ParseIntError> {
    let mut answer = String::new();

    io::stdin().read_line(&mut answer).expect("Die Anwort konnte nicht gelesen werden.");
    if let "q" = answer.trim().to_lowercase().as_str() {
        draw::text("\nWollen Sie das Training wirklich beenden? [j/N] ".to_string(), Color::Yellow);

        let mut answer = String::new();
        io::stdin().read_line(&mut answer).expect("Die Eingabe konnte nicht gelesen werden.");
        if "j" == answer.trim().to_lowercase().as_str() {
            draw::farewell();
        } else if "n" == answer.trim().to_lowercase().as_str() {
            return Ok(Answer { jump_to_new_round: true, value: 0 });
        }
    }

    let answer: u32 = answer.trim().parse()?;
    return Ok(Answer{ jump_to_new_round: false, value: answer});
}

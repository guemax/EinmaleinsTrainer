use ctrlc;

pub mod game;
use game::draw;


fn main() {
	ctrlc::set_handler(move || {
		draw::newline();
		draw::farewell();
	}).expect("Ctrl+C Eventhandler konnte nicht eingerichtet werden.");

	draw::greeting();
	game::start();
	draw::farewell();
}

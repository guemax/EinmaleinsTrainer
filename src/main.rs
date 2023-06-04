fn main() {
    println!("Dies ist der Einmaleins-Trainer v{}.", env!("CARGO_PKG_VERSION"));
    println!("Das Training wird nun gestartet. (Drücken Sie Ctrl+C zum Beenden.)\n");

    let indentation = "    ";

    loop {
	let num_1 = 7;
	let num_2 = 5;
	println!("{indentation}{num_1} ✕ {num_2} = ");
	break;
    }

    println!("\nWollen sie das Training wirklich beenden? [j/N]");
    println!("\nSie haben 9 von 10 Fragen richtig beanwortet. Dies entspricht einer Erfolgsrate von 90%.");
    println!("Herzlichen Glückwunsch!");
}

pub fn align_equation_at_equal_sign_and_at_multiplication_sign(first_factor: u32,
                                                           second_factor: u32,
                                                           product: u32) -> String {
    format!("{} ✕ {} = {}",
			format_first_factor(first_factor),
			format_second_factor(second_factor),
			format_product_placeholder(product))
}


fn format_first_factor(first_factor: u32) -> String {
	if is_single_digit(first_factor) {
		format!(" {first_factor}")
	} else {
		format!("{first_factor}")
	}
}


fn is_single_digit(number: u32) -> bool {
	number.to_string().len() == 1
}


fn format_second_factor(second_factor: u32) -> String {
	if is_single_digit(second_factor) {
		format!("{second_factor} ")
	} else {
		format!("{second_factor}")
	}
}

fn format_product_placeholder(product: u32) -> String {
	if is_single_digit(product) {
		format!("  ")
	} else if is_double_digit(product) {
		format!(" ")
	} else {
		format!("")
	}
}


fn is_double_digit(number: u32) -> bool {
	number.to_string().len() == 2
}

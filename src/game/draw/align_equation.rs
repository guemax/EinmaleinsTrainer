use crate::game::Problem;


pub fn align_equation_at_equal_sign_and_at_multiplication_sign(problem: &Problem) -> String {
	// Equation is going to look like this:
	//     1 ✕ 1  =   1
	//     1 ✕ 10 =  10
	//    10 ✕ 1  =  10
	//    10 ✕ 10 = 100
    format!("{} ✕ {} = {}",
			format_first_factor(problem.factors.0),
			format_second_factor(problem.factors.1),
			format_product_placeholder(problem.product))
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


#[cfg(test)]
mod tests {
	use crate::align_equation::{is_double_digit, is_single_digit};

	#[test]
	fn is_single_digit_returns_true() {
		for i in 1..=9 {
			assert_eq!(is_single_digit(i), true);
		}
	}
	#[test]
	fn is_single_digit_returns_false() {
		for i in 10..=20 {
			assert_eq!(is_single_digit(i), false);
		}
	}

	#[test]
	fn is_double_digit_returns_true() {
		for i in 10..=20 {
			assert_eq!(is_double_digit(i), true);
		}
	}
	#[test]
	fn is_double_digit_returns_false() {
		for i in 1..=9 {
			assert_eq!(is_double_digit(i), false);
		}
	}
}

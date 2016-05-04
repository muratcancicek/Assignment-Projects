//============================================================================
// Name        : evaluate.cpp
// Author      : Hasan Sozer
// Version     : 1.0
// Copyright   : (c) 2012 Ozyegin University
// Description : Includes the main function that will be used as part of the
//               program to be submitted as Homework 2, which is assigned in the 
//               context of the course CS201, Data Structures and Algorithms.
//				 Asks for an arithmetic expression from the user in infix form.
//				 Prints out the expression in postfix form, evaluates the 
//				 expression and also prints out the result.
//============================================================================

/* Coded by Muratcan Çiçek S004233 Computer Science */

#include <iostream>
#include <string>
#include <sstream>
#include "Calculator.h"

int main ()
{
	string infixExpression;

	cout << "Enter an arithmetic expression ";
	cout << "(operators and operands must be separated with a space character and the expression must end with a \';\' character)";
	cout << endl << ": ";
	getline(cin, infixExpression);

	Calculator *calc = new Calculator(infixExpression);
	
	cout << "Postfix form: " << calc->getPostfix() << endl;
	cout << "Result: " << calc->calculate() << endl;	
	
	delete calc;
	return 0;
}

//============================================================================
// Name        : Calculator.h
// Author      : Hasan Sozer
// Version     : 1.0
// Copyright   : (c) 2012 Ozyegin University
// Description : Includes the header file of the Calculator class that will be 
//               used as part of the program to be submitted as Homework 2,  
//               which is assigned in the context of the course CS201, 
//				 Data Structures and Algorithms.
//============================================================================

/* Coded by Muratcan Çiçek S004233 Computer Science */

#include <string>
#include "Stack.h"

using namespace std;

class Calculator {
public:
	Calculator(string); // constructor that takes an arithmetic expression in infix representation
	~Calculator(); // destructor
	string getPostfix(); // returns the postfix representation of the arithmetic expression
	int calculate(); // evaluates and returns the result of the arithmetic expression
private:
	Stack *stack; // stack to be used for infix-postfix conversion and evaluation of an arithmetic expression
	string postfixExpression; // keeps a postfix representation of the arithmetic expression
	string infixExpression; // keeps an infix representation of the arithmetic expression 
};

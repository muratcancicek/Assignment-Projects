/* Coded by Muratcan Çiçek S004233 Computer Science */

#include "Calculator.h" 

Calculator::Calculator(string infixExp)
{
	stack = new Stack(); 
	int i = 0;
	string token = "";

	while (infixExp.at(i) != ';') {
		if (infixExp.at(i) != ' ')
		{
			token += infixExp.at(i);
		}
		else
		{
			StackItem* item = new StackItem(token);
			token = "";
			if (!item->isOperator){
				postfixExpression += item->toString() + ' '; 
			}
			else if (stack->isEmpty())
			{
				stack->push(item);
			}
			else if (item->op < OPERATOR_LEFTPAR){

				if (!stack->isEmpty())
				{
					if (stack->top()->op != OPERATOR_LEFTPAR)
					{
						if (item->op <= stack->top()->op || item->op / 2 == stack->top()->op / 2)
						{
							postfixExpression += stack->top()->toString() + ' ';
							delete stack->pop();
						} 
					}
				} 
					stack->push(item);
			}
			else if (item->op == OPERATOR_LEFTPAR)
			{
				stack->push(item);
			}
			else if (item->op == OPERATOR_RIGHTPAR)
			{
				while(stack->top()->op != OPERATOR_LEFTPAR)
				{
					postfixExpression += stack->top()->toString() + ' ';
					delete stack->pop();
					if (stack->isEmpty())
						break;  
				}
				if (!stack->isEmpty())
				{
					if (stack->top()->op == OPERATOR_LEFTPAR)
					{
						delete stack->pop();
					}
				}
			}
		}
		i++;
	}
	while (!stack->isEmpty())
	{
		postfixExpression += stack->top()->toString() + ' ';
		delete stack->pop();
	} 

	postfixExpression += ";";
}
  
int Calculator::calculate()
{
	// stack already initialised in the constructor, used and fully emptied up to now; 
	int i = 0, result = 0, num1 = 0; 
	string token = "";

	while (postfixExpression.at(i) != ';') {
		if (postfixExpression.at(i) != ' ')
		{
			token += postfixExpression.at(i);
		}
		else
		{
			StackItem* item = new StackItem(token);
			token = "";
			if (!item->isOperator){ 
				stack->push(item);
			}
			else 
			{
				num1 = stack->top()->n;
				delete stack->pop();
				result = stack->top()->n;
				delete stack->pop();

				switch (item->op) {
				case OPERATOR_MINUS:
					result -= num1; 
					break;
				case OPERATOR_PLUS: 
					result += num1;
					break;
				case OPERATOR_DIVISION:
					result /= num1;
					break;
				case OPERATOR_MULTIPLICATION:
					result *= num1;
					break; 
				}
				stack->push(new StackItem(std::to_string(result)));
			}
		}
		i++;
	}
	return result;
}


string Calculator::getPostfix()
{
	return postfixExpression;
}


Calculator::~Calculator()
{
	delete stack;
}


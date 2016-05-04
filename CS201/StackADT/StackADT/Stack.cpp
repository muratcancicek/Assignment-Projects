/* Coded by Muratcan Çiçek S004233 Computer Science */

#include "Stack.h" 

Stack::Stack()
{

}

Stack::Stack(int size)
{
	Stack();
}


Stack::~Stack()
{ 
	while (head)
	{
		delete	pop();
	}
}


StackItem* Stack::pop()
{
	StackItem* temp = head;
	StackItem* itemToBePopped;
	if (head->next){
		while (temp->next->next)
		{
			temp = temp->next;
		}
		itemToBePopped = temp->next;
		temp->next = NULL; 
	} 
	else
	{
		itemToBePopped = head;
		head = NULL;
	}

	return itemToBePopped;
}


StackItem* Stack::top()
{
	StackItem* temp = head;
	while (temp->next)
	{
		temp = temp->next;
	}  
	return temp;
}


void Stack::push(StackItem * item)
{ 
	if (head)
		top()->next = item;
	else
		head = item;
}


bool Stack::isEmpty()
{
	return !head;
}

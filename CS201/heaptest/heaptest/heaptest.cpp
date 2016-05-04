//=============================================================================
// Name        : heaptest.cpp
// Author      : Hasan Sozer
// Version     : 1.0
// Copyright   : (c) 2013 Ozyegin University
// Description : Includes the main function that will be used to test the 
//               BinaryHeap class to be submitted as part of Homework 4, which  
//               is assigned in the context of the course CS201, Data  
//				 Structures and Algorithms. It assumes the implementation of a
//				 Binary Min-Heap ADT and runs a set of tests on the ADT.  
//				 Reports any violation of the expected behavior.
//=============================================================================

#include <iostream>
#include <cassert>
#include "BinaryHeap.h"

using namespace std;

int main ()
{
	cout << "Testing your heap implementation..." << endl << endl;

	BinaryHeap heap(10);

	// BASICS
	cout << "Testing insert for a single item..." << endl;
	heap.insert(3);
	assert(heap.getMin() == 3);
	heap.deleteMin();

	// INSERT
	cout << "Testing insert..." << endl;
	heap.insert(5);
	heap.insert(10);
	heap.insert(4);
	heap.insert(2);
	heap.insert(56);
	heap.insert(34);

	// GETMIN
	cout << "Testing getMin..." << endl;
	assert(heap.getMin() == 2);

	// DELETEMIN
	cout << "Testing deleteMin..." << endl;
	heap.deleteMin();
	heap.deleteMin();

	// GETMIN AFTER DELETEMIN
	cout << "Testing getMin after deleteMin..." << endl;
	assert(heap.getMin() == 5);

	// EXCESSIVE DELETEMIN
	cout << "Testing deleteMin on an empty heap..." << endl;
	heap.deleteMin();
	heap.deleteMin();
	heap.deleteMin();
	heap.deleteMin();
	heap.deleteMin();

	// GETMIN AFTER EXCESSIVE DELETEMIN
	cout << "Testing deleteMin on an empty heap..." << endl;
	assert(heap.getMin() == -1);

	// DUPLICATE ELEMENTS
	cout << "Testing insert with duplicate values..." << endl;
	heap.insert(5);
	heap.insert(10);
	heap.insert(4);
	heap.insert(4);
	heap.insert(2);
	heap.insert(56);
	heap.insert(10);
	heap.insert(34);

	// GETMIN WITH DUPLICATE ELEMENTS
	cout << "Testing getMin..." << endl;
	assert(heap.getMin() == 2);

	// EXCESSIVE INSERT
	cout << "Testing insert over capacity..." << endl;
	heap.insert(25);
	heap.insert(100);
	heap.insert(54);
	heap.insert(44);
	heap.insert(26);
	heap.insert(3);
	heap.insert(48);
	heap.insert(9);

	// GETMIN AFTER EXCESSIVE INSERT
	cout << "Testing getMin..." << endl;
	assert(heap.getMin() == 2);

	cout << endl << "Congrats! Your Heap implementation passed all the tests!" << endl;
	cout << "Now you can use your implementation to complete Homework 4;" << endl;
	cout << "copy the files BinaryHeap.h and BinaryHeap.cpp to extend Homework 1..." << endl;

	return 0;
}

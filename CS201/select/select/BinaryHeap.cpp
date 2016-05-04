//============================================================================
// Name        : BinaryHeap.cpp
// Author      : Hasan Sozer
// Version     : 1.2
// Copyright   : (c) 2013 Ozyegin University
// Description : Includes the (incomplete) implementation file of the  
//               BinaryHeap class that will be used as part of the program    
//               to be submitted as Homework 4, which is assigned in the   
//				 context of the course CS201, Data Structures and Algorithms.
//               
//				 THE IMPLEMENTATION MUST BE COMPLETED TO MAKE ALL THE TESTS
//				 IN THE MAIN METHOD PASS.
//
//				 After completing the heap implementation, "BinaryHeap.h" and
//				 "BinaryHeap.cpp" files will be used for extending homework 1,
//				 and the extended program will be submitted as Homework 4.
//============================================================================

#include "BinaryHeap.h"

BinaryHeap::BinaryHeap(int capacity) {
    this->capacity = capacity;
	heap = new int[capacity+1];
	size = 0; 
}

BinaryHeap::~BinaryHeap() {
	delete [] heap;
}

void BinaryHeap::insert(int element) {
	/*
	// TO BE COMPLETED
	
	// The capacity of the heap is assumed to be fixed.
	// Insert the element if size < capacity
	// Do nothing otherwise.
	
	// After the new element is inserted, perform a percolate up operation here.
	// You can add a percolateUp method to the class,
	// or just implement the operations within this insert method.*/

	if (size < capacity)
	{
		int hole = ++size;
		for ( ; hole > 1 && element < heap[hole/2]; hole/=2)
		{
			heap[hole] = heap[hole / 2];
		}

		heap[hole] = element; 
	}

}

void BinaryHeap::deleteMin() { 
	// TO BE COMPLETED
	if (size > 0)
	{
		heap[1] = heap[size];
		size--;
		percolateDown(1);
	}
	
}

int BinaryHeap::getMin() {
	// TO BE COMPLETED 
	
	if (size > 0) 
		return heap[1]; 
	else
		return -1;
}

void BinaryHeap::percolateDown(int hole) {
	// TO BE COMPLETED 

	if (2 * hole <= size)
	{
		if (heap[hole] > heap[2 * hole])
		{
			if (heap[hole] > heap[2 * hole + 1])
			{
				if (heap[2 * hole] > heap[2 * hole + 1])
				{
					swap(hole, 2 * hole + 1);
					percolateDown(heap[2 * hole + 1]);
				}
				else
				{
					swap(hole, 2 * hole);
					percolateDown(heap[2 * hole]);
				}
			}
			else
			{
				swap(hole, 2 * hole);
				percolateDown(heap[2 * hole]);
			}
		}
		else if (heap[hole] > heap[2 * hole + 1])
		{ 
			swap(hole, 2 * hole + 1);
			percolateDown(heap[2 * hole + 1]);
		}
	}
	
}

void BinaryHeap::swap(int i, int j) {
	int t = heap[i];
	heap[i] = heap[j];
	heap[j] = t;
}

/* Coded by Muratcan Çiçek S004233 Computer Science */
#include "AlgorithmSortAll.h" 
#include <iostream>

AlgorithmSortAll::AlgorithmSortAll(int k)
{
	this->k = k;
}

int AlgorithmSortAll::select()
{
	int theNumber = 0;	
	int n = 0; 
	std::cin >> n;
	int* array = new int[n];

	for (int i = 0; i < n; i++)
	{
		int temp = 0;
		std::cin >> temp;
		array[i] = temp;
	}
	quickSort(array, 0, n-1);


	theNumber = array[k - 1];
	delete array;
	return theNumber;
}

AlgorithmSortAll::~AlgorithmSortAll()
{
}


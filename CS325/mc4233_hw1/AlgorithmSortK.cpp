/* Coded by Muratcan Çiçek S004233 Computer Science */
#include "AlgorithmSortK.h"
#include <iostream>


AlgorithmSortK::AlgorithmSortK(int k)
{
	this->k = k;
}


int AlgorithmSortK::select()
{
	int theNumber = 0;
	int n = 0; 
	std::cin >> n;
	int* array = new int[k];

	for (int i = 0; i < k; i++)
	{
		std::cin >> array[i];
	}
	quickSort(array, 0, k-1);
	for (int i = k; i < n; i++)
	{
		int input = 0;
		std::cin >> input;
		if (array[k - 1] < input){
			array[k - 1] = input;
			int j = k-1;
			while (j > 0 && array[j] > array[j-1])
				{
					int temp = array[j];
					array[j] = array[j-1];
					array[j-1] = temp;
					j--;
				} 
		}
	}
	theNumber = array[k - 1];
	delete array;
	return theNumber;
}

AlgorithmSortK::~AlgorithmSortK()
{
}

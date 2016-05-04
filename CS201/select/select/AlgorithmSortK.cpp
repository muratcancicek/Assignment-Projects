/* Coded by Muratcan Çiçek S004233 Computer Science */
#include "AlgorithmSortK.h"
#include <iostream>


AlgorithmSortK::AlgorithmSortK(int k, std::string myfile)
{
	this->k = k;
	this->myfile = myfile;
}

void AlgorithmSortK::BubbleSort(int num[], int numLength)
{
	int i, j, flag = 1;    // set flag to 1 to start first pass
	int temp;             // holding variable 
	for (i = 1; (i <= numLength) && flag; i++)
	{
		flag = 0;
		for (j = 0; j < (numLength - 1); j++)
		{
			if (num[j + 1] > num[j])      // ascending order simply changes to <
			{
				temp = num[j];             // swap elements
				num[j] = num[j + 1];
				num[j + 1] = temp;
				flag = 1;               // indicates that a swap occurred.
			}
		}
	}
	return;   //arrays are passed to functions by address; nothing is returned
}

int AlgorithmSortK::select()
{
	int theNumber = 0;
	int n = 0; 	
	//std::cin >> n;	
	std::ifstream file(myfile);
	if (file.is_open())
	{
		file >> n;
		file >> this->k;
		file >> n;

		int* array = new int[k];

		for (int i = 0; i < k; i++)
		{
			//std::cin >> array[i];
			file >> array[i];
		}
		//BubbleSort(array, k - 1);
		quickSort(array, 0, k - 1);
		for (int i = k; i < n; i++)
		{
			int input = 0;
			//std::cin >> temp;
			file >> input;
			if (array[k - 1] < input){
				array[k - 1] = input;
				int j = k - 1;
				while (j > 0 && array[j] > array[j - 1])
				{
					int temp = array[j];
					array[j] = array[j - 1];
					array[j - 1] = temp;
					j--;
				}
			}
		}
		theNumber = array[k - 1];
		delete array;
	}
	else
		std::cout << "Unable to open file";
	return theNumber;
} 


void AlgorithmSortK::quickSort(int array[], int begin, int last)
{
	int p;

	if (begin < last)
	{
		p = pivot(array, begin, last);
		quickSort(array, begin, p - 1);
		quickSort(array, p + 1, last);
	}
}

int AlgorithmSortK::pivot(int array[], int begin, int last)
{
	int  p = begin;
	int pivotElement = array[begin];

	for (int i = begin + 1; i <= last; i++)
	{
		if (array[i] > pivotElement)
		{
			p++;
			int temp = array[i];
			array[i] = array[p];
			array[p] = temp;
		}
	}

	int temp = array[begin];
	array[begin] = array[p];
	array[p] = temp;
	return p;
}


AlgorithmSortK::~AlgorithmSortK()
{
}

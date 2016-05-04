/* Coded by Muratcan Çiçek S004233 Computer Science */
#include "AlgorithmSortAll.h" 
#include <iostream>

AlgorithmSortAll::AlgorithmSortAll(int k, std::string myfile)
{
	this->k = k;
	this->myfile = myfile;
}

void AlgorithmSortAll::BubbleSort(int num[], int numLength)
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

int AlgorithmSortAll::select()
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

		int* array = new int[n];

		for (int i = 0; i < n; i++)
		{
			int temp = 0;
			//std::cin >> temp;
			file >> temp;
			array[i] = temp;
		}
		quickSort(array, 0, n - 1);


		theNumber = array[k - 1];
		delete array;
	}
	else
		std::cout << "Unable to open file";
	return theNumber;
}

void AlgorithmSortAll::quickSort(int array[], int begin, int last)
{
	int p;

	if (begin < last)
	{
		p = pivot(array, begin, last);
		quickSort(array, begin, p - 1);
		quickSort(array, p + 1, last);
	}
}

int AlgorithmSortAll::pivot(int array[], int begin, int last)
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

AlgorithmSortAll::~AlgorithmSortAll()
{
}


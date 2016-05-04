#include "AlgorithmSortQuick.h"
#include <iostream>
#include<fstream>
#include <string>

AlgorithmSortQuick::AlgorithmSortQuick(int k, std::string myfile)
{
	this->k = k;
	this->myfile = myfile;
}

AlgorithmSortQuick::~AlgorithmSortQuick()
{ 

}

void swap(int* i, int* j)
{
	int t = *i;
	*i = *j;
	*j = t;
}

int madian3(int* numbers, int left, int right)
{
	int center = (left + right) / 2;

	if (numbers[center] > numbers[left])
		swap(&numbers[left], &numbers[center]);
	if (numbers[right] > numbers[left])
		swap(&numbers[left], &numbers[right]);
	if (numbers[right] > numbers[center])
		swap(&numbers[right], &numbers[center]);

	swap(&numbers[center], &numbers[right - 1]);
	return numbers[right - 1];
} 

int AlgorithmSortQuick::quickselect(int* numbers, int left, int right, int k)
{
	//for (int i = left; i <= right; i++)
	//{
	//	std::cout << numbers[i] << " - ";
	//}
	//std::cout << "\n ";
	if (left + 10 <= right)
	{
		int pivot = madian3(numbers, left, right);

		int i = left, j = right - 1;

		for ( ; ; )
		{	

			while (numbers[++i] > pivot) { }
			while (pivot > numbers[--j]) { }
			if (i < j) 
				swap(&numbers[i], &numbers[j]);
			else
				break; 
		}
		//std::cout << "\n " << numbers[i] << " - " << numbers[right - 1];
		swap(&numbers[i], &numbers[right - 1]);
		//std::cout << "\n " << numbers[i] << " - " << numbers[right - 1];
	
		if (k < i)
		{
			quickselect(numbers, left, i-1, k); 
		}
		else if (k == i)
		{
			return numbers[i];
		}
		else 
		{
			quickselect(numbers, i + 1, right, k);  
		}
	}
	else
	{
		int j;
		for (int p = 1; p < right+1; p++)
		{				
				int temp = numbers[p];
				for (j = p; j > 0 && temp >= numbers[j - 1]; j--)				
					numbers[j] = numbers[j - 1];
				numbers[j] = temp;				
		}

		return numbers[k - 1];
	} 
}

int AlgorithmSortQuick::select()
{
	int theNumber = 0;

	int n = 0;
	int input = 0; 
	//std::cin >> n;  
	std::ifstream file(myfile); 
	if (file.is_open())
	{ 
		file >> n;
		file >> this->k; 
		file >> n;

		int* numbers = new int[n];

		for (int i = 0; i < n; i++)
		{
			//std::cin >> input;  
			file >> input;
			numbers[i] = input;
		}

		file.close();
		theNumber = quickselect(numbers, 0, n-1, k);  
	}
	else 
		std::cout << "Unable to open file";

	return theNumber;
}


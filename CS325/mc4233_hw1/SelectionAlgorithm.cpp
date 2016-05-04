/* Coded by Muratcan Çiçek S004233 Computer Science */
#include "SelectionAlgorithm.h"

SelectionAlgorithm::SelectionAlgorithm()
{
	
}
SelectionAlgorithm::SelectionAlgorithm(int k)
{
	this->k = k;
}
void SelectionAlgorithm::sort(int* array, int n)
{
	for (int i = 0; i < n - 1; i++)
	{
		for (int j = i + 1; j < n; j++)
		{
			if (array[i] < array[j])
			{
				int temp = array[i];
				array[i] = array[j];
				array[j] = temp;
			}
		}
	}
}

void SelectionAlgorithm::quickSort(int array[], int begin, int last)
{
	int p;

	if (begin < last)
	{
		p= pivot(array, begin, last);
		quickSort(array, begin, p - 1);
		quickSort(array, p + 1, last);
	}
}

int SelectionAlgorithm::pivot(int array[], int begin, int last)
{
	int  p = begin;
	int pivotElement = array[begin];

	for (int i = begin + 1; i <= last; i++)
	{
		/* If you want to sort the list in the other order, change "<=" to ">" */
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

int SelectionAlgorithm::select()
{
	return 0;
}

SelectionAlgorithm::~SelectionAlgorithm()
{

}

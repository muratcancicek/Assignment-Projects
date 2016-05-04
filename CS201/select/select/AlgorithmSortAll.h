/* Coded by Muratcan Çiçek S004233 Computer Science */
#ifndef ALGORITHMSORTALL_H
#define ALGORITHMSORTALL_H
#include "SelectionAlgorithm.h"

class AlgorithmSortAll :
	public SelectionAlgorithm
{
public:
	AlgorithmSortAll(int k, std::string myfile);
	int select();

	void BubbleSort(int num[], int numLength);
	void quickSort(int array[], int begin, int last);
	int pivot(int array[], int first, int last);
	~AlgorithmSortAll();
};

#endif 

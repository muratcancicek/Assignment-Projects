/* Coded by Muratcan Çiçek S004233 Computer Science */
#ifndef  ALGORITHMSORTK_H
#define  ALGORITHMSORTK_H
#include "SelectionAlgorithm.h"

class AlgorithmSortK :
	public SelectionAlgorithm
{
public:
	AlgorithmSortK(int k, std::string myfile);
	int select();
	void BubbleSort(int num[], int numLength);
	void quickSort(int array[], int begin, int last);
	int pivot(int array[], int first, int last);
	~AlgorithmSortK();
};

#endif 

/* Coded by Muratcan Çiçek S004233 Computer Science Ozyegin University */
#ifndef  ALGORITHMSORTHEAP_H
#define  ALGORITHMSORTHEAP_H

#include "SelectionAlgorithm.h"
class AlgorithmSortHeap :
	public SelectionAlgorithm
{
public:
	AlgorithmSortHeap(int k, std::string myfile);
	int select();
	~AlgorithmSortHeap();

};

#endif 
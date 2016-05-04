/* Coded by Muratcan Çiçek S004233 Computer Science Ozyegin University */
#include "AlgorithmSortHeap.h"
#include "BinaryHeap.h"
#include <iostream>

AlgorithmSortHeap::AlgorithmSortHeap(int k, std::string myfile)
{
	this->k = k;
	this->myfile = myfile;
}

int AlgorithmSortHeap::select()
{
	int theNumber = 0;
	int n = 0;
	//std::cout << "ooo";
	//std::cin >> n;
	std::ifstream file(myfile);
	if (file.is_open())
	{
		file >> n;
		file >> this->k; 
		file >> n;
		BinaryHeap* heap = new BinaryHeap(k);

		int input = 0;
		for (int i = 0; i < k; i++)
		{
			//std::cin >> input;
			file >> input;
			heap->insert(input);
		}
		for (int i = k; i < n; i++)
		{
			//std::cin >> input;
			file >> input;
			if (input > heap->getMin()){
				heap->deleteMin();
				heap->insert(input);
			}
		}
		file.close();
		theNumber = heap->getMin();
		delete heap;
	}
	else
		std::cout << "Unable to open file";
	return theNumber;
}

AlgorithmSortHeap::~AlgorithmSortHeap()
{
}

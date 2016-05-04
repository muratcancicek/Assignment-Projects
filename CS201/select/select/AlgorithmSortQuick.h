#include "SelectionAlgorithm.h"

class AlgorithmSortQuick :
	public SelectionAlgorithm
{
public: 
	AlgorithmSortQuick(int k, std::string myfile);
	~AlgorithmSortQuick();
	int select();
	int quickselect(int* numbers, int left, int right, int k);
private:
	int k = 0;
};


/* Coded by Muratcan Çiçek S004233 Computer Science */
#ifndef SELECTIONALGORITHM_H
#define SELECTIONALGORITHM_H 

class SelectionAlgorithm
{
public:
	SelectionAlgorithm();
	SelectionAlgorithm(int k);
	virtual int select();
	 
	void sort(int* array, int n);
	void quickSort(int array[], int begin, int last);
	int pivot(int array[], int first, int last);
	~SelectionAlgorithm();
protected:
	int k;
};
#endif 

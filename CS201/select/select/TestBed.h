/* Coded by Muratcan Çiçek S004233 Computer Science */
#ifndef TESTBED_H
#define TESTBED_H
#include "SelectionAlgorithm.h"
class TestBed
{
public:
	TestBed();
	~TestBed();

	SelectionAlgorithm* algorithm;
	void execute();
	void SetAlgorithm(int type, int k, std::string myfile);
private: 
	std::ofstream myOutputFile;
	int k;
	int type;
};

#endif 

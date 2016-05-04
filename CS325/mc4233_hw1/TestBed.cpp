/* Coded by Muratcan Çiçek S004233 Computer Science */
#include "TestBed.h" 
#include "AlgorithmSortAll.h"
#include "AlgorithmSortK.h"
#include <iostream>
#include <ctime>

TestBed::TestBed()
{
	
}

void TestBed::execute()
{
// Time stamp before the computations
	clock_t start = clock();

	/* Computations to be measured */
	std::cout << "The number " << algorithm->select();

	// Time stamp after the computations
	clock_t end = clock();
	double cpu_time = static_cast<double>(end - start) / CLOCKS_PER_SEC;
	std::cout << " is found in " << cpu_time << " seconds.";
}

void TestBed::SetAlgorithm(int type, int k)
{
	if (type == 1){
		algorithm = new AlgorithmSortAll(k);
	}
	else if (type == 2){
		algorithm = new AlgorithmSortK(k);
	}
}

TestBed::~TestBed()
{
	delete algorithm;
}

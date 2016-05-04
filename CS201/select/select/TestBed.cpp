/* Coded by Muratcan Çiçek S004233 Computer Science */
#include "TestBed.h" 
#include "AlgorithmSortAll.h"
#include "AlgorithmSortK.h"
#include "AlgorithmSortHeap.h"
#include "AlgorithmSortQuick.h"
#include <iostream>
#include <fstream>
#include <ctime>

TestBed::TestBed()
{
	type = 0;
	myOutputFile.open("output.txt");
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
	std::cout << " is found in " << cpu_time << " seconds.\n";
	//			ostringstream oss;
	//			oss << "myTestInput" << "_" << algorithmType << "_" << selectionIndex << "_" << inputSize << ".txt";
	myOutputFile << type << "\t" << 2*this->k << "\t" << cpu_time << "\n";
}

void TestBed::SetAlgorithm(int type, int k, std::string myfile)
{
	this->type = type;
	this->k = k;
	if (type == 1){
		algorithm = new AlgorithmSortAll(k, myfile);
	}
	else if (type == 2){
		algorithm = new AlgorithmSortK(k, myfile);
	}
	else if (type == 3){
		algorithm = new AlgorithmSortHeap(k, myfile);
	}
	else if (type == 4){
		algorithm = new AlgorithmSortQuick(k, myfile);
	}
}

TestBed::~TestBed()
{
	delete algorithm;
	myOutputFile.close();
}

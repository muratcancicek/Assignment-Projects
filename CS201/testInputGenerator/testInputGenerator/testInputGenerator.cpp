//============================================================================
// Name        : testInputGenerator.cpp
// Author      : Hasan Sozer
// Version     : 2.0
// Copyright   : (c) 2012 Ozyegin University
// Description : Generates test input data for Homework 1 that is assigned
//               in the context of the course CS201, Data Structures
//               and Algorithms.
// Usage       : testInputGenerator T k N r
// Parameters  :
//               T (algorithm type)	: 1 or 2
//				 k (selection index): an integer between 0 and N
//               N (input size)		: an integer greater than 0
//               r (input range)	: an integer greater than 0
//============================================================================

#include <iostream>
#include <cstdlib>
using namespace std;

int algorithmType = 0;
int selectionIndex = 0;
int inputSize = 0;
int inputRange = 0;

void printUsage() {
	cout << endl << "Usage:" << endl;
	cout << "testInputGenerator T k N r" << endl;
	cout << endl << "Parameters:" << endl;
	cout << "T (algorithm type)	: 1 or 2" << endl;
	cout << "k (selection index) : an integer between 0 and N" << endl;
	cout << "N (input size)	: an integer greater than 0" << endl;
	cout << "r (input range) : an integer greater than 0" << endl;
}

int parseArguments(int count, char *argList[]) {

	if(count != 5) {
		cout << "ERROR: Wrong amount of parameters!" << endl;
		return -1;
	}
	algorithmType = atoi(argList[1]);
	selectionIndex = atoi(argList[2]);
    inputSize = atoi(argList[3]);
	inputRange = atoi(argList[4]);

	if ((algorithmType != 1 && algorithmType != 2 && algorithmType != 3) ||
	   (inputSize < 1) ||
	   (inputRange < 1) ||
	   (selectionIndex < 0) ||
	   (selectionIndex > inputSize)) {
	   cout << "ERROR: Wrong value(s) of parameters!" << endl;
	   return -1;
	}
	return 0;
}

int main(int argc, char *argv[]) {

	if(parseArguments(argc, argv) < 0) {
		printUsage();
		return -1;
	}

	cout << algorithmType << endl;
	cout << selectionIndex << endl;
	cout << inputSize << endl;
	for (int var = 0; var < inputSize; var++) {
		cout << rand()%inputRange << endl;
	}
	return 0;
}



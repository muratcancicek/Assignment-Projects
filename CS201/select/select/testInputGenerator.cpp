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
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <cstring>
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

int parseArguments(/*int count, int argList[]*/) {

	//if(count != 1) {
	//	cout << "ERROR: Wrong amount of parameters!" << endl;
	//	return -1;
	//}
	//algorithmType = atoi(argList[1]);
	//selectionIndex = atoi(argList[2]);
 //   inputSize = atoi(argList[3]);
	//inputRange = atoi(argList[4]); 
    if(!(algorithmType >= 1 && algorithmType <= 4) ||
	   (inputSize < 1) ||
	   (inputRange < 1) ||
	   (selectionIndex < 0) ||
	   (selectionIndex > inputSize)) {
	   cout << "ERROR: Wrong value(s) of parameters!" << endl;
	   return -1;
	}
	return 0;
}

//int main(int argc, char *argv[]) { 
//
//	/*string ar1 = "1";
//	int a[] = { 0, algorithmType, selectionIndex, inputSize, inputRange};*/
//	
//	for (int i = 10; i <= 1000000; i+=100000)
//	{
//		//if (i >= 100000)
//		//	break;// i += 100000;
//		//else
//		//	i *= 100;
//
//		for (int j = 1; j < 5; j++)
//		{
//			algorithmType = j;
//			inputSize = i;
//			selectionIndex = i / 2;
//			inputRange = i * 3;
//			if(parseArguments(/*argc, a*/) < 0) {
//				printUsage();
//				return -1;
//			} 
//			ofstream myfile;
//			ostringstream oss;
//			oss << "myTestInput" << "_" << algorithmType << "_" << selectionIndex << "_" << inputSize << ".txt";
//			myfile.open(oss.str());
//			myfile << algorithmType << endl;
//			myfile << selectionIndex << endl;
//			myfile << inputSize << endl;
//			for (int var = 0; var < inputSize; var++) {
//				myfile << rand()%inputRange << endl;
//			}
//			myfile.close();
//		}
//		
//	}
//	
//	return 0;
//}
//
//

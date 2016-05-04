#include <iostream>
#include <fstream>
#include <sstream>  
#include <string>
#include <ctime> 
#include <time.h> 
//#include <sys/time.h>
#include <limits.h>
#include <vector> 
#include <stdlib.h>
#include <limits>
using namespace std;

long counter = 0;		

int algOne(int arr[], int lenOfArr) { 
	int bestSum = 0;	
	int sum = 0;	
	for (int i = 1; i <= lenOfArr; i++)		
	{
		for (int j = 0; j < lenOfArr; ++j)		
		{
			if (j + i > lenOfArr)	
				break;
			int sum = 0;
			for (int k = j; k < (j + i); k++) {
				sum += arr[k];
				counter++;
	//cout << counter << endl; 
			}
			if(sum > bestSum)
				bestSum = sum;
		}
	}  
	return bestSum > 0 ? bestSum : 0;
}

int algTwo(int arr[], int lenOfArr) { 
	int bestSum = INT_MIN;
	int sum = 0;
	for (int i = 0; i < lenOfArr; ++i) 	
	{
		int sum = 0;
		for (int j = 1; j <= lenOfArr; ++j)
		{
			if (i + j > lenOfArr) 
				break;
			sum += arr[i + j - 1];
			counter++;
			if (sum > bestSum)
				bestSum = sum;
		}
	}
	return bestSum > 0 ? bestSum : 0;
}

int algThree(int arr[], int lenOfArr) { 
	int bestSum = 0;
	int sum = 0; 
	for (int i = 0; i < lenOfArr; i++)
	{
		sum = sum + arr[i];
		counter++; 
		if (sum < 0)
			sum = 0;
		if (bestSum < sum)
			bestSum = sum;
	} 
	return bestSum > 0 ? bestSum : 0;
}

typedef int (*algorithm)(int[], int);
typedef numeric_limits <double> dbl;
double runningTime;
int testAlgSpeed(algorithm alg, const char* algName, int arr[], int lenOfArr) 
{
	//Time stamp before the computations
	clock_t start = clock();   
	/* Computations to be measured */ 
	int bestSum = (*alg)(arr, lenOfArr);
	// Time stamp after the computations
	clock_t end = clock();  
	double cpu_time = (double)(end - start) / CLOCKS_PER_SEC;
	cout << algName << " is ran in " << cpu_time << " seconds ( n = " << counter << ") ";
	runningTime = cpu_time;
	return bestSum; 
}

vector<int> originalAnswers; 
vector<vector<int> > readTestArraysFromFile() {
	vector<vector<int> > testArrays;
	ifstream testFile("testing.txt"); 
	if (testFile.fail())
	{
		cout << "The file could not be opened!\n";
		exit(1); // 0 – nrormal exit, non zero – some error
	}
	string l ="";
	while (getline(testFile, l))
	{
		if (l.empty()) continue;
		stringstream line(l); 
		vector<int> arr; 
		int number;
		char otherChar;
		line >> otherChar;
		while (line >> number)
		{
			arr.push_back(number);
			line >> otherChar;
			if (otherChar == ']')
			{ 
				line >> otherChar;
			} 
		}
		originalAnswers.push_back(arr.back());
		arr.pop_back();
		testArrays.push_back(arr); 
	} 
	testFile.close();
	return testArrays;
}

vector<int> answersOfAlg1;
vector<int> answersOfAlg2;
vector<int> answersOfAlg3;
void analyseValidationFile()
{
	char msg1[] ="The Algorithm 1";
	char msg2[] = "The Algorithm 2";
	char msg3[] = "The Algorithm 3";
	vector<vector<int> > testArrays = readTestArraysFromFile();

	for (int i = 0; i < testArrays.size(); i++)
	{ 
		int answer1 = testAlgSpeed(algOne, msg1, &(testArrays[i][0]), testArrays[i].size());
		cout << " for the Array " << (i + 1) << ", the answer is " << answer1 << "\n";
		answersOfAlg1.push_back(answer1);
		counter = 0;
		int answer2 = testAlgSpeed(algTwo, msg2 , &(testArrays[i][0]), testArrays[i].size());
		cout << " for the Array " << (i + 1) << ", the answer is " << answer2 << "\n";
		answersOfAlg2.push_back(answer2);
		counter = 0;
		int answer3 = testAlgSpeed(algThree, msg3, &(testArrays[i][0]), testArrays[i].size());
		cout << " for the Array " << (i + 1) << ", the answer is " << answer3 << endl << "\n\n";
		answersOfAlg3.push_back(answer3);

		counter = 0;
	}
}

void writeAnswersLine(ofstream* output, vector<int>* answers)
{
	for (int i = 0; i < (*answers).size(); i++)
	{
		(*output) << (*answers)[i] << ' ';
	}
	(*output) << '\n';
}

void printAnswersLine(ostream* output, vector<int>* answers)
{
	for (int i = 0; i < (*answers).size(); i++)
	{
		(*output) << (*answers)[i] << ' ';
	}
	(*output) << '\n';
}

void writeOutput()
{
	ofstream output;
	output.open("Output.txt");
	if (output.fail())
	{
		cout << "The output file could not be created\n\n"; 
		printAnswersLine(&cout, &answersOfAlg1);
		printAnswersLine(&cout, &answersOfAlg2);
		printAnswersLine(&cout, &answersOfAlg3);
	}
	else
	{
		writeAnswersLine(&output, &answersOfAlg1);
		writeAnswersLine(&output, &answersOfAlg2);
		writeAnswersLine(&output, &answersOfAlg3);
	}
}

int *genArr(int sizes)
{
	int *array = new int[sizes];
	for(int i = 0; i < sizes; i++)
	{
		array[i] = ((rand() % 2000) - 1000);
	}
	return array;
}

void printArr(int arr[], int sizes)
{
	char msg1[] = "The Algorithm 1, our 100's arrays";
	char msg2[] = "The Algorithm 2, our 100's arrays";
	char msg3[] = "The Algorithm 3, our 100's arrays";
	int answer1 = testAlgSpeed(algOne, msg1, arr, sizes);
	cout << " the answer is " << answer1 << endl;

	int answer2 = testAlgSpeed(algTwo, msg2, arr, sizes);
	cout << " the answer is " << answer2 << endl;

	int answer3 = testAlgSpeed(algThree, msg3, arr, sizes);
	cout << " the answer is " << answer3 << endl << endl;
}
void printArr2(int arr[], int sizes)
{

	char msg2[] = "The Algorithm 2, our 1000's arrays";
	char msg3[] = "The Algorithm 3, our 1000's arrays";

	int answer2 = testAlgSpeed(algTwo, msg2, arr, sizes);
	cout << " the answer is " << answer2 << endl;

	int answer3 = testAlgSpeed(algThree, msg3, arr, sizes);
	cout << " the answer is " << answer3 << endl << endl;
}

void testRandomArray()
{
	int *array1;
	int *array2;
	for (int i = 100; i < 1000; i += 100) {
		array1 = new int [i];
		array1 = genArr(i);
		printArr(array1, i);
		delete array1;

	}
	for (int i = 1000; i < 10000; i += 1000) {
		array2 = new int [i];
		array2 = genArr(i);
		printArr2(array2, i);
		delete array2;

	}
}

// ALTERNATIVE TESTING //

void writeAnswersLine(ofstream* output, int n, double* answers)
{
	(*output) << n << '\t';
	for (int i = 0; i < 2; i++)
	{
		(*output) << answers[i] << '\t';
	}
	(*output) << '\n';
}
void printAnswersLine(ostream* output, int n, double* answers)
{
	(*output) << n << '\t';
	for (int i = 0; i < 2; i++)
	{
		(*output) << answers[i] << '\t';
	}
	(*output) << '\n';
}

void testAlgTime(algorithm alg,const char* algName, ofstream *output, int scale)
{
	for (int i = scale; i <= scale * 10; i += scale)
	{
		double* ns = new double[2];
		int* arr = genArr(i);
		int j = 0;
		testAlgSpeed(alg, algName, arr, i);
		ns[0] = counter;
		ns[1] = runningTime;
		cout << endl;
		counter = 0; runningTime = 0;
		if ((*output).fail())
		{
			cout << "The alternativeTestingOutput file could not be created!\n\n";
			printAnswersLine(&(cout), i, ns);
		}
		else
		{
			writeAnswersLine(&(*output), i, ns);
		}
	}
	cout << endl;
	(*output) << '\n';
}

void alternativeTesting()
{
	ofstream output;
	output.open("AlternativeTestingOutput.txt"); 
	testAlgTime(algOne, "Algorithm 1", &output, 100);
	testAlgTime(algTwo, "Algorithm 2", &output, 1000);
	testAlgTime(algThree, "Algorithm 3", &output, 1000000);

}
int main() {
	srand(time(NULL));
	testRandomArray();
	analyseValidationFile(); 
	writeOutput(); 
	alternativeTesting();
	return 0;

}


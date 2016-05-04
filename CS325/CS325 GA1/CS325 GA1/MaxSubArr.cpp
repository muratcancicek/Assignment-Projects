//#include <iostream>
//#include <fstream>
//#include <sstream>  
//#include <string>
//#include <ctime>
//#include <limits>
//#include <vector> 
//
//using namespace std;
//
//int counter = 0;		
//
//int algOne(int arr[], int lenOfArr) { 
//	int bestSum = 0;	
//		int sum = 0;	
//		for (int i = 1; i <= lenOfArr; i++)		
//		{
//			for (int j = 0; j < lenOfArr; ++j)		
//			{
//				if (j + i > lenOfArr)	
//					break;
//				int sum = 0;
//				for (int k = j; k < (j + i); k++) {
//					sum += arr[k];
//					counter++;
//				}
//				if(sum > bestSum)
//					bestSum = sum;
//			}
//		}  
//		return bestSum > 0 ? bestSum : 0;
//}
//
//int algTwo(int arr[], int lenOfArr) { 
//	int bestSum = INT_MIN;
//	int sum = 0;
//	for (int i = 0; i < lenOfArr; ++i) 	
//	{
//		int sum = 0;
//		for (int j = 1; j <= lenOfArr; ++j)
//		{
//			if (i + j > lenOfArr) 
//				break;
//			sum += arr[i + j - 1];
//			counter++;
//			if (sum > bestSum)
//				bestSum = sum;
//		}
//	}
//	return bestSum > 0 ? bestSum : 0;
//}
//
//int algThree(int arr[], int lenOfArr) { 
//	int bestSum = 0;
//	int sum = 0; 
//	for (int i = 0; i < lenOfArr; i++)
//	{
//		sum = sum + arr[i];
//		counter++; 
//		if (sum < 0)
//			sum = 0;
//		if (bestSum < sum)
//			bestSum = sum;
//	} 
//	return bestSum > 0 ? bestSum : 0;
//}
//
//typedef int (*algorithm)(int[], int); 
//int testAlgSpeed(algorithm alg,char* algName, int arr[], int lenOfArr) 
//{
//	// Time stamp before the computations
//	clock_t start = clock(); 
//	/* Computations to be measured */
//	int bestSum = (*alg)(arr, lenOfArr);
//	// Time stamp after the computations
//	clock_t end = clock();
//	double cpu_time = (static_cast<double>(end - start) / CLOCKS_PER_SEC) ;
//	// Result  
//	cout << algName << " is ran in " << cpu_time << " ms (n = " << counter << ") ";
//
//	printf("\nElapsed: %f seconds\n", (double)(end - start) / CLOCKS_PER_SEC);
//	return bestSum; 
//}
//
//vector<int> originalAnswers; 
//vector<vector<int>> readTestArraysFromFile() {
//	vector<vector<int>> testArrays;
//	ifstream testFile("../validation.txt"); 
//	if (testFile.fail())
//	{
//		cout << "The file could not be opened!\n";
//		exit(1); // 0 – nrormal exit, non zero – some error
//	}
//	string l ="";
//	while (getline(testFile, l))
//	{
//		if (l.empty()) continue;
//		stringstream line(l); 
//		vector<int> arr; 
//		int number;
//		char otherChar;
//		line >> otherChar;
//		while (line >> number)
//		{
//			arr.push_back(number);
//			line >> otherChar;
//			if (otherChar == ']')
//			{ 
//				line >> otherChar;
//			} 
//		}
//		originalAnswers.push_back(arr.back());
//		arr.pop_back();
//		testArrays.push_back(arr); 
//	} 
//	testFile.close();
//	return testArrays;
//}
//
//vector<int> answersOfAlg1;
//vector<int> answersOfAlg2;
//vector<int> answersOfAlg3;
//void analyseValidationFile()
//{
//	vector<vector<int>> testArrays = readTestArraysFromFile();
//	for (int i = 0; i < testArrays.size(); i++)
//	{ 
//		int answer1 = testAlgSpeed(algOne, "The Algorithm 1", &(testArrays[i][0]), testArrays[i].size());
//		cout << " for the Array " << (i + 1) << ", the answer is " << answer1 << endl;
//		answersOfAlg1.push_back(answer1);
//		counter = 0;
//		int answer2 = testAlgSpeed(algTwo, "The Algorithm 2", &(testArrays[i][0]), testArrays[i].size());
//		cout << " for the Array " << (i + 1) << ", the answer is " << answer2 << endl;
//		answersOfAlg2.push_back(answer2);
//		counter = 0;
//		int answer3 = testAlgSpeed(algThree, "The Algorithm 3", &(testArrays[i][0]), testArrays[i].size());
//		cout << " for the Array " << (i + 1) << ", the answer is " << answer3 << endl << endl;
//		answersOfAlg3.push_back(answer3);
//		counter = 0;
//	}
//}
//
//void writeAnswersLine(ofstream* output, vector<int>* answers)
//{
//	for (int i = 0; i < (*answers).size(); i++)
//		{
//			(*output) << (*answers)[i] << ' ';
//		}
//	(*output) << '\n';
//}
//
//void writeOutput()
//{
//	ofstream output;
//	output.open("Output.txt");
//	if (output.fail())
//	{
//		cout << "The file could not be opened!\n";
//		exit(1); // 0 – nrormal exit, non zero – some error
//	}
//	writeAnswersLine(&output, &answersOfAlg1);
//	writeAnswersLine(&output, &answersOfAlg2);
//	writeAnswersLine(&output, &answersOfAlg3);
//}
//
//int main() {  
//	analyseValidationFile(); 
//	writeOutput();
//	return 0;
//
//}
//	
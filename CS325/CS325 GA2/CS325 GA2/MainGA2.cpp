#include <string> 
#include <iostream> 
#include <fstream> 
#include <sstream>  
#include <vector>
#include <algorithm>
#include <ctime>
#include "TestCase.h" 

using namespace std;

vector<int>* readIntVectorFromLine(string l)
{  
	vector<int>* v = new vector<int>();
	int nextInt;
	stringstream line(l);
	while ((line) >> nextInt)
	{
		v->push_back(nextInt-1);
	} 
	sort(v->begin(), v->end());
	return v;
}

std::istream& safeGetline(std::istream& is, std::string& t)
{
	t.clear();

	// The characters in the stream are read one-by-one using a std::streambuf.
	// That is faster than reading them one-by-one using the std::istream.
	// Code that uses streambuf this way must be guarded by a sentry object.
	// The sentry object performs various tasks,
	// such as thread synchronization and updating the stream state.

	std::istream::sentry se(is, true);
	std::streambuf* sb = is.rdbuf();

	for (;;) {
		int c = sb->sbumpc();
		switch (c) {
		case '\n':
			return is;
		case '\r':
			if (sb->sgetc() == '\n')
				sb->sbumpc();
			return is;
		case EOF:
			// Also handle the case when the last line has no line ending
			if (t.empty())
				is.setstate(std::ios::eofbit);
			return is;
		default:
			t += (char)c;
		}
	}
}

string l = "";
TestCase* readACase(ifstream* testFile)
{
	string label = "";
	int lockersNumber = -9;
	int keysNumber = -9;
	int ballsNumber = -9;
	vector<int>* givenKeys = NULL;
	vector<int>* givenBalls = NULL;
	int expectedOutput = -1; // check later if exists
	//safeGetline((*testFile), l); 
	while (l.empty())  
		safeGetline((*testFile), l); 
	label = l; 
	safeGetline((*testFile), l);  stringstream line(l);	 // N M T 
	line >> lockersNumber >> keysNumber >> ballsNumber;
	safeGetline((*testFile), l);
	givenKeys = readIntVectorFromLine(l);	// M key tags
	safeGetline((*testFile), l);
	givenBalls = readIntVectorFromLine(l);	// T ball tags  
	TestCase* testCase = new TestCase(label, lockersNumber, givenKeys, givenBalls);
	safeGetline((*testFile), l); // OUTPUT TITLE OR BLANK 
	if (!l.empty())
	{
		safeGetline((*testFile), l); stringstream line(l); // EXPECTED OUTPUT 
		line >> expectedOutput;
		testCase->setExpectedOutput(expectedOutput);
	}
	//cout << endl;
	return testCase;
}
 
vector<TestCase*> readTestCasesFrom(const char* fileName)
{ 
	ifstream testFile(fileName);
	if (testFile.fail())
	{
		cout << "The file could not be opened!\n";
		exit(1); // 0 – nrormal exit, non zero – some error
	}  
	vector<TestCase*> testCases; 
	int counter = 1;  
	while (!(safeGetline((testFile), l)).eof())
	{  
			testCases.push_back(readACase(&testFile)); 
	} 
	testFile.close();
	return testCases;
}
 

void testAlgorithmsFor(const char* file)
{
	vector<TestCase*> allCases = readTestCasesFrom(file);;
	cout << "################################# FILE: " << file << " ############################" << endl << endl;
	for (int algorithm = 1; algorithm < 3; algorithm++) {

	cout << "################################# ALGORITHM " << algorithm << " ##################################" << endl;
	for (int i = 0; i < allCases.size(); i++)
	{
		if(algorithm == 1)
			allCases[i]->getOutputOfAlgorithm1();
		else if (algorithm == 2)
			allCases[i]->getOutputOfAlgorithm2();
		else if (algorithm == 3)
			allCases[i]->getOutputOfAlgorithm3();
	} 
	cout << endl << "################################################################################" << endl << endl;
	}
}
int main()
{
	testAlgorithmsFor("dp.txt");
	testAlgorithmsFor("dp_set1.txt");
	testAlgorithmsFor("dp_set2.txt"); 
	return 0;
}
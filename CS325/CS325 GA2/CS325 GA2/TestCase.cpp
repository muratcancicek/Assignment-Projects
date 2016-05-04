#include <iostream>
#include <algorithm>
#include <vector>
#include "TestCase.h"
#include "Locker.h"
#include <string>

using namespace std;

TestCase::TestCase(string labl, const int lockersNum, vector<int>* givenKeys, vector<int>* givenBalls)
{  
	label = labl;
	lockersNumber = lockersNum; 
	balls = givenBalls;
	keys = givenKeys;
	expectedOutput = -1;
	openedLockersNumber = 0; 
	for (int i = 0; i < lockersNumber; i++)
	{
		lockers.push_back(new Locker(i));
	}
	for (int k = 0; k < keys->size(); k++) 
	{
		lockers[(*keys)[k]]->setHasKey(true);
	}
	for (int b = 0; b < balls->size(); b++) 
	{
		lockers[(*balls)[b]]->setHasBall(true);
	}
}
 
TestCase::~TestCase()
{
	delete keys;
	delete balls; 
}


void TestCase::setExpectedOutput(int expectedOutput)
{
	this->expectedOutput = expectedOutput;
}

bool contains(vector<int>* v, int element)
{
	return find(v->begin(), v->end(), element) != v->end();
}

void removeByValue(vector<int>* vec, int value)
{
	vec->erase(remove(vec->begin(), vec->end(), value), vec->end());
}
int lockerDistance(int a, int b)
{
	return (a - b) >= 0 ? (a - b) : (b - a);
}


void TestCase::ballFoundAt(int locker)
{
	foundBallsNumber++;
	removeByValue(balls, locker); 
}


void TestCase::addNewKeyOf(int key)
{
	if (contains(keys, key)) return;
	lockers[key]->setHasKey(true);
	keys->push_back(key); 
	sort(keys->begin(), keys->end());
}

void TestCase::open(int locker)
{
	if (lockers[locker]->isOpen())
		return;
	else
		lockers[locker]->setOpen(true);
	if (lockers[locker]->hasABall())
		ballFoundAt(locker);
	if (algorithm == 1) 
	{
		addNewKeyOf(locker);
	}
	openedLockersNumber++; 
}

void TestCase::openNKeepAdjacentKeysOf(int locker)
{
	if (lockers[locker]->isOpen())
		return;
	else
	{
		open(locker); 
		addAdjacentKeysOf(locker); 
	}
		
}

void TestCase::addAdjacentKeysOf(int locker, bool left, bool right)
{
	if (locker - 1 >= 0 && left)
	{
		addNewKeyOf(locker - 1);
	}
	if (locker + 1 < lockers.size() && right)
	{
		addNewKeyOf(locker + 1);
	}
}

void TestCase::openLockersFromTo(int start, int destination)
{
	if (start < destination)
	{
		for (int locker = start; locker <= destination; locker++) // GO RIGHT
		{
			open(locker);
		}
	} 
	else
	{
		for (int locker = start; locker >= destination; locker--) // GO LEFT
		{
			open(locker);
		}
	} 
	if (algorithm == 1)
	{
		addAdjacentKeysOf(destination);
		addNewKeyOf(destination);
	}
}

void TestCase::openLockersHaveKeyAndBall()
{
	for (int i = 0; i < lockers.size(); i++)
	{
		if (lockers[i]->hasABall() && lockers[i]->hasAKey())
		{
			open(i);
			addAdjacentKeysOf(i);
		}
	}
}

// ALGORITHM X 

void TestCase::findBestBall()
{
	// [B, K, distance] but start with left side 
	int minDistance = lockerDistance(balls->front(), keys->front());
	int b[2] = { keys->front(), balls->front() };
	int* bestPair = b;
	if (minDistance == 0)
	{
		openNKeepAdjacentKeysOf(bestPair[1]);
		return;
	}
	for (int b = 0; b < balls->size(); b++)
	{
		for (int k = 0; k < keys->size(); k++)
		{
			int tempDistance = lockerDistance((*balls)[b], (*keys)[k]); 
			if (tempDistance == 0)
			{
				openNKeepAdjacentKeysOf((*keys)[k]);
				return;
			}
			else if (tempDistance < minDistance)
			{
				minDistance = tempDistance;
				int tempPair[2] = { (*keys)[k], (*balls)[b] };
				bestPair = tempPair;
			}
		}
	}
	openLockersFromTo(bestPair[0], bestPair[1]);	
}


int TestCase::getOutputOfAlgorithm1()
{ 
	algorithm = 1;
	openLockersHaveKeyAndBall();
	while (!balls->empty())
	{ 
		findBestBall();
	}
	checkCorrection(1);
	return openedLockersNumber;
}

// ALGORITHM Y


void TestCase::findRightMostBall()
{
	int rightMostBall = balls->back(); 
	int rightMostKey = keys->back();
	if (rightMostBall > rightMostKey )
	{
		openLockersFromTo(rightMostKey, rightMostBall);
		keys->pop_back();
		addAdjacentKeysOf(rightMostKey, true, false); // just keep left adjacent key
	}
	else if (keys->size() == 1)
	{
		openLockersFromTo(rightMostKey, rightMostBall);
		keys->pop_back();
		addAdjacentKeysOf(rightMostBall, true, false); // just keep left adjacent key
	}
	else
	{
		int secondRightMostKey = (*keys)[keys->size() - 2];
		while (rightMostBall < secondRightMostKey)
		{
			keys->pop_back(); // delete current RightMostKey 
			rightMostKey = secondRightMostKey;
			if (keys->size() == 1)
			{
				openLockersFromTo(rightMostKey, rightMostBall);
				keys->pop_back();
				addAdjacentKeysOf(rightMostBall, true, false); // just keep left adjacent key
				return;
			}
			secondRightMostKey = (*keys)[keys->size() - 2];
		}
		int rightDistance = lockerDistance(rightMostKey, rightMostBall);
		int leftDistance = lockerDistance(secondRightMostKey, rightMostBall);
		if (leftDistance <= rightDistance)
		{
			keys->pop_back(); // delete current RightMostKey
			keys->pop_back();
			addAdjacentKeysOf(secondRightMostKey);
			addAdjacentKeysOf(rightMostBall, true, false); // just keep left adjacent key
			openLockersFromTo(secondRightMostKey, rightMostBall);  
		}
		else
		{
			keys->pop_back(); // delete current RightMostKey
			//keys->pop_back();
			addAdjacentKeysOf(rightMostBall, true, false); // just keep left adjacent key
			openLockersFromTo(rightMostKey, rightMostBall);
			//keys->pop_back();
		}

	}
}

int TestCase::getOutputOfAlgorithm2()
{  
	algorithm = 2;
	openLockersHaveKeyAndBall();
	while (!balls->empty())
	{
		findRightMostBall();
	}
	checkCorrection(2);
	return openedLockersNumber;
}

int TestCase::getOutputOfAlgorithm3()
{ 
	// fill here
	checkCorrection(3);
	return openedLockersNumber;
}

void TestCase::checkCorrection(int i)
{
	if (expectedOutput == openedLockersNumber)
		cout << "The algorithm " << i << " for " << label << " worked correctly, output = " << openedLockersNumber << endl;
	else if (expectedOutput != -1)
		cout << "The algorithm " << i << " for " << label << " DON'T WORK!, it returns " 
		<< openedLockersNumber << " instead of " << expectedOutput << endl;
	else
		cout << "The algorithm " << i << " for " << label << " found the output = " << openedLockersNumber << endl;
}

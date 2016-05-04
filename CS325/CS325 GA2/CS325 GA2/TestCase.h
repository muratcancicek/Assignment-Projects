#pragma once
#ifndef  TESTCASE_H
#define  TESTCASE_H
#include <algorithm>
#include <vector>
#include <string>
class Locker;

class TestCase
{
public: 
	TestCase(std::string labl, const int lockersNum, std::vector<int>* keys, std::vector<int>* balls);
	~TestCase(); 
	void setExpectedOutput(int output);
	int getOutputOfAlgorithm1();
	int getOutputOfAlgorithm2();
	int getOutputOfAlgorithm3();
	void ballFoundAt(int locker);
	void addNewKeyOf(int locker);
	int openedLockersNumber;
private:
	std::string label;
	void open(int key);
	void openNKeepAdjacentKeysOf(int key);
	void addAdjacentKeysOf(int locker, bool left = true, bool right = true);
	void openLockersFromTo(int from, int to);
	void openLockersHaveKeyAndBall(); 
	void findBestBall();
	void findRightMostBall(); 
	void checkCorrection(int i); 
	int lockersNumber; 
	int keysNumber; 
	int ballsNumber; 
	int algorithm;
	std::vector<Locker*> lockers;
	std::vector<int>* keys;
	std::vector<int>* balls;
	int foundBallsNumber;  
	int expectedOutput; // may not be exist
};

#endif


/* Coded by Muratcan Çiçek S004233 Computer Science */
#include "TestBed.h"
#include <iostream>

using namespace std;
// select.exe < test1_500_1000.txt
// select.exe < test1_50000_100000.txt
// select.exe < test2_5000_10000.txt
// select.exe < test2_50000_100000.txt
// select.exe < test2_250000_500000.txt
int main(){ 
	int type = 0; 
	cin >> type;
	while (type < 1 || type > 2){ 
		cin >> type;
	}

	int k = 0; 
	cin >> k;  
	
	TestBed* test = new TestBed(); 
	test->SetAlgorithm(type, k);
	test->execute(); 
}
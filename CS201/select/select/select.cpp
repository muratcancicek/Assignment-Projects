/* Coded by Muratcan Çiçek S004233 Computer Science */
#include "TestBed.h"
#include <iostream> 
#include <sstream>
#include<fstream>

using namespace std;
/*
select.exe < test1_500_1000.txt
select.exe < test1_50000_100000.txt
select.exe < test2_5000_10000.txt
select.exe < test2_50000_100000.txt
select.exe < test2_250000_500000.txt
select.exe < test3_500_1000.txt
select.exe < test3_5000_10000.txt
select.exe < test3_50000_100000.txt
select.exe < test3_250000_500000.txt
select.exe < test4_500_1000.txt 
select.exe < test4_5000_10000.txt
select.exe < test4_50000_100000.txt
select.exe < test4_250000_500000.txt

select.exe < t.txt
*/ 

int main(){ 
	TestBed* test = new TestBed(); 
	int type = 1; 
	int k = 0; 
	//int i = 100000;
	//cin >> type;
	//while (type < 1 || type > 4){ 
	//	cin >> type;
	//}
	//cin >> k;   
	ifstream myfile;
	myfile.open("");

	myfile >> type;
	myfile >> k;
	//type = 4;
	//i = 100000;
	//k = i / 2;
	for (int j = 1; j < 2; j++)
	{ 
		for (int i = 1; i < 1000000; )
		{
			if (i < 100000)
				i *= 10;
			else if (i < 1000000)
				i += 100000;
		//int i = 1;
			type = j;
			k = i / 2; 
			ostringstream oss;
			oss << "myTestInput" << "_" << type << "_" << k << "_" << i << ".txt";
			//oss << "test" << type << "_50000_100000.txt";// << k << "_" << i << ".txt";
// "t.txt";
			test->SetAlgorithm(type, k, oss.str());
			test->execute();
		}
	}
	myfile.close();
	delete test;

return 0;
}
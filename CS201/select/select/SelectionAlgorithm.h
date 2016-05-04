/* Coded by Muratcan Çiçek S004233 Computer Science */
#include <iostream>
#include<fstream>
#ifndef SELECTIONALGORITHM_H
#define SELECTIONALGORITHM_H 


class SelectionAlgorithm
{
public:
	SelectionAlgorithm();
	SelectionAlgorithm(int k, std::string myfile);
	virtual int select();
	~SelectionAlgorithm();
	int k;
protected:
	std::string myfile; 

};
#endif 

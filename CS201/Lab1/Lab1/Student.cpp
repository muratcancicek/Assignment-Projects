#include "stdafx.h" 
#include "Student.h"
#include <iostream>

Student::Student()
{
	exams = new int[examsSize];
	for (int i = 0; i < examsSize; i++)
	{
		exams[i] = 0;
	}	
}
Student::Student(int num, std::string name)
{
	id = num;
	this->name = name;
	exams = new int[examsSize];
	for (int i = 0; i < examsSize; i++)
	{
		exams[i] = 0; 
	}
}

void Student::setExamGrade(int ind, int grade)
{
	if (ind >= 0 && ind <= 2)
	{
		exams[ind] = grade; 
	} 
}

int Student::getOverallGrade()
{
	int result = 0;
	for (int i = 0; i < examsSize; i++)
	{
		result += exams[i];
	}
	return result / examsSize;
}

void Student::display()
{
	std::cout << "ID: " << id <<  " NAME: " << name << " GRADE : " << getOverallGrade() << "\n";
}

Student::~Student()
{
	delete exams;
}

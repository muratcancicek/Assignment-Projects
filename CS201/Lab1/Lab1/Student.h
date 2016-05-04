#pragma once

#include <string>

class Student
{
public:
	Student();
	Student(int num, std::string text);
	~Student();
	int id;
	static const int examsSize = 3;
	int* exams;
	std::string name;

	void setExamGrade(int ind, int grade);
	int getOverallGrade();
	void display();

	 
};


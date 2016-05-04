
#include "stdafx.h" 
#include "Student.h"
#include <iostream>

using namespace std;

void readStudents(); 

int _tmain(int argc, _TCHAR* argv[])
{
	readStudents();

	system("PAUSE");
	return 0;
}

void readStudents()
{
	int numberOfStudent = 0;
	cout << "Enter the number of students:";
	cin >> numberOfStudent;
	Student* students = new Student[numberOfStudent];

	for (int i = 0; i < numberOfStudent; i++)
	{
		int id = 0;
		string name = "";
		cout << "Enter the id of student #" << i << ":";
		cin >> id;
		cout << "Enter the name of student" << i << ":";
		cin >> name;

		students[i] = *(new Student(id, name));
		for (int j = 0; j < Student::examsSize; j++)
		{
			int grade = 0;
			cout << "Enter the grade of student #0 for the " << j << ". exam:";
			cin >> grade;
			students[i].setExamGrade(j, grade);
		}
	}

	for (int i = 0; i < numberOfStudent; i++)
	{
		students[i].display(); 
		//delete students[i];
	}

	delete students;
}
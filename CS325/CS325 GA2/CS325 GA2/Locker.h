#pragma once
#ifndef  LOCKER_H
#define  LOCKER_H
class TestCase;
class Locker
{
public:
	Locker(int number);
	~Locker();
	bool isOpen();
	bool hasAKey();
	bool hasABall();
	void setOpen(bool ope);
	void setHasKey(bool has);
	void setHasBall(bool has);
private:
	int thisLocker; 
	bool hasKey;
	bool hasBall;
	bool open;
	
};
#endif


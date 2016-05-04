
#include "Locker.h"
#include "TestCase.h"

Locker::Locker(int number)
{
	thisLocker = number;
	open = false;
	hasBall = false;
	hasKey = false;
}

Locker::~Locker()
{
}

bool Locker::isOpen()
{
	return open;
}

bool Locker::hasAKey()
{
	return hasKey;
}

bool Locker::hasABall()
{
	return hasBall;
}

void Locker::setOpen(bool ope)
{
	this->open = ope;
}

void Locker::setHasKey(bool has)
{ 
	this->hasKey = has;
}

void Locker::setHasBall(bool has)
{
	this->hasBall = has;
}



// Description : Includes the header file of the BinarySearchTree class 
//				 that will be used as part of the program to be submitted 
//				 as Homework 3, which is assigned in the context of  
//				 the course CS201, Data Structures and Algorithms.

#ifndef __BINARYSEARCHTREE__
#define __BINARYSEARCHTREE__

#include "BinaryTreeNode.h"

using namespace std;

class BinarySearchTree {

public:
	BinarySearchTree();
	~BinarySearchTree();
	void insert(int);
	void printPreorder();
	void printInorder();
	void printPostOrder();

private:
	BinaryTreeNode *root;
	void insert(int, BinaryTreeNode * & n);
	void traversePreorder(BinaryTreeNode * n);
	void traverseInorder(BinaryTreeNode * n);
	void traversePostorder(BinaryTreeNode * n);
	void deleteNodes(BinaryTreeNode * & n);
};

#endif /* __BINARYSEARCHTREE__ */
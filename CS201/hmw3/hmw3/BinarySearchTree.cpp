/* Coded by Muratcan Çiçek S004233 Computer Science */
#include "BinarySearchTree.h"
#include <iostream>

BinarySearchTree::BinarySearchTree()
{
	root = NULL;
}

void BinarySearchTree::insert(int value){ 
		insert(value, root);  
}

void BinarySearchTree::printPreorder(){
	traversePreorder(root);
}

void BinarySearchTree::printInorder(){
	traverseInorder(root);
}

void BinarySearchTree::printPostOrder(){
	traversePostorder(root);
}

void BinarySearchTree::insert(int number, BinaryTreeNode * & n){ 
	if (!n){
		n = new BinaryTreeNode(number);
	}
	else if (number < n->element)
		insert(number, n->left); 
	else if (number >  n->element) 
		insert(number, n->right);  
}

void BinarySearchTree::traversePreorder(BinaryTreeNode * n){
	if (!n){ 
		return;
	}
	cout <<  n->element << "  ";
	traversePreorder(n->left);
	traversePreorder(n->right);
}

void BinarySearchTree::traverseInorder(BinaryTreeNode * n){
	if (!n){
		return;
	}
	traverseInorder(n->left);
	cout<< n->element << "  ";
	traverseInorder(n->right);
}

void BinarySearchTree::traversePostorder(BinaryTreeNode * n){
	if (!n){ 
		return;
	}
	traversePostorder(n->left);
	traversePostorder(n->right);
	cout << n->element << "  ";
}

void BinarySearchTree::deleteNodes(BinaryTreeNode * & n){
		if (!n)
		{
			deleteNodes(n->left);
			deleteNodes(n->right);
			delete n;
		}
}

BinarySearchTree::~BinarySearchTree()
{
	deleteNodes(root);
}
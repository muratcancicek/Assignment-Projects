/* Coded by Muratcan Çiçek S004233 Computer Science */
#include <iostream>
#include "BinarySearchTree.h"
#include "BinaryTreeNode.h"7

int main(){

	BinarySearchTree* BiSTree = new BinarySearchTree();

	cout << "Enter your numbers for BST (-1 to stop): " << endl;
	int n;
	while (1){
		cin >> n;

		if (n != -1)
			BiSTree->insert(n);
		else
			break;
	}	
	
	cout << "Preorder: ";
	BiSTree->printPreorder();

	cout << "\nInorder: ";
	BiSTree->printInorder();


	cout << "\nPostorder: ";
	BiSTree->printPostOrder(); 

}
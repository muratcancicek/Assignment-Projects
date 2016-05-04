#include <iostream>
#include <fstream>   // file I/O
#include <vector>
#include <string>
#include <unordered_map>
#include <bitset>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <exception> 
#include <functional>
#include <limits>
#include <memory>
#include <ostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
#include "LinearProbing.h"

using namespace std;

bool isArgsNumberValid(int argc, char* argv[]) {
	if (argc != 3)
	{
		cout << " Invalid argument number, program is closing..." << endl;
		return false;
	}
	//cout << "argc = " << argc << endl;
	//for (int i = 0; i < argc; i++)
	//	cout << "argv[" << i << "] = " << argv[i] << endl;
}

vector<string>* readTextFile(string fileName) {
	// SERCEN: Kaç karakter geleceini bilmediimiz için vector kulland1k, vector = Java'daki ArrayList 
	vector<string>* chars = new vector<string>();
	ifstream textFile;
	textFile.open(fileName);
	if (!textFile.good()) // SERCEN: Dosya bulunamad1ysa
	{
		cout << fileName << " cannot be found, program is closing..." << endl;
		return NULL;
	}
	while (textFile)
	{
		char c;
		textFile >> c;
		string s = string(1, c); // SERCEN: ""+ bir sey deyince o seyin turunu string'e ceviriyor
		chars->push_back(s); // SERCEN: .push_back(c) = Java'daki arraylist.add(c); 
	}
	if (chars->empty()) // SERCEN: Dosya bossa
	{
		cout << fileName << " is empty or not acceptable, program is closing..." << endl;
		return NULL;
	}
	textFile.close();
	return chars;
}

vector<string>* getCharacters(int argc, char* argv[]) {
	if (isArgsNumberValid(argc, argv))
	{
		return readTextFile(argv[1]);
	}
	else
	{
		return NULL;
	}
}

vector<int>* getEncodedOutput(vector<string>* characters)
{
	string ITEM_NOT_FOUND = "-9999";  // SERCEN: Verilen kodtan copy-paste 
	HashTable<string> hashTable(ITEM_NOT_FOUND, 4096);
	unordered_map<std::string, int> codeMap;
	int code = 0;
	for (; code < 256; code++)
	{
		string character = string(1, code);
		hashTable.insert(character);
		codeMap[character] = code;
	}
	vector<int>* outputCode = new vector<int>();
	string currentString = "";
	string subString = "";
	int currentStringLength = 0;
	for (int i = 0; i < characters->size(); i++)
	{
		currentString += characters->at(i); // SERCEN: characters->at(i) demek, Java arrayList.get(i) demek 
		if (hashTable.find(currentString) == ITEM_NOT_FOUND)
		{
			codeMap[currentString] = code++;
			hashTable.insert(currentString);
			subString = currentString.substr(0, currentStringLength);
			outputCode->push_back(codeMap[subString]);
			currentString = characters->at(i);
			currentStringLength = 1;
		}
		else
		{
			currentStringLength++;
			if (i + 1 == characters->size())
			{
				currentString = characters->at(i);
				outputCode->push_back(codeMap[currentString]);

			}
		}
	}
	return outputCode;
}

vector<int>* loadLZW(string fileName)
{
	vector<int>* codes = new vector<int>();
	ifstream lzwFile(fileName, ios::binary);;
	bitset<2> numberOfCodesAsBits;
	lzwFile.read(reinterpret_cast<char*>(&numberOfCodesAsBits), 2);
	int numberOfCodes = numberOfCodesAsBits.to_ulong();
	for (int i = 0; i < numberOfCodes; i++)
	{
		bitset<2> codeAsBits;
		lzwFile.read(reinterpret_cast<char*>(&codeAsBits), 2);
		codes->push_back(codeAsBits.to_ulong());
	}
	lzwFile.close();
	return codes;
}
//sizeof(unsigned int).write((char*)&numberOfCodes, bitsNumber);
int main(int argc, char* argv[]) {
	loadLZW(argv[2]);

	//system("pause");
	return 0;
}
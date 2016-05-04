#include <iostream>

int main2(){
	int myArray[] = {31, -41, 59, 26, -53, 58, 97, -93, -23, 84};
	int bestSum = 0;
	int sum = 0;
	int counter = 0;
	for(int i = 0; i <= 9; i++){
		for(int j = i; j <= 9; j++){
			counter++;
			sum = sum + myArray[j];
			if(sum > bestSum){
				bestSum = sum;
			}

			std::cout << " i: " << i << " j: " << j << " sum: " << bestSum << std::endl;
		}
		sum = 0;
	}

	std::cout << "Count: " << counter << std::endl;

	return 0;

}

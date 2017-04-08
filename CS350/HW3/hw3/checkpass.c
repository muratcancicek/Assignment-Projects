/* Muratcan cicek, S004233 */
#include <stdio.h>
#include <string.h>

int compareStr(char *str1, char *str2)
{
	int i = 0;
	while (str1[i] != '\0' || str2[i] != '\0')
	{
		if (str1[i] != str2[i])
		{
			return 0;
		}
		i++;
	}
	if (str1[i] == '\0' && str2[i] == '\0')
		return 1;
	else
		return 0;
}

int main(int argc, char **argv)
{
	if (argc != 2)
	{
		printf("Next time, you must pass a password as an argument. Program terminating...\n");
		return 0;
	}

	char *actualPassword = argv[1], enteredPassword[100000];
	printf("Enter password:");
	scanf("%[^\n]%*c", enteredPassword);

	int tryCount = 3;
	while (!compareStr(actualPassword, enteredPassword))
	{
		if (tryCount <= 0)
		{
			printf("All passwords you entered were wrong. Program terminating...\n");
			return 0; 
		}
		printf("Try again (%i):", tryCount);
		scanf("%[^\n]%*c", enteredPassword);
		tryCount--;
	}

	printf("Correct password!\n");
	return 0;
}

/*-----------------------------------------------

gcc checkpass.c -o checkpass
./checkpass p
and
the
p


-----------------------------------------------*/
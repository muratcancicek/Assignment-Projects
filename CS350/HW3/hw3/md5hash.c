#include <stdio.h>
#include <string.h>
#include <openssl/md5.h>

int main(int argc, char **argv)
{
	
	char digest[MD5_DIGEST_LENGTH];
	const char* str = "homework3";

	MD5_CTX ctx;
	MD5_Init(&ctx);
	MD5_Update(&ctx, str, strlen(str));
	MD5_Final(digest, &ctx);

	char mdString[33];
	int n = 0;
	for (n = 0; n < 16; ++n) {
		snprintf(&(mdString[n * 2]), 16 * 2, "%02x", (unsigned int)digest[n]);
	}

	printf("MD5(%s) = %s\n", str, mdString);


	return 0;
}
/*-----------------------------------------------

gcc –o md5hash md5hash.c –lcrypto
./md5hash
./md5hash test.txt

-----------------------------------------------*/
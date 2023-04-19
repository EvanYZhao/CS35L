#ifndef OUTPUT_H
#define OUTPUT_H

#include <stdbool.h>

bool writebytes (unsigned long long x, int nbytes);
int stdioPrintFunction(long long nbytes, char* input);
int writeFunction(long long nbytes, char* input, int value);

#endif /* OUTPUT_H */

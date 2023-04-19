#ifndef RAND64_SW_H
#define RAND64_SW_H

#include <stdio.h>

void software_rand64_init(char* file);
unsigned long long software_rand64(void);
void software_rand64_fini(void);
/* Initialize the software mrand48_r implementation */
void software_mrand48_init(void);

/* Return a random value, using mrand48_r */
unsigned long long software_mrand48 (void);

/* Finalize the software mrand48_r implementation */
void software_mrand48_fini(void);

#endif /* RAND64_SW_H */

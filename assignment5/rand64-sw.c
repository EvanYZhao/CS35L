#include "rand64-sw.h"
#include <stdlib.h>
#include <time.h>

/* Input stream containing random bytes. */
static FILE *urandstream;

/* Initialize the software rand64 implementation.  */
void
software_rand64_init (char* file)
{
  urandstream = fopen (file, "r");
  if (! urandstream)
    abort ();
}

/* Return a random value, using software operations.  */
unsigned long long
software_rand64 (void)
{
  unsigned long long int x;
  if (fread (&x, sizeof x, 1, urandstream) != 1)
    abort ();
  return x;
}

/* Finalize the software rand64 implementation.  */
void
software_rand64_fini (void)
{
  fclose (urandstream);
}

/* Necessary Initialization parameters for mrand48_r */
static struct drand48_data rand_state;

/* Initialize the software mrand48_r implementation */
void
software_mrand48_init(void)
{
  srand48_r(time(NULL), &rand_state);
}

/* Return a random value, using mrand48 */
unsigned long long software_mrand48(void)
{
  long int x;
  mrand48_r(&rand_state, &x);
  return (unsigned long long)x;
}

/* Finalize the software mrand48_r implementation */
void
software_mrand48_fini(void)
{
}

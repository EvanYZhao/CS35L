#include "output.h"
#include "rand64-hw.h"
#include "rand64-sw.h"
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>

// Function that writes out a given value x to stdout using putchar() 
bool
writebytes (unsigned long long x, int nbytes)
{
  do
    {
      if (putchar (x) < 0)
	return false;
      x >>= CHAR_BIT;
      nbytes--;
    }
  while (0 < nbytes);

  return true;
}

int
stdioPrintFunction(long long nbytes, char* input)
{
  /* Now that we know we have work to do, arrange to use the
     appropriate library.  */
  void (*initialize) (void);
  unsigned long long (*rand64) (void);
  void (*finalize) (void);
  void (*swinit) (char *);
  if (strcmp(input, "rdrand") == 0) // -i rdrand case
    {
      initialize = hardware_rand64_init;
      rand64 = hardware_rand64;
      finalize = hardware_rand64_fini;
      initialize();
    }
  else if (strcmp(input, "mrand48_r") == 0) // -i mrand48_r case
    {
      initialize = software_mrand48_init;
      rand64 = software_mrand48;
      finalize = software_mrand48_fini;
      initialize();
    }
  else // -i FILE case
    {
      swinit = software_rand64_init;
      rand64 = software_rand64;
      finalize = software_rand64_fini;
      swinit(input);
    }

  int wordsize = sizeof rand64 ();
  int output_errno = 0;
  
  do
    {
      unsigned long long x = rand64 ();
      int outbytes = nbytes < wordsize ? nbytes : wordsize;
      if (!writebytes (x, outbytes))
	{
	  output_errno = errno;
	  break;
	}
      nbytes -= outbytes;
    }
  while (0 < nbytes);

  if (fclose (stdout) != 0)
    output_errno = errno;

  if (output_errno)
    {
      errno = output_errno;
      perror ("output");
    }

  finalize ();
  return !!output_errno;
}

int
writeFunction(long long nbytes, char* input, int value)
{
  /* Now that we know we have work to do, arrange to use the
      appropriate library.  */
  void (*initialize) (void);
  unsigned long long (*rand64) (void);
  void (*finalize) (void);
  void (*swinit) (char *);
  if (strcmp(input, "rdrand") == 0) // -i rdrand case
    {
      initialize = hardware_rand64_init;
      rand64 = hardware_rand64;
      finalize = hardware_rand64_fini;
      initialize();
    }
  else if (strcmp(input, "mrand48_r") == 0) // -i mrand48_r case
    {
      initialize = software_mrand48_init;
      rand64 = software_mrand48;
      finalize = software_mrand48_fini;
      initialize();
    }
  else // -i FILE case
    {
      swinit = software_rand64_init;
      rand64 = software_rand64;
      finalize = software_rand64_fini;
      swinit(input);
    }

  int output_errno = 0;
  long long *buf = (long long*)malloc(nbytes);
  if(buf == NULL)
    {
      fprintf(stderr, "failed to allocate memory");
      exit(EXIT_FAILURE);
    }
  /* Filling Buffer */
  int i;
  for (i = 0; i < nbytes; i+=8)
    {
      long long randomNum = rand64();
      buf[i/8] = randomNum;      
    }
  /* Fills remainder of buffer if nbytes is not divisible by 8 */
  if (nbytes % 8 != 0)
    {
      long long randomNum = rand64();
      int remainder = nbytes % 8;
      randomNum &= ((unsigned long long)1 << (remainder * 8)) - 1;
      char* remainingBuf = (char*)&buf[i/8];
      for (int j = 0; j < remainder; j++)
	{
	  remainingBuf[j] = (char)randomNum;
	  randomNum >>= 8;
	}
    }
  int bytes_written = 0;
  do
    {
      int blocksize = (nbytes - bytes_written) < value ? (nbytes - bytes_written) : value;
      bytes_written += write(STDOUT_FILENO, buf+bytes_written, blocksize);
      if (bytes_written == -1)
	{
	  fprintf(stderr, "write failed");
	  exit(EXIT_FAILURE);
	}
    }
  while(bytes_written != nbytes);
  finalize();
  free(buf);
  
  return !!output_errno;
}

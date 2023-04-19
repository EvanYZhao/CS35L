#include "options.h"
#include <stdlib.h>
#include <unistd.h>

long long nameArgCheck(int argc, char **argv){
  
  /* Check name argument using getopt  */
  long long nbytes;
  if(optind >= argc){
    printf("Error: Usage: %s [-i input] [-o output] NBYTES\n", argv[0]);
      exit(EXIT_FAILURE);
  }

  char *endptr;
  nbytes = strtoll(argv[optind], &endptr, 10);

  /* If there's no work to do, don't worry about which library to use.  */
  if (nbytes == 0)
    return 0;

  /* If all passes, return nbytes value to indicate to continue */
  return nbytes;
}

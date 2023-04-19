/* Generate N bytes of random output.  */

/* When generating output this program uses the x86-64 RDRAND
   instruction if available to generate random numbers, falling back
   on /dev/random and stdio otherwise.

   nThis program is not portable.  Compile it with gcc -mrdrnd for a
   x86-64 machine.

   Copyright 2015, 2017, 2020 Paul Eggert

   This program is free software: you can redistribute it and/or
   modify it under the terms of the GNU General Public License as
   published by the Free Software Foundation, either version 3 of the
   License, or (at your option) any later version.

   This program is distributed in the hope that it will be useful, but
   WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

#include "options.h"
#include "output.h"
#include "rand64-hw.h"
#include "rand64-sw.h"
#include <unistd.h>
#include <string.h>
#include <stdlib.h>

/* Main program, which outputs N bytes of random data.  */
int
main (int argc, char **argv)
{
  long long nbytes;
  char* input = "rdrand";
  char* output = "stdio";
  
  int opt;
  while((opt = getopt(argc, argv, "i:o:")) != -1){
    switch(opt){
    case 'i':
      input=optarg;
      break;
    case 'o':
      output=optarg;
      break;
    default:
      fprintf(stderr, "Usage: %s [-i input] [-o output] NBYTES\n", argv[0]);
      exit(EXIT_FAILURE);
    }
  }

  nbytes = nameArgCheck(argc, argv); /* Make sure this goes after processing options processing */

  /* If there's no work to do, then don't print anything */
  if (nbytes == 0){
    return 0;
  }
  
  // Takes input option and checks if default is supported or not
  if(strcmp(input, "rdrand") == 0){
    if (!rdrand_supported()){
      fprintf(stderr, "Error: RDRAND not supported\n");
      exit(EXIT_FAILURE);
    }
  }

  //Checks value of output option
  if(strcmp(output, "stdio") == 0){
    return stdioPrintFunction(nbytes, input);
  }
  else{
    int blocksize = atoi(output);
    if (blocksize <= 0){
      fprintf(stderr, "Error: value provided after -o must be a nonnegative, nonzero integer");
      exit(EXIT_FAILURE);
    }
    return writeFunction(nbytes, input, blocksize);
  }
}

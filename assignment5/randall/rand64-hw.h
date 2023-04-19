#ifndef RAND64_HW_H
#define RAND64_HW_H
#include <stdbool.h>

/* Hardware Implementation */

/* Description of the current CPU. */
struct cpuid { unsigned eax, ebx, ecx, edx; };

/* Returns information about the CPU. */
struct cpuid cpuid(unsigned int leaf, unsigned int subleaf);

/* Returns true if CPU supports the RDRAND instruction */
_Bool rdrand_supported(void);

/* Initialize the hardware rand64 implementation */
void hardware_rand64_init(void);

/* Return a random value, using hardware operations.  */
unsigned long long hardware_rand64 (void);

/* Finalize the hardware rand64 implementation.  */
void hardware_rand64_fini (void);

#endif /* RAND64_HW_H */

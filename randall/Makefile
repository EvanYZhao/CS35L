# Make x86-64 random byte generators.

# Copyright 2015, 2020, 2021 Paul Eggert

# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

# Optimization level.  Change this -O2 to -Og or -O0 or whatever.
OPTIMIZE = -O0

# The C compiler and its options.
CC = gcc
CFLAGS = $(OPTIMIZE) -g3 -Wall -Wextra -fanalyzer \
  -march=native -mtune=native -mrdrnd

# The archiver command, its options and filename extension.
TAR = tar
TARFLAGS = --gzip --transform 's,^,randall/,'
TAREXT = tgz

default: randall

randall: randall.c
	$(CC) $(CFLAGS) $@.c options.c rand64-hw.c rand64-sw.c output.c -o $@

assignment: randall-assignment.$(TAREXT)
assignment-files = COPYING Makefile randall.c
randall-assignment.$(TAREXT): $(assignment-files)
	$(TAR) $(TARFLAGS) -cf $@ $(assignment-files)

submission-tarball: randall-submission.$(TAREXT)
submission-files = $(assignment-files) \
  notes.txt options.* output.* rand64*
randall-submission.$(TAREXT): $(submission-files)
	$(TAR) $(TARFLAGS) -cf $@ $(submission-files)

repository-tarball:
	$(TAR) -czf randall-git.tgz .git

.PHONY: default clean assignment submission-tarball repository-tarball

check: randall
	./randall 1024 | wc -c | grep -q '^1024$$'
	./randall -i mrand48_r 1024 | wc -c | grep -q '^1024$$'
	./randall -i rdrand -o stdio 1024 | wc -c | grep -q '^1024$$'
	./randall -o 4 1024 | wc -c | grep -q '^1024$$'
	./randall -o 100 50 | wc -c | grep -q '^50$$'
	./randall -o 2 50 | wc -c | grep -q '^50$$'
	./randall -o 3 50 | wc -c | grep -q '^50$$'
	./randall -o 4 50 | wc -c | grep -q '^50$$'
	./randall -o 7 50 | wc -c | grep -q '^50$$'
	./randall -i /dev/urandom -o stdio 32 | wc -c | grep -q '^32$$'


clean:
	rm -f *.o *.$(TAREXT) randall

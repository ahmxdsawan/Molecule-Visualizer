CC = clang
CFLAGS = -Wall -std=c99 -pedantic -g
TESTFILE = test
INCLUDE = /Library/Frameworks/Python.framework/Versions/3.11/include/python3.11
LIB = /Library/Frameworks/Python.framework/Versions/3.11/lib

all: _molecule.so

libmol.so: mol.o
	$(CC) mol.o -shared -lm -o libmol.so

swig:
	swig -python molecule.i

_molecule.so: libmol.so molecule_wrap.o
	$(CC) $(CFLAGS) -shared molecule_wrap.o -L. -lmol -L$(LIB) -lpython3.11 -lmol -dynamiclib -o _molecule.so

molecule_wrap.o: swig molecule_wrap.c
	$(CC) $(CFLAGS) -c -fPIC -I$(INCLUDE) molecule_wrap.c -o molecule_wrap.o

molecule_wrap.c: molecule.i
	swig -python molecule.i

mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -c mol.c -fPIC -o mol.o
	
$(TESTFILE).o: $(TESTFILE).py mol.h
	$(CC) $(CFLAGS) -c $(TESTFILE).py -o $(TESTFILE).o

test3: clean all
	$(CC) $(CFLAGS) -L. test3.c -o test3 -lmol

run: $(TESTFILE).o
	$(CC) $(TESTFILE).o -L. -lmol -o run -lm -lpython3.11
	export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:.
	
clean:
	rm -f *.o *.so run test3 molecule.py molecule_wrap.c

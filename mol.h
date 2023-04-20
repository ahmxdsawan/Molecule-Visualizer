#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#ifndef M_PI

#define M_PI 3.1415926
#endif

typedef struct atom
{
    char element[3]; // A null-terminated string representing the element name of the atom (e.g. Na for sodium).

    double x, y, z; // x, y, and z are double precision floating point numbers describing the position in Angstroms (Å)
                    // of the atom relative to a common origin for a molecule.
} atom;

//a1 and a2 are indices of the two atoms in the co-valent bond within an array with address atoms.
//epairs is the number of electron pairs in the bond (i.e. epairs=2 represents a double bond).
//x1, y1, x2, y2 will store the x and y coordinates of atoms a1 and a2 respectively.
//z will store the average z value of a1 and a2. len will store the distance from a1 to a2.
//dx and dy will store the differences between the x and y values of a2 and a1 divided by the length of the bond.
typedef struct bond
{
    unsigned short a1, a2;
    unsigned char epairs;
    atom *atoms;
    double x1, x2, y1, y2, z, len, dx, dy;
} bond;

typedef struct molecule
{
    unsigned short atom_max, atom_no;
    atom *atoms, **atom_ptrs;
    unsigned short bond_max, bond_no;
    bond *bonds, **bond_ptrs;
} molecule;

// xform_matrix reprents a 3-d affine transformation matrix (an extension of the 2-d affine transformation you saw in the first lab).
typedef double xform_matrix[3][3];

// FUNCTION PROTOTYPES:

// This function should copy the values pointed to by element, x, y, and z into the atom stored at atom.
// You may assume that sufficient memory has been allocated at all pointer addresses.
// NOTE that using pointers for the function “inputs”, x, y, and z, is done here to match the function arguments of atomget.
void atomset(atom *atom, char element[3], double *x, double *y, double *z);

void atomget(atom *atom, char element[3], double *x, double *y, double *z);

void bondset( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs );

void bondget( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs );

void compute_coords( bond *bond );

int bond_comp( const void *a, const void *b );

molecule *molmalloc(unsigned short atom_max, unsigned short bond_max);

molecule *molcopy(molecule *src);

void molfree(molecule *ptr);

void molappend_atom(molecule *molecule, atom *atom);

void molappend_bond(molecule *molecule, bond *bond);

void molsort(molecule *molecule);

void xrotation(xform_matrix xform_matrix, unsigned short deg);

void yrotation(xform_matrix xform_matrix, unsigned short deg);

void zrotation(xform_matrix xform_matrix, unsigned short deg);

void mol_xform(molecule *molecule, xform_matrix matrix);


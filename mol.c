#include "mol.h"


void atomset(atom *atom, char element[3], double *x, double *y, double *z)
{

    strncpy(atom->element, element, 3); // copies the content from element into the struct
    atom->x = *x;                       // copies the value pointed to by x into the struct
    atom->y = *y;                       // copies the value pointed to by y into the struct
    atom->z = *z;                       // copies the value pointed to by z into the struct
}

// This function should copy the values pointed to by element, x, y, and z into the atom stored at atom.
// You may assume that sufficient memory has been allocated at all pointer addresses.
// Note that using pointers for the function “inputs”, x, y, and z, is done here to match the function arguments of atomget.
void atomget(atom *atom, char element[3], double *x, double *y, double *z)
{

    strncpy(element, atom->element, 3); // copies the content from the struct into the variable string element
    *x = atom->x;                       // copies the of x from the struct into the the value pointed by x
    *y = atom->y;                       // copies the of y from the struct into the the value pointed by y
    *z = atom->z;                       // copies the of z from the struct into the the value pointed by z
}

// This function should copy the values pointed to by a1, a2, atoms, and epairs into the corresponding structure attributes in bond. 
// In addition,you should call the compute_coords function (see below) on the bond.
void bondset( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs )
{
    bond->a1 = *a1;         // copies the address of a1 into the struct
    bond->a2 = *a2;         // copies the address of a2 into the struct
    bond->atoms = *atoms;
    bond->epairs = *epairs; // copies the address of epairs into the struct

    compute_coords(bond);
}

// This function should copy the structure attributes in bond to their corresponding arguments: a1, a2, atoms, and epairs.
void bondget( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs )
{

    *epairs = bond->epairs; // copies the number of bonds from the struct into epairs
    *atoms = bond->atoms;
    *a1 = bond->a1;         // copies the value of a1 from the struct into a1
    *a2 = bond->a2;         // copies the value of a2 from the struct into a2
}

// This function should return the address of a malloced area of memory, large enough to hold a molecule.
// The value of atom_max should be copied into the structure;
// the value of atom_no in the structure should be set to zero;
// the arrays atoms and atom_ptrs should be malloced to have enough memory to hold atom_max atoms and pointers (respectively).
// The value of bond_max should be copied into the structure;
// the value of bond_no in the structure should be set to zero;
// the arrays bonds and bond_ptrs should be malloced to have enough memory to hold bond_max bonds and pointers (respectively).

molecule *molmalloc(unsigned short atom_max, unsigned short bond_max)
{

    molecule *mol_mal = (struct molecule *)malloc(sizeof(struct molecule)); // allocating mol_mal sturct to hold enough memory to the size of a molecule

    // checking if the malloc was not succesful, and if not, it returns a NULL
    if (mol_mal == NULL)
    {
        return NULL;
    }

    mol_mal->atom_max = atom_max; // copying the value of atom_max into the new struct
    mol_mal->atom_no = 0;         // setting the value of number of atoms to 0
    mol_mal->bond_max = bond_max; // copying the value of bond_max into the new struct
    mol_mal->bond_no = 0;         // setting the value of number of bonds to 0

    mol_mal->atoms = (struct atom *)malloc(sizeof(atom) * atom_max); // mallocing atoms to have enough memory to hold atom_max atoms

    // checking if the malloc was not succesful, and if not, it returns a NULL
    if (mol_mal->atoms == NULL)
    {
        free(mol_mal);
        return NULL;
    }

    mol_mal->bonds = (struct bond *)malloc(sizeof(bond) * bond_max); // mallocing bonds to have enough memory to hold bond_max

    // checking if the malloc was not succesful, and if not, it returns a NULL
    if (mol_mal->bonds == NULL)
    {
        free(mol_mal->atoms);
        free(mol_mal);
        return NULL;
    }

    mol_mal->atom_ptrs = (struct atom **)malloc(sizeof(atom *) * atom_max); // mallocing atom pointers to have enough memory to hold atom_max atoms

    // checking if the malloc was not succesful, and if not, it returns a NULL
    if (mol_mal->atom_ptrs == NULL)
    {
        free(mol_mal->atoms);
        free(mol_mal->bonds);
        free(mol_mal);
        return NULL;
    }

    mol_mal->bond_ptrs = (struct bond **)malloc(sizeof(bond *) * bond_max); // mallocing bond pointers to have enough memory to hold bond_max

    // checking if the malloc was not succesful, and if not, it returns a NULL
    if (mol_mal->bond_ptrs == NULL)
    {
        free(mol_mal->atoms);
        free(mol_mal->bonds);
        free(mol_mal->atom_ptrs);
        free(mol_mal);
        return NULL;
    }

    // returning the address of the malloced area of memory
    return mol_mal;
}

// This function should return the address of a malloced area of memory, large enough to hold a  molecule.
// Additionally, the values of atom_max, atom_no, bond_max, bond_no should be copied from src into the new structure.
// Finally, the arrays atoms, atom_ptrs, bonds and bond_ptrs must be allocated to match the size of the ones in src.
// You should re-use (i.e. call) the molmalloc function in this function.

molecule *molcopy(molecule *src)
{

    unsigned short i;
    molecule *newStruct;

    newStruct = molmalloc(src->atom_max, src->bond_max);

    if (newStruct == NULL){
        return NULL;
    }

    newStruct->atom_no = src->atom_no; // copying the value of atom_no from src to the new struct
    newStruct->bond_no = src->bond_no; // copying the value of bond_no from src to the new struct

    // for loop that copies the value of atom_max and bond_max from src to the new struct
    for (i = 0; i < src->atom_no; i++){
        memcpy(newStruct->atoms + i, src->atoms + i, sizeof(atom));
        newStruct->atom_ptrs[i] = newStruct->atoms + i; // set the atoms pointer for the copied atom to the array of atom pointers in the copied molecule
    }

    // for loop that copies the value of bond_max and bond_max from src to the new struct
    for (i = 0; i < src->bond_no; i++){
        memcpy(newStruct->bonds + i, src->bonds + i, sizeof(bond));
        newStruct->bond_ptrs[i] = newStruct->bonds + i;
        newStruct->bonds[i].atoms =*newStruct->atom_ptrs; // set the bonds pointer for the copied bond to the bonds of bonds pointers in the copied molecule
    }
    return newStruct; // return the new struct
}

// This function should free the memory associated with the molecule pointed to by ptr
// This includes the arrays atoms, atom_ptrs, bonds, bond_ptrs.
void molfree(molecule *ptr)
{

    // freeing all the elements in the struct then finally freeing the whole struct to avoid any memory leaks
    free(ptr->atoms);
    free(ptr->atom_ptrs);
    free(ptr->bonds);
    free(ptr->bond_ptrs);
    free(ptr);
}

// This function should copy the data pointed to by atom to the first “empty” atom in atoms in the molecule pointed to by molecule
// Set the first “empty” pointer in atom_ptrs to the same atom in the atoms array incrementing the value of atom_no.
// If atom_no equals atom_max,then atom_max must be incremented, and the capacity of the atoms, and atom_ptrs arrays increased accordingly.
// If atom_max was 0, it should be incremented to 1, otherwise it should be doubled.
// Increasing the capacity of atoms,and atom_ptrs should bedone using realloc so that a larger amount of memory is allocated and the existing data is copied to the new location.
void molappend_atom(molecule *molecule, atom *atom)
{

    // if condition that checks if the number of atom max equals the number of atoms
    if (molecule->atom_max == molecule->atom_no)
    {
        // if condition that checks if atom max is equal to 0 then increment it to 1
        if (molecule->atom_max == 0)
        {
            molecule->atom_max = molecule->atom_max + 1;
        }
        // else multiply atom max by 2
        else
        {
            molecule->atom_max = molecule->atom_max * 2;
        }

        // if any of the conditions are met, then realloc, ie, move the content of the area to another memory location with an increased amount of memory.
        molecule->atoms = (struct atom *)realloc(molecule->atoms, sizeof(struct atom) * molecule->atom_max);
        molecule->atom_ptrs = (struct atom **)realloc(molecule->atom_ptrs, sizeof(struct atom *) * molecule->atom_max);
    }

    // for loop the moves the atom content to the new molecule
    for (int i = 0; i < molecule->atom_no; i++)
    {
        molecule->atom_ptrs[i] = &(molecule->atoms[i]);
    }

    molecule->atoms[molecule->atom_no] = *atom;
    molecule->atom_ptrs[molecule->atom_no] = &(molecule->atoms[molecule->atom_no]);
    // increment the number of atoms
    molecule->atom_no++;
}

// This function should operate like that molappend_atom function, except for bonds. // comments should be the same for mollappend_atom
void molappend_bond(molecule *molecule, bond *bond)
{

    if (molecule->bond_max == molecule->bond_no)
    {
        if (molecule->bond_max == 0)
        {
            molecule->bond_max++;
        }

        else
        {
            molecule->bond_max = molecule->bond_max * 2;
        }

        molecule->bonds = (struct bond *)realloc(molecule->bonds, sizeof(struct bond) * molecule->bond_max);
        molecule->bond_ptrs = (struct bond **)realloc(molecule->bond_ptrs, sizeof(struct bond *) * molecule->bond_max);
    }

    for (int i = 0; i < molecule->bond_no; i++)
    {
        molecule->bond_ptrs[i] = &(molecule->bonds[i]);
    }

    molecule->bonds[molecule->bond_no] = *bond;
    molecule->bond_ptrs[molecule->bond_no] = &(molecule->bonds[molecule->bond_no]);
    molecule->bond_no++;
}

int atom_cmp(const void *a, const void *b)
{
    const atom *double_a = *(const atom **)a;
    const atom *double_b = *(const atom **)b;

    if (double_a->z < double_b->z)
    {
        return -1;
    }

    else if (double_a->z > double_b->z)
    {
        return 1;
    }

    else
    {
        return 0;
    }
}

int bond_comp( const void *a, const void *b )
{
    bond **bond1 = (bond **)a;
    bond **bond2 = (bond **)b;


    if ((*bond1)->z < (*bond2)->z)
    {
        return -1;
    }

    else if ((*bond1)->z > (*bond2)->z)
    {
        return 1;
    }

    else
    {
        return 0;
    }
}

// This function should sort the atom_ptrs array in place in order of increasing z value. I.e.
// atom_ptrs[0] should point to the atom that contains the lowest z value and
// atom_ptrs[atom_no-1] should contain the highest z value. It should also sort the bond_ptrs
// array in place in order of increasing “ z value”. Since bonds don’t have a z attribute, their z
// value is assumed to be the average z value of their two atoms. I.e. bond_ptrs[0] should point
// to the bond that has the lowest z value and bond_ptrs[atom_no-1] should contain the highest
// z value.
void molsort(molecule *molecule)
{
    qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(atom *), atom_cmp);
    qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(bond *), bond_comp);
}

// This function will set the values in an affine transformation
// matrix, xform_matrix, corresponding to a rotation of deg degrees around the x-axis.
void xrotation(xform_matrix xform, unsigned short deg)
{

    double radians = deg * M_PI / 180; // converting to randians

    // setting the values that corresponds to the x-axis matrix
    xform[0][0] = 1;
    xform[0][1] = 0;
    xform[0][2] = 0;
    xform[1][0] = 0;
    xform[1][1] = cos(radians);
    xform[1][2] = -sin(radians);
    xform[2][0] = 0;
    xform[2][1] = sin(radians);
    xform[2][2] = cos(radians);
}

// This function will set the values in an affine transformation
// matrix, xform_matrix, corresponding to a rotation of deg degrees around the y-axis.
void yrotation(xform_matrix xform, unsigned short deg)
{

    double radians = deg * M_PI / 180; // converting to randians

    // setting the values that corresponds to the y-axis matrix
    xform[0][0] = cos(radians);
    xform[0][1] = 0;
    xform[0][2] = sin(radians);
    xform[1][0] = 0;
    xform[1][1] = 1;
    xform[1][2] = 0;
    xform[2][0] = -sin(radians);
    xform[2][1] = 0;
    xform[2][2] = cos(radians);
}

// This function will set the values in an affine transformation
// matrix, xform_matrix, corresponding to a rotation of deg degrees around the z-axis.
void zrotation(xform_matrix xform, unsigned short deg)
{

    double radians = deg * M_PI / 180; // converting to randians

    // setting the values that corresponds to the z-axis matrix
    xform[0][0] = cos(radians);
    xform[0][1] = -sin(radians);
    xform[0][2] = 0;
    xform[1][0] = sin(radians);
    xform[1][1] = cos(radians);
    xform[1][2] = 0;
    xform[2][0] = 0;
    xform[2][1] = 0;
    xform[2][2] = 1;
}

// This function will apply the transformation matrix to all the atoms of the molecule by
// performing a vector matrix multiplication on the x, y, z coordinates.
void mol_xform(molecule *molecule, xform_matrix matrix)
{

    for (unsigned short i = 0; i < molecule->atom_no; i++)
    {
        // Apply the transformation matrix to each atom
        atom *atm = &molecule->atoms[i];
        double x = atm->x, y = atm->y, z = atm->z;
        atm->x = matrix[0][0] * x + matrix[0][1] * y + matrix[0][2] * z;
        atm->y = matrix[1][0] * x + matrix[1][1] * y + matrix[1][2] * z;
        atm->z = matrix[2][0] * x + matrix[2][1] * y + matrix[2][2] * z;
    }

    for (unsigned short i = 0; i < molecule->bond_no; i++)
    {
        // Recompute the bond coordinates after transforming the atoms
        bond *bonds = &molecule->bonds[i];
        compute_coords(bonds);
    }
    
}

void compute_coords(bond *bond)
{

    atom *a1, *a2;

    a1 = &bond->atoms[bond->a1];
    a2 = &bond->atoms[bond->a2];

    bond->x1 = a1->x;
    bond->y1 = a1->y;
    bond->x2 = a2->x;
    bond->y2 = a2->y;
    bond->z = (a1->z + a2->z) / 2;
    bond->len = sqrt(pow(a2->x - a1->x, 2) + pow(a2->y - a1->y, 2));

    bond->dx = ((a2->x - a1->x) / bond->len);
    bond->dy = (a2->y - a1->y) / bond->len;
}

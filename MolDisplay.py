import molecule


# radius = {'H': 25,
#           'C': 40,
#           'O': 40,
#           'N': 40,
#           }

# element_name = {'H': 'grey',
#                 'C': 'black',
#                 'O': 'red',
#                 'N': 'blue',
#                 }

header = """<svg version="1.1" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">"""

footer = """</svg>"""

offsetx = 500
offsety = 500


# Atom Class

class Atom:

    # This class should be a wrapper class for your atom class/struct in your C code.
    # Objects of the Atom class should be initialized by calling an Atom(c_atom) constructor method with an atom class/struct as its argument.
    # The constructor should store the atom class/struct as a member variable. It should also initialize a member variable, z, to be the value in the wrapped class/struct.
    def __init__(self, c_atom):
        self.c_atom = c_atom
        self.z = c_atom.z

    def __str__(self):
        return f'Element: "%s", x: "%.2f", y: "%.2f", z: "%.2f\n' % (self.c_atom.element, self.c_atom.x, self.c_atom.y, self.c_atom.z,)

    def svg(self):
        cx = self.c_atom.x * 100.0 + offsetx
        cy = self.c_atom.y * 100.0 + offsety
        r = radius[self.c_atom.element]
        fill = element_name[self.c_atom.element]
        return f' <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % (cx, cy, r, fill)


class Bond:

        #Create a Bond class. This class should be a wrapper class for your bond class/struct in your C
        # code. Objects of the Bond class should be initialized by calling a Bond( c_bond ) constructor
        # function with an bond class/struct as its argument. The constructor should store the bond
        # class/struct as a member variable. It should also initialize a member variable, z, to be the value
        # in the wrapped class/struct.
    def __init__(self, c_bond):
        self.c_bond = c_bond
        self.z = c_bond.z

    def __str__(self):
        #for debugging purposous
        return f'a1: %.1f, a2: %.1f, epairs: %.1f, dx: %f, dy: %f, len: %f' % (self.c_bond.a1, self.c_bond.a2, self.c_bond.epairs, self.c_bond.dx, self.c_bond.dy, self.c_bond.len)

    def svg(self):

        # calculation to retrive the 8 points for the "thick" rectangle
        x1 = (self.c_bond.x1 * 100 + offsetx - self.c_bond.dy * 10)
        y1 = (self.c_bond.y1 * 100 + offsety + self.c_bond.dx * 10)

        x2 = (self.c_bond.x1 * 100 + offsetx + self.c_bond.dy * 10)
        y2 = (self.c_bond.y1 * 100 + offsety - self.c_bond.dx * 10)

        x3 = (self.c_bond.x2 * 100 + offsetx + self.c_bond.dy * 10)
        y3 = (self.c_bond.y2 * 100 + offsety - self.c_bond.dx * 10)

        x4 = (self.c_bond.x2 * 100 + offsetx - self.c_bond.dy * 10)
        y4 = (self.c_bond.y2 * 100 + offsety + self.c_bond.dx * 10)

        return '  <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' % (x1, y1, x2, y2, x3, y3, x4, y4) # return its svg string


class Molecule(molecule.molecule):

    # str method to debug the code
    def __str__(self):
        return f'Atoms: {self.atoms}, Bonds: {self.bonds}'

    # an svg method
    def svg(self):

        # string = ""
        # string += header

        # a_index = 0
        # b_index = 0

        # for i in range(self.atom_no + self.bond_no):
            
        #     if a_index < self.atom_no:
        #         a1 = Atom(self.get_atom(a_index));
        #     if b_index < self.bond_no:
        #         b1 = Bond(self.get_bond(b_index));

        #     if a1.z < b1.z:

        #         string += a1.svg();
        #         if a_index < self.atom_no:
        #             a_index += 1;
        #         else:
        #             string += b1.svg();
        #     else:

        #         if b_index < self.bond_no and b1.z < a1.z:

        #             string += b1.svg();
        #             if b_index < self.bond_no:
        #                 b_index += 1;

        #         else:

        #             string += a1.svg();
        #             if a_index + 1 < self.atom_no:
        #                 a_index += 1;

        # string += footer
        # return string


        string = "" # initialize an empty string array
        string += header # add the header into the empty string list

        # for loop that equaits an atom at every index
        atoms = [Atom(self.get_atom(i)) for i in range(self.atom_no)]
        # for loop that equaits an bond at every index
        bonds = [Bond(self.get_bond(i)) for i in range(self.bond_no)]
        items = atoms + bonds # add the bonds and atom attributes into an items array
        items_sorted = sorted(items, key=lambda item: item.z) # make a new array and sort it using lambda and z value

        # for loop that goes through the sorted list and calls the svg method and appends them into the original string
        for item in items_sorted:
            string += item.svg()

        string += footer # append the footer into the string
        return string # return the string

    def parse(self, sdf):

        # for loop that skips the first three lines
        for i in range(3):
            line = sdf.readline()

        line = sdf.readline() # let line #4 equal the string line
        line = line.split() # split the string into elemented array

        num_atoms = int(line[0]) # let the first index being 0 equal the total number of atoms
        num_bonds = int(line[1]) # let the second index being 1 equal the total number of bonds
        

        # for loop that reads every line in the range of the number of atoms
        for i in range(num_atoms):
            line = sdf.readline() # let line equal the string line

            if isinstance(line, bytes):
                line = line

            # if type (function) is string dont decode if it is byte decode

            x = line[:10] # x = the fisrt 10 characters
            y = line[10:20] # y = the characters between 10 and 20
            z = line[20:30] # z = the characters between 20 and 30
            element = line[31:34] # element equal characters between 31 and 34

            # appending the attributes of an element using append_atom (reasoning behind using strip is to delete any qoutation marks present)
            self.append_atom(element.strip(), float(x), float(y), float(z))

        # for loop that reads every line in the range of the number of bonds
        for i in range(num_bonds):

            line = sdf.readline() # let line equal the string line

            if isinstance(line, bytes):
                line = line.decode()
            
            
            a1, a2, bond_type = map(int, line.split()[:3]) # then use the map function the append everything into their apprioriate vatiables
            self.append_bond(a1-1, a2-1, bond_type) # finally append the attrubutes of a bond using append_bond


#
#       Testing my methods:
#
if __name__ == "__main__":

    with open("CID_31260.sdf", "rb") as f:
        mol = Molecule()
        mol.parse(f)
        svg_str = mol.svg()
        with open("output.svg", "w") as svg_file:
            svg_file.write(svg_str)

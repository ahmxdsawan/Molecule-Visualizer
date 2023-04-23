import os
import sqlite3
import MolDisplay
import molecule


class Database:

    def __init__(self, reset=False):
        if reset and os.path.exists("molecules.db"):
            os.remove("molecules.db")
        self.conn = sqlite3.connect("molecules.db")
        self.cursor = self.conn.cursor()

    def create_tables(self):

        self.conn.execute("""CREATE TABLE IF NOT EXISTS Elements 
            (   ELEMENT_NO      INTEGER NOT NULL,
                ELEMENT_CODE    VARCHAR(3) PRIMARY KEY NOT NULL,
                ELEMENT_NAME    VARCHAR(32) NOT NULL,
                COLOUR1         CHAR(6) NOT NULL,
                COLOUR2         CHAR(6) NOT NULL,
                COLOUR3         CHAR(6) NOT NULL,
                RADIUS          DECIMAL(3) NOT NULL );""")

        self.conn.execute("""CREATE TABLE IF NOT EXISTS Atoms 
            (   ATOM_ID         INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                ELEMENT_CODE    VARCHAR(3) NOT NULL,
                X               DECIMAL(7,4) NOT NULL,
                Y               DECIMAL(7,4) NOT NULL,
                Z               DECIMAL(7,4) NOT NULL,
                FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements );""")

        self.conn.execute("""CREATE TABLE IF NOT EXISTS Bonds 
            (   BOND_ID     INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                A1          INTEGER NOT NULL,
                A2          INTEGER NOT NULL,
                EPAIRS      INTEGER NOT NULL );""")

        self.conn.execute("""CREATE TABLE IF NOT EXISTS Molecules 
            (   MOLECULE_ID     INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                NAME            TEXT UNIQUE NOT NULL );""")

        self.conn.execute("""CREATE TABLE IF NOT EXISTS MoleculeAtom 
            (   MOLECULE_ID     INTEGER NOT NULL,
                ATOM_ID         INTEGER NOT NULL,
                PRIMARY KEY (MOLECULE_ID, ATOM_ID),
                FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                FOREIGN KEY (ATOM_ID) REFERENCES Atoms );""")

        self.conn.execute("""CREATE TABLE IF NOT EXISTS MoleculeBond 
            (   MOLECULE_ID     INTEGER NOT NULL,
                BOND_ID         INTEGER NOT NULL,
                PRIMARY KEY (MOLECULE_ID, BOND_ID),
                FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                FOREIGN KEY (BOND_ID) REFERENCES Bonds );""")

        self.conn.commit()

    def __setitem__(self, table, values):
        placeholders = ", ".join("?" * len(values))
        query = f"INSERT INTO {table} VALUES ({placeholders})"
        self.conn.execute(query, values)
        self.conn.commit()

    # This method should add the attributes of the atom object (class MolDisplay.Atom) to the
    # Atoms table, and add an entry into the MoleculeAtom table that links the named molecule
    # to the atom entry in the Atoms table.
    def add_atom(self, molname, atom):
        c = self.conn.cursor()  # Creates a cursor object to interact with the database
        c.execute("INSERT INTO Atoms(ELEMENT_CODE, X, Y, Z) VALUES (?, ?, ?, ?)", (atom.element,
                  atom.x, atom.y, atom.z))  # Inserts the atom's attributes into the Atoms table
        self.conn.commit()  # Commits the changes to the database
        atom_id = c.lastrowid  # Fetches the ID of the newly inserted atom
        # Links the atom to the specified molecule in the MoleculeAtom table
        c.execute(
            "INSERT INTO MoleculeAtom(MOLECULE_ID, ATOM_ID) VALUES (?, ?)", (molname, atom_id))
        self.conn.commit()  # Commits the changes to the database

    # This method should add the attributes of the bond object (class MolDisplay.Bond) to the
    # Bonds table, and add an entry into the MoleculeBond table that links the named molecule to
    # the atom entry in the Bonds table.
    def add_bond(self, molname, bond):
        c = self.conn.cursor()
        c.execute("INSERT INTO Bonds(A1, A2, EPAIRS) VALUES (?, ?, ?)",
                  (bond.a1, bond.a2, bond.epairs))
        self.conn.commit()
        bond_id = c.lastrowid
        c.execute(
            "INSERT INTO MoleculeBond(MOLECULE_ID, BOND_ID) VALUES (?, ?)", (molname, bond_id))
        self.conn.commit()

    def add_molecule(self, name, fp):
        mol = MolDisplay.Molecule()
        mol.parse(fp)

        self.cursor.execute(f"INSERT INTO Molecules (name) VALUES ('{name}')")

        mol_id = self.cursor.lastrowid

        for i in range(mol.atom_no):
            atom = mol.get_atom(i)
            self.add_atom(mol_id, atom)

        for i in range(mol.bond_no):
            bond = mol.get_bond(i)
            self.add_bond(mol_id, bond)

        self.conn.commit()

    def load_mol(self, name):
        atom_query = f"""SELECT Atoms.ATOM_ID, ELEMENT_CODE, X, Y, Z
                    FROM Atoms
                    JOIN MoleculeAtom ON Atoms.ATOM_ID = MoleculeAtom.ATOM_ID
                    JOIN Molecules ON MoleculeAtom.MOLECULE_ID = Molecules.MOLECULE_ID
                    WHERE Molecules.NAME = '{name}'
                    """
        atoms = self.conn.execute(atom_query).fetchall()

        bond_query = f"""SELECT Bonds.BOND_ID, A1, A2, EPairs
                    FROM Bonds
                    JOIN MoleculeBond ON Bonds.BOND_ID = MoleculeBond.BOND_ID
                    JOIN Molecules ON MoleculeBond.MOLECULE_ID = Molecules.MOLECULE_ID
                    WHERE Molecules.NAME = '{name}'
                    """
        bonds = self.conn.execute(bond_query).fetchall()

        mol = MolDisplay.Molecule()
        for atom in atoms:
            mol.append_atom(atom[1], atom[2], atom[3], atom[4])
        for bond in bonds:
            mol.append_bond(bond[1], bond[2], bond[3])
        return mol

    def radius(self):
        self.cursor.execute("SELECT ELEMENT_CODE, RADIUS FROM Elements")
        return dict(self.cursor.fetchall())

    def element_name(self):
        query = "SELECT ELEMENT_CODE, ELEMENT_NAME FROM Elements;"
        self.cursor.execute(query)
        elements = {}
        for row in self.cursor.fetchall():
            elements[row[0]] = row[1]
        return elements

    def radial_gradients(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3 FROM Elements")
        elements = cursor.fetchall()
        gradients = []
        for element in elements:
            radialGradientSVG = """
            <radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
                <stop offset="0%%" stop-color="#%s"/> 
                <stop offset="50%%" stop-color="#%s"/> 
                <stop offset="100%%" stop-color="#%s"/>
            </radialGradient>""" % (element[0], element[1], element[2], element[3])
            gradients.append(radialGradientSVG)
        return ''.join(gradients)


# if __name__ == "__main__":

#     db = Database(reset=True)
#     db.create_tables()

#     db['Elements'] = (1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25)
#     db['Elements'] = (6, 'C', 'Carbon', '808080', '010101', '000000', 40)
#     db['Elements'] = (7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40)
#     db['Elements'] = (8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40)
#     fp = open('water-3D-structure-CT1000292221.sdf')
#     db.add_molecule('Moi2', fp)
#     # fp = open('caffeine-3D-structure-CT1001987571.sdf')
#     # db.add_molecule('Caffeine', fp)
#     # fp = open('CID_31260.sdf')
#     # db.add_molecule('Isopentanol', fp)
#     # # display tables

#     print("ELEMENTS TABLE:")
#     print(db.conn.execute("SELECT * FROM Elements;").fetchall())
#     print("MOLECULES TABLE:")
#     print(db.conn.execute("SELECT * FROM Molecules;").fetchall())
#     print("ATOMS TABLE:")
#     print(db.conn.execute("SELECT * FROM Atoms;").fetchall())
#     print("BONDS TABLE:")
#     print(db.conn.execute("SELECT * FROM Bonds;").fetchall())
#     print("MoleculesATOM TABLE:")
#     print(db.conn.execute("SELECT * FROM MoleculeAtom;").fetchall())
#     print("MoleculeBond TABLE:")
#     print(db.conn.execute("SELECT * FROM MoleculeBond;").fetchall())

#     db = Database(reset=False)  # or use default

#     MolDisplay.radius = db.radius()
#     MolDisplay.element_name = db.element_name()
#     MolDisplay.header += db.radial_gradients()


#     for molecule in ['Moi2']:
#         mol = db.load_mol(molecule)
#         mol.sort()
#         fp = open(molecule + ".svg", "w")
#         fp.write(mol.svg())
#         fp.close()




import cgi
import json
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import MolDisplay
from molsql import Database
import sqlite3
import molecule

mol = MolDisplay.Molecule()

conn = sqlite3.connect("molecules.db")
cursor = conn.cursor()

db = Database(reset=True)
db.create_tables()

global_molname = ""
global_svg = ""

# db['Elements'] = (1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25)
# db['Elements'] = (6, 'C', 'Carbon', '808080', '010101', '000000', 40)
# db['Elements'] = (7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40)
# db['Elements'] = (8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40)


class MyHandler(BaseHTTPRequestHandler):
    # store the names of the molecules
    molecules = {}

    # dictionary to store mapping of url path to html file path
    pages = {
        "/": "index.html",
        "/molecule.js": "molecule.js",
        "/add_remove.html": "add_remove.html",
        "/upload.html": "upload.html",
        "/style.css": "style.css",
        "/pic.png": "pic.png"
    }

    def do_GET(self):
        # check if the requested path is present in the pages dictionary
        if self.path in self.pages:
            page_path = self.pages[self.path]
            # read the requested file and send it as response
            with open(page_path, "rb") as file:
                content = file.read()
            self.send_response(200)

            if self.path.endswith(".js"):
                self.send_header("Content-type", "text/javascript")

            elif self.path.endswith(".css"):
                self.send_header("Content-type", "text/css")

            elif self.path.endswith(".png"):
                self.send_header("Content-type", "image/png")

            else:
                self.send_header("Content-type", "text/html")

            self.send_header("Content-length", len(content))
            self.end_headers()
            self.wfile.write(content)
        else:
            # if requested path is not present in the pages dictionary
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: not found", "utf-8"))


    def do_POST(self):
        if self.path == "/upload.html":
            
            print("YOU ENTERED POST UPLOAD")


            db = Database(reset=False)
            db.create_tables()
            

            # parse the form data
            form_data = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )

            # get the uploaded file name and molecule name from the form data
            file_item = form_data['sdf_file']
            
            file_name = os.path.basename(file_item.filename)
            # print(file_name)
            molecule_name = form_data['mol_name'].value
            # print(molecule_name)
            # read the uploaded file data
            file_data = file_item.file.read()
            # print(file_data)

            # write the uploaded file to the server
            with open(file_name, 'wb') as f:
                f.write(file_data)
            
            file_path = os.path.abspath(file_name)
            print(file_path)

            with open(file_path) as f:
                fp = open(file_path)
                db.add_molecule(molecule_name, fp)

                print("ELEMENTS TABLE:")
                print(db.conn.execute("SELECT * FROM Elements;").fetchall())
                print("MOLECULES TABLE:")
                print(db.conn.execute("SELECT * FROM Molecules;").fetchall())
                print("ATOMS TABLE:")
                print(db.conn.execute("SELECT * FROM Atoms;").fetchall())
                print("BONDS TABLE:")
                print(db.conn.execute("SELECT * FROM Bonds;").fetchall())
                print("MoleculesATOM TABLE:")
                print(db.conn.execute("SELECT * FROM MoleculeAtom;").fetchall())
                print("MoleculeBond TABLE:")
                print(db.conn.execute("SELECT * FROM MoleculeBond;").fetchall())
                

                # do something with the file
                pass

            print("ATOMS TABLE:")
            print(db.conn.execute("SELECT * FROM Atoms;").fetchall())
            print("BONDS TABLE:")
            print(db.conn.execute("SELECT * FROM Bonds;").fetchall())

            db = Database(reset=False)  # or use default

            MolDisplay.radius = db.radius()
            MolDisplay.element_name = db.element_name()
            MolDisplay.header += db.radial_gradients()

            molname = str(molecule_name)

            for molecule in [molname]:

                mol = db.load_mol(molecule)
                mol.sort()
                svg = mol.svg()
                svg = svg.replace('"', "'")

                
                # fp = open(molecule + ".svg", "w")
                # fp.write(mol.svg())
                # fp.close()
            print(svg)
            
            # print("MOLECULES TABLE:")
            # print(db.conn.execute("SELECT * FROM Molecules;").fetchall())            

            # add the molecule to the molecule list
            # self.molecules[molecule_name] = svg

            # create an option tag for the new molecule
            with open('index.html', 'r') as f:
                index_html = f.read()

            option_tag = f'\n        <option value="{molecule_name}" data-svg="{svg}">{molecule_name.capitalize()}</option>'
            select_index = index_html.find('molecule-select')
            option_index = index_html.rfind('</option>', select_index) + len('</option>')
            new_index_html = index_html[:option_index] + option_tag + index_html[option_index:]

            with open('index.html', 'w') as f:
                f.write(new_index_html)


                
            # redirect to the main HTML page
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
        
        elif self.path == "/add_remove.html":
            print("YOU ENTERED POST ADD ELEMENT")

            db = Database(reset=False)
            db.create_tables()

            
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )

            action_type = form.getfirst('action_type', '')
            print(f"action_type = {action_type}")



            if action_type == 'add':

                element_number = form.getvalue('element_number')
                element_code = form.getvalue('element_code')
                element_name = form.getvalue('element_name')
                color1 = form.getvalue('color1')
                color2 = form.getvalue('color2')
                color3 = form.getvalue('color3')
                radius = form.getvalue('radius')
                
                db['Elements'] = (element_number, element_code, element_name, color1, color2, color3, radius)

                print("ELEMENTS TABLE:")
                print(db.conn.execute("SELECT * FROM Elements;").fetchall())
                db.conn.commit()


                
                # redirect to the add_remove.html page
                self.send_response(303)
                self.send_header('Location', '/add_remove.html')
                self.end_headers()

            # elif action_type == 'remove':

            #     element_number = form.getvalue('element_number')

                

            #     db.conn.execute("DELETE FROM Elements WHERE ELEMENT_NO=?", (element_number,))
            #     db.conn.commit()

            #     print("ELEMENTS TABLE:")
            #     print(db.conn.execute("SELECT * FROM Elements;").fetchall())

            #     # redirect to the add_remove.html page
            #     self.send_response(303)
            #     self.send_header('Location', '/add_remove.html')
            #     self.end_headers()

            elif action_type == 'remove':

                print("ENTERED THE REMOVE BUTTON NORMAL")

                element_number = form.getvalue('element_number')

                

                db.conn.execute("DELETE FROM Elements WHERE ELEMENT_NO=?", (element_number,))
                db.conn.commit()

                print("ELEMENTS TABLE:")
                print(db.conn.execute("SELECT * FROM Elements;").fetchall())

                # redirect to the add_remove.html page
                self.send_response(303)
                self.send_header('Location', '/add_remove.html')
                self.end_headers()

            elif action_type == 'remove-list':

                print("ENTERED THE REMOVE BUTTON TABLE")

                element_number = form.getvalue('elementNumber')

                print(element_number)

                db.conn.execute("DELETE FROM Elements WHERE ELEMENT_NO=?", (element_number,))
                db.conn.commit()

                print("ELEMENTS TABLE:")
                print(db.conn.execute("SELECT * FROM Elements;").fetchall())

                # redirect to the add_remove.html page
                self.send_response(303)
                self.send_header('Location', '/add_remove.html')
                self.end_headers()

            # elif self.path == "/remove_element":
            #     print("REMOVED ELEMENT")

            #     form = cgi.FieldStorage(
            #         fp=self.rfile,
            #         headers=self.headers,
            #         environ={'REQUEST_METHOD': 'POST'}
            #     )

            #     element_number = form.getvalue('element_number')

            #     db = Database(reset=False)
            #     db.conn.execute("DELETE FROM Elements WHERE ELEMENT_NO=?", (element_number,))
            #     db.conn.commit()

            #     # redirect to the add_remove.html page
            #     self.send_response(303)
            #     self.send_header('Location', '/add_remove.html')
            #     self.end_headers()

        # elif self.path == "/add_remove.html":
        #     print("YOU ENTERED POST REMOVE ELEMENT")

        #     form = cgi.FieldStorage(
        #         fp=self.rfile,
        #         headers=self.headers,
        #         environ={'REQUEST_METHOD': 'POST'}
        #     )

        #     element_number = form.getvalue('element_number')

        #     db.conn.execute("DELETE FROM Elements WHERE element_number = ?", (element_number,))
        #     db.conn.commit()

        #     self.send_response(303)
        #     self.send_header('Location', '/add_remove.html')
        #     self.end_headers()


        elif self.path == "/":
            print("ENTER MAIN PAGE POST")

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: not found", "utf-8"))



if __name__ == '__main__':
    # create the HTTP server
    httpd = HTTPServer(('localhost', int(sys.argv[1])), MyHandler)
    print(f"Server started on http://localhost:{sys.argv[1]}")
    httpd.serve_forever()

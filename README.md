# Molecule Visualizer

The Molecule Visualizer is a software tool that allows users to visualize molecules in high-quality 3D graphics. This program is designed with the combination of Python, C, HTML, JavaScript, CSS, and SQL, and utilizes Swig to link C and Python libraries. With this program, users can upload an SDF file containing the desired molecule and enter elements to visualize them in stunning detail.

## Features

- User-friendly interface
- High-quality 3D graphics
- Customizable visual properties (e.g., color, radius size)
- Multiple viewing options
- SQL database for storing user preferences and molecule data

## Installation

1. Clone the repository:

```python
git clone https://github.com/your-username/molecule-visualizer.git
```

2. Export the dependencies:

```python
export LD_LIBRARY_PATH=.
```

3. Link the files:

```python
make
```

**Note:** If you encounter an error when running `make`, such as "Python.h file not found", you may need to update the `INCLUDE` and `LIB` paths in the `Makefile` to match your own Python path. For example, if you're using Python 3.11 installed via Homebrew on macOS, you might need to change the paths to:
```python
INCLUDE = /usr/local/Cellar/python@3.11/3.11.0_1/Frameworks/Python.framework/Versions/3.11/include/python3.11
LIB = /usr/local/Cellar/python@3.11/3.11.0_1/Frameworks/Python.framework/Versions/3.11/lib
```

4. Run the program:

```python
python3 server.py 5500
```

**Note:** 5500 is the port number, you can choose a diffirent port number to your liking

## Usage

1. Enter elements to visualize
2. Upload an SDF file containing the desired molecule
3. Customize visual properties as desired
4. View molecule from different angles and perspectives

## Screenshots

Here are some screenshots of the molecule visualizer in action:

![Home Page](https://i.imgur.com/RPMW807.png)
*Figure 1: The Home Page*

![Elements Page](https://i.imgur.com/2Ut7hV9.png)
*Figure 2: The Elements Page*

![Upload Page](https://i.imgur.com/pmnobQP.png)
*Figure 3: The Upload Page*



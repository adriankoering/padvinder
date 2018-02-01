# Padvinder

Padvinder is a little pathtracing renderer written in Python. Originally I was keen to implement my own pathtracer.

## Example Usage

Run an example renering from the root of the repository via
```
python -m padvinder
```
I find this to be cleaner and shorter than having a main.py file. It makes use of Python's ability to execute modules. Under the hood \_\_main\_\_.py is executed.

## Tests

Run the tests similarly to running the example via
```
python -m padvinder.test
```
Again, this executes the \_\_main\_\_.py file in the test module while keeping the command line concise.

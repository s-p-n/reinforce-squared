# reinforce-squared
A machine learning environment with live configuration. (Based on a SentDex tutorial)

Okay, don't use this yet. It's not ready.

# Environment
	This is a Python3 project. See the top of `run.py` for the dependencies. You can probably use pip3 to install everything that's needed to run this.

# Where did this code come from?
* `qlearning-4.py` is pretty much straight from Sentdex's tutorial located here: https://pythonprogramming.net/own-environment-q-learning-reinforcement-learning-python-tutorial/
* `qlearning-4.py` is only for reference, and will be removed from later versions. It is not a dependency of `run.py` and so is not needed.
* `run.py` is based on `qlearning-4.py`, but has several added features supplied by me, Spencer A. Lockhart. 

# Installing this project
If python3 exists at `/usr/bin/python3`, the following code should get you at least to some python3 dependency errors:
```
cd ~
git clone https://github.com/s-p-n/reinforce-squared.git
cd reinforce-squared
python3 ./run.py
```
You might get a message about libraries not being installed, similar to this:
```
Traceback (most recent call last):
  File "./run.py", line 2, in <module>
    import foo
ModuleNotFoundError: No module named 'foo'
```
Where `foo` is the name of the module you need to install using something like:
```
pip3 install foo
``` 

Obviously, `foo` is not a real library- make sense?

So yeah, just keep attempting to run the program, and installing libraries as needed using `pip`.

# Running the program:
The payload is `run.py`. It comes with a line at the top of the file like so:

```
python3 run.py
```

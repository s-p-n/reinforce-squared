# reinforce-squared
A machine learning environment with live configuration. (Based on a SentDex tutorial)

I really love this program, I hope you do too. I tried to make it friendly to non-programmers, but still challenge the non-programmer or new programmer to get it working, and reward them with a quite satisfying command-line interface.

This is experimental. By proceding, you agree that nobody is liable for anything that happens as a result of executing this code. If you are interested in trying **reinforce-squared**, here's how I suggest getting things set-up.
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
The payload is `run.py`

```
python3 run.py
```


You should (eventually) be greeted with all of this:
```
WARNING:	using default config
	^-- Fix by running `save latest`
Please wait, as I try loading ./latest.pickle..
Welp, I failed to find ./latest.pickle.
Please wait while I create a q_table.
This will take a while.
Pro tip, you can save your work to resume later. The command is `save latest`

|   Type 'h' or 'help' or '-h' or '--help' for this dialog.  |
|   Do not close the simulation windows (it crashes)         |
|   Type 'q' or 'CTRL+C' over-and-over to quit               |
|   Type 'save latest' to save to latest                     |
|   Type 'save backup' to save to a time-stamped filename    |
|---You may configure the environment.-----------------------|
|   Type 'list' to show the current configuration            |
|   Type something like:                                     |
|       > enemyHandicap = 1                                  |
|   Or something like:                                       |
|       > bounds=False                                       |
|   to alter a configuration entry.                          |


> 
```


Don't worry about the warnings for now. Basically, follow the directions. This is a cheap-o command-line interface running on a seperate thread. It's really cool, you can change the environment while the model is learning, and it leads to pretty smart models. Here's the fun part. Are the models overfitting? Find out by changing the suggested settings, and see what happens!



# Happy Modelling!!

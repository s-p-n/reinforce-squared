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
If python3 exists at `/usr/bin/python3`, the following code should get you setup:
```
cd ~
git clone https://github.com/s-p-n/reinforce-squared.git
cd reinforce-squared
pip3 install opencv-python matplotlib image numpy
python3 ./run.py
```
Hopefully that gets all the dependencies. Otherwise, hit up Google and find the needed packages.

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

Once you're in, you can try typing a command, such as `list`:
```
> list
	sleepTime = 0.02
	showEvery = 500
	movePenalty = 1
	timeoutPenalty = 75
	enemyPenalty = 150
	foodReward = 150
	epsilon = 0.6065003298938891
	epsilonDecay = 0.9998
	learningRate = 0.1
	discount = 0.95
	enemyHandicap = 100
	enemyCount = 1
	bounds = True
	playerFirst = True
	iterations = 100
```

Now that you know all of the configuration names and value-types, you can attempt to alter them.

Go ahead and try making the environment wrap around instead of having outer walls using `bounds = False`

I think this model is too dumb to learn how to evade a faster enemy. But just for kicks, let's make the enemy as fast as your model:
```
> enemyHandicap = 1
```
... Wait...

Woah, that model is getting pretty smart! We'd better **save**:
```
> save latest
Would you like to save the current configuration? (y|n)y
Saving config..
Saving to 'latest.pickle'..
```
Cool, Python pauses the simulation while the save is in progress, and once the save is complete, your model is saved, but also remains in memory and resumes running.
# Happy Modelling!!

#!/usr/bin/python3
import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time
import random
import re
from threading import Thread,Lock
import json

SIZE = 25

class globalVars():
    pass

class Blob:
    def __init__(self):
        self.x = np.random.randint(0, SIZE)
        self.y = np.random.randint(0, SIZE)

    def __str__(self):
        return f"{self.x}, {self.y}"

    def __sub__(self, other):
        return (self.x-other.x, self.y-other.y)

    def action(self, choice):
        '''
        Gives us 4 total movement options. (0,1,2,3)
        '''
        if choice == 0:
            self.move(x=-1, y=-1)
        elif choice == 1:
            self.move(x=-1, y=0)
        elif choice == 2:
            self.move(x=-1, y=1)
        elif choice == 3:
            self.move(x=0, y=-1)
        elif choice == 4:
            self.move(x=0, y=0)
        elif choice == 5:
            self.move(x=0, y=1)
        elif choice == 6:
            self.move(x=1, y=-1)
        elif choice == 7:
            self.move(x=1, y=0)
        elif choice == 8:
            self.move(x=1, y=1)

    def moveTowards(self, target):
        x = 0
        #if target.x == self.x:
        #    x = 0
        if target.x < self.x:
            x = -1
        elif target.x > self.x:
            x = 1

        y = 0
        #if target.x == self.x:
        #    x = 0
        if target.y < self.y:
            y = -1
        elif target.y > self.y:
            y = 1

        return self.move(x, y)

    def move(self, x=False, y=False):

        # If no value for x, move randomly
        if not x:
            self.x += np.random.randint(-1, 2)
        else:
            self.x += x

        # If no value for y, move randomly
        if not y:
            self.y += np.random.randint(-1, 2)
        else:
            self.y += y


        # If we are out of bounds, fix!
        if G.configuration["bounds"]:
            if self.x < 0:
                self.x = 0
            elif self.x > SIZE-1:
                self.x = SIZE-1
            if self.y < 0:
                self.y = 0
            elif self.y > SIZE-1:
                self.y = SIZE-1
        else:
            if self.x < 0:
                self.x = SIZE+self.x
            elif self.x >= SIZE:
                self.x = 0
            if self.y < 0:
                self.y = SIZE+self.y
            elif self.y >= SIZE:
                self.y = 0

style.use("ggplot")
plt.ion()
G = globalVars()
G.lock = Lock()
G.fig = plt.figure()
G.quit = False
G.episode_rewards = []

start_q_table = "./latest.pickle" # None or Filename

PLAYER_N = 1  # player key in dict
FOOD_N = 2  # food key in dict
ENEMY_N = 3  # enemy key in dict

# the dict!
d = {1: (255, 175, 0),
     2: (0, 255, 0),
     3: (0, 0, 255)}

def loadConfig (configFile):
    try:
        with open(configFile) as json_file:
            G.configuration = json.load(json_file)
    except FileNotFoundError:
        with open('default.json') as json_file:
            print("WARNING:\tusing default config")
            print("\t^-- Fix by running `save latest`")
            G.configuration = json.load(json_file)

def saveConfig (configFile):
    with open(configFile, 'w') as json_file:
        json.dump(G.configuration, json_file)

def commandPrompt():
    first = True
    while True:
        prompt = """
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
"""
        if first:
            first = False
            print(prompt)
        go = input("\n> ")
        helpList = [
            'h',
            'help',
            '-h',
            '--help'
        ]
        if go in helpList:
            print(prompt)
        elif go == 'q':
            print("Stopping..")
            G.quit = True
            #plt.close('all')
            exit(0)
        elif go[0:4] == 'save':
            target = go.split(' ')[1]
            if target == 'latest':
                answer = ''
                while answer != 'y' and answer != 'n':
                    answer = input("Would you like to save the current configuration? (y|n)").lower()
                
                if answer == 'y':
                    print("Saving config..")
                    saveConfig('latest.json')
                print(f"Saving to 'latest.pickle'..")
                with open("latest.pickle", "wb") as f:
                    pickle.dump(q_table, f)
            elif target == 'backup':
                fn = f"qtable-{int(time.time())}.pickle"
                print(f"Saving to {fn}")
                with open(fn, "wb") as f:
                    pickle.dump(q_table, f)
        elif go == 'list':
            for name, value in G.configuration.items():
                print(f"\t{name} = {value}")
        else:
            cmd = re.match("([a-zA-Z]+)\s*\=\s*([0-9]+(?:\.[0-9]+)?|[a-zA-Z0-9]+)", go)
            if cmd == None:
                print("Unrecognized Command.")
                continue
            name, val = cmd.groups()
            if name in G.configuration:
                try:
                    if type(G.configuration[name]) is bool:
                        val = val != "False"
                    else:
                        val = type(G.configuration[name])(val)
                    G.configuration[name] = val
                    if name == "showEvery":
                        print("Resetting episode rewards..")
                        G.episode_rewards = []
                    print(f"{name} = {val}")
                except Exception:
                    print("Type-error, try again.")
                    pass
            else:
                print(f"I'm sorry, the name '{name}' is not in the configuration.\nRemember, type 'list' to view the configurable options.")

loadConfig('./latest.json')

tCmd = Thread(target=commandPrompt)
#tChart = Thread(target=liveChart)
            
print(f"Please wait, as I try loading {start_q_table}..")
try:
    with open(start_q_table, "rb") as f:
        q_table = pickle.load(f)
except FileNotFoundError:
    print(f"Welp, I failed to find {start_q_table}.")
    print("Please wait while I create a q_table.")
    print("This will take a while.")
    print("Pro tip, you can save your work to resume later. The command is `save latest`")
    q_table = {}
    for i in range(-SIZE+1, SIZE):
        for ii in range(-SIZE+1, SIZE):
            for iii in range(-SIZE+1, SIZE):
                    for iiii in range(-SIZE+1, SIZE):
                        q_table[((i, ii), (iii, iiii))] = [np.random.uniform(-5, 0) for i in range(9)]

tCmd.start()
#tChart.start()
# can look up from Q-table with: print(q_table[((-9, -2), (3, 9))]) for example

episode = 0
while G.quit == False:
    # Configuration:
    sleepTime = G.configuration["sleepTime"]
    SHOW_EVERY = G.configuration["showEvery"]
    ITERATION_PENALTY = G.configuration["timeoutPenalty"]
    MOVE_PENALTY = G.configuration["movePenalty"]
    ENEMY_PENALTY = G.configuration["enemyPenalty"]
    FOOD_REWARD = G.configuration["foodReward"]
    epsilon = G.configuration["epsilon"]
    EPS_DECAY = G.configuration["epsilonDecay"]
    LEARNING_RATE = G.configuration["learningRate"]
    DISCOUNT = G.configuration["discount"]
    enemyHandicap = G.configuration["enemyHandicap"]
    enemyCount = G.configuration["enemyCount"]

    # Episode Cast (as in, cast for a TV Show/Movie)
    player = Blob()
    food = Blob()
    enemies = []
    for i in range(enemyCount):
        enemies.append(Blob())


    # Episode Tracking
    if episode % SHOW_EVERY == 0:
        show = True
    else:
        show = False


    episode_reward = 0
    j = 0
    episode += 1



    for i in range(G.configuration["iterations"]):
        if G.quit == True:
            break
        start_dist = np.linalg.norm(player-food)
        enemy = enemies[j]
        j += 1
        if j == len(enemies):
            j = 0

        #### move enemy toward player ###
        if i % enemyHandicap == 0:
            enemy.moveTowards(player)

        obs = (player-food, player-enemy)

        if np.random.random() > epsilon:
            # GET THE ACTION
            action = np.argmax(q_table[obs])
        else:
            action = np.random.randint(0, 9)
        # Take the action!
        player.action(action)

        #foodDist = np.linalg.norm(player-food)
        #enemyDist = np.linalg.norm(player-enemy)
        playerEaten = player.x == enemy.x and player.y == enemy.y
        foodEaten = player.x == food.x and player.y == food.y
        if playerEaten:
            reward = -ENEMY_PENALTY
        elif foodEaten:
            reward = FOOD_REWARD
        elif i == (G.configuration["iterations"] - 1):
            reward = -ITERATION_PENALTY
        else:
            reward = -MOVE_PENALTY
        # first we need to obs immediately after the move.
        new_obs = (player-food, player-enemy)
        max_future_q = np.max(q_table[new_obs])
        current_q = q_table[obs][action]

        if reward == FOOD_REWARD:
            new_q = FOOD_REWARD
        else:
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
        q_table[obs][action] = new_q
        if show:
            env = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)  # starts an rbg of our size
            env[food.x][food.y] = d[FOOD_N]  # sets the food location tile to green color
            env[player.x][player.y] = d[PLAYER_N]  # sets the player tile to blue
            env[enemy.x][enemy.y] = d[ENEMY_N]  # sets the enemy location to red
            img = Image.fromarray(env, 'RGB')  # reading to rgb. Apparently. Even tho color definitions are bgr. ???
            img = img.resize((800, 800))  # resizing so we can see our agent in all its glory.
            cv2.imshow("image", np.array(img))  # show it!
            time.sleep(sleepTime)
            if reward == FOOD_REWARD or reward == -ENEMY_PENALTY:  # crummy code to hang at the end if we reach abrupt end for good reasons or not.
                if cv2.waitKey(500) & 0xFF == ord('q'):
                    break
            else:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        episode_reward += reward
        if reward == FOOD_REWARD or reward == -ENEMY_PENALTY:
            break
    G.episode_rewards.append(episode_reward)
    G.configuration['epsilon'] *= EPS_DECAY
    if show:
        moving_avg = np.convolve(G.episode_rewards, np.ones((G.configuration["showEvery"],))/G.configuration["showEvery"], mode='valid')
        plt.plot([i for i in range(len(moving_avg))], moving_avg)
        plt.ylabel(f"Reward {G.configuration['showEvery']}ma")
        plt.xlabel("episode #")
        plt.pause(1)
        plt.clf()
# tic-tac-toe
A human can challenge three algorithms (random, deep q-network, minimax) in the game [tic-tac-toe](https://en.wikipedia.org/wiki/Tic-tac-toe) with the scripts provided in this repository.
The gameplay has several restrictions:
* the human plays mark X while the machine plays mark O,
* the human player starts the game,
* in the first game, the machine plays according to the deep q-network (DQN) policy.

The policy of the machine player can be changed from the main menu.
Changing the policy invokes the reset of the game.

The training script of the DQN is also enclosed in the repository, however, both the observation and the action spaces and the hyperparamters are not aligned to the task.

### Files in the repo
```
.
├── Dockerfile		- definition file for the docker container
├── LICENSE		- license terms
├── README.md		- you are reading this at the moment
├── XOEnv.py		- game backend in a gymnasium-compatible format
├── dqn_model.zip	- a trained DQN policy
├── game.py		- GUI for the game
├── requirements.txt	- pip requirements for the game
└── train_rl_agent.py	- training script for the DQN policy
```

### Setting up an environment for training the DQN policy
The game and the training of the DQN policy depend on Python 3.11, TkInter (python3-tk) and some other Python packages those can be installed by invoking:
`pip install -r requirements.txt`
.

### Docker
To run the game with the pretrained DQN policy, either a Python environment has to be set up or a docker container (tested only on native Linux) must be built by invoking:
`docker build -f Dockerfile --tag xo .`
.

To display the GUI, the following command is needed:
`xhost +local:docker`
.

The container can be started with:
```
docker run -e DISPLAY=$DISPLAY \
           -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
           -v $HOME/.Xauthority:/root/.Xauthority:rw \
           --net=host \
           --rm -it xo
```
.

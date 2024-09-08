import copy
import numpy as np
import gymnasium as gym
from stable_baselines3 import DQN

class XOEnv(gym.Env):
    def __init__(self, machine_policy='random', render_mode=None):
        self.num_rows = 3
        self.num_cols = 3
        self.size = self.num_rows * self.num_cols
        self.board = np.zeros((self.size,), dtype=np.float32)
        self.board_rectangular_view = self.board.reshape((self.num_rows, self.num_cols))
        self.episode_length = 0

        self.id_x = 1
        self.id_o = 4
        self.id_draw = -10
        self.mm_cnt = 0

        if machine_policy == 'random':
            self.machine_policy = self.random_policy
        elif machine_policy == 'minimax':
            self.machine_policy = self.minimax_policy
        elif machine_policy == 'dqn':
            self.machine_policy = self.dqn_policy
            self.dqn_model = DQN.load('dqn_model')

        self.observation_space = gym.spaces.Box(
                low = -.5,
                high = .5,
                shape = (self.size,),
                dtype = np.float32
                )
        self.action_space = gym.spaces.Discrete(self.size)

    def reset(self, seed=0):
        self.board.fill(0)
        self.episode_length = 0

        observation = self.get_semi_normalized_observation()
        info = {}
        return observation, info

    def step(self, move_of_x):
        reward = 0
        terminated = False
        if self.is_valid_move(move_of_x):
            self.board[move_of_x] = self.id_x
            self.episode_length += 1

            if not self.terminal(self.board):
                move_of_o, _ = self.machine_policy(board=self.board, is_maximizing=False, alpha=-100, beta=100)
                self.board[move_of_o] = self.id_o
                self.episode_length += 1
        else:
            reward = -1
            terminated = True

        info = {'winner': None}
        if self.episode_length >= 5:
            terminal_of_id = self.terminal(self.board)
            if terminal_of_id:
                terminated = True
                info = {'winner': terminal_of_id}
                if terminal_of_id == self.id_x:
                    reward = 1#-self.episode_length
                elif terminal_of_id == self.id_o:
                    #reward = self.episode_length-10
                    reward = -1
                elif terminal_of_id == self.id_draw:
                    reward = .5

        observation = self.get_semi_normalized_observation()
        return observation, reward, terminated, False, info

    def get_semi_normalized_observation(self):
        flattened_board = copy.deepcopy(self.board)
        flattened_board[flattened_board == self.id_x] = .5
        flattened_board[flattened_board == self.id_o] = -.5
        return flattened_board

    def is_valid_move(self, action):
        if action < self.size:
            if self.board[action] == 0:
                return True
        return False

    def is_winner(self, board, player_id):
        three_marks_sum = 3*player_id
        board_rectangular_view = board.reshape((self.num_rows, self.num_cols))
        if not np.any((np.sum(board_rectangular_view, axis=0) - three_marks_sum) == 0):
            if not np.any((np.sum(board_rectangular_view, axis=1) - three_marks_sum) == 0):
                if not np.any((np.trace(board_rectangular_view) - three_marks_sum) == 0):
                    if not np.any((np.trace(np.flipud(board_rectangular_view)) - three_marks_sum) == 0):
                        return False
        return True
                
    def terminal(self, board):
        terminal_of_id = None
        if self.is_winner(board, self.id_x):
            terminal_of_id = self.id_x
        elif self.is_winner(board, self.id_o):
            terminal_of_id = self.id_o
        elif len(board.nonzero()[0]) == self.size:
            terminal_of_id = self.id_draw
        return terminal_of_id

    def random_policy(self, **kwargs):
        # TODO: replace to shuffle vec and find the first valid move
        move = np.random.randint(low=0, high=self.size)
        while not self.is_valid_move(move):
            move = np.random.randint(low=0, high=self.size)
        return move, 0

    def minimax_policy(self, board, is_maximizing, alpha, beta):
        self.mm_cnt += 1
        terminal_of_id = self.terminal(board)
        best_move = None
        if terminal_of_id:
            if terminal_of_id == self.id_x:
                best_value = 1
            elif terminal_of_id == self.id_o:
                best_value = -1
            elif terminal_of_id == self.id_draw:
                best_value = 0
        else:
            possible_moves = np.where(board == 0)[0]
            if is_maximizing:
                best_value = -10
                for move in possible_moves:
                    branch_board = copy.deepcopy(board)
                    branch_board[move] = self.id_x
                    _, value = self.minimax_policy(branch_board, not is_maximizing, alpha, beta)
                    if value > best_value:
                        best_value = value
                        best_move = move
                    alpha = max(alpha, best_value)
                    if beta <= alpha:
                        break
            else:
                best_value = 10
                for move in possible_moves:
                    branch_board = copy.deepcopy(board)
                    branch_board[move] = self.id_o
                    _, value = self.minimax_policy(branch_board, not is_maximizing, alpha, beta)
                    if value < best_value:
                        best_value = value
                        best_move = move
                    beta = min(beta, best_value)
                    if beta <= alpha:
                        break
        return best_move, best_value

    def dqn_policy(self, **kwargs):
        observation = self.get_semi_normalized_observation()
        action, _ = self.dqn_model.predict(observation, deterministic=True)
        return action, 0

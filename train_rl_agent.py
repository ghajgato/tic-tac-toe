from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.evaluation import evaluate_policy

from XOEnv import XOEnv

trn_env = make_vec_env(XOEnv, env_kwargs={'machine_policy': 'random'}, n_envs=8, vec_env_cls=DummyVecEnv)

model = DQN("MlpPolicy", trn_env, exploration_fraction=.5, gamma=.98, verbose=0)
model.learn(total_timesteps=2000000, progress_bar=True)
model.save('tempo')

eval_env = XOEnv(machine_policy='random')
print(evaluate_policy(model, eval_env, 100))
eval_env = XOEnv(machine_policy='minimax')
print(evaluate_policy(model, eval_env, 100))

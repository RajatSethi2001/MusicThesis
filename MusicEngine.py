import numpy as np
import torch
from MusicEnv import MusicEnv
from os.path import exists
from stable_baselines3 import PPO, TD3
from stable_baselines3.common.noise import NormalActionNoise

env = MusicEnv()
model_name = "MusicModelTD3.zip"
buffer_size = 100000
n_timesteps = 1
learning_starts = 32
train_freq = 4
gradient_steps = 4
batch_size = 1

n_actions = env.action_space.shape[-1]
action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))

policy_kwargs = dict(net_arch=[64, 64])

model = TD3(
    'MlpPolicy',
    env,
    buffer_size=buffer_size,
    learning_starts=learning_starts,
    batch_size=batch_size,
    train_freq=train_freq,
    gradient_steps=gradient_steps,
    action_noise=action_noise,
    policy_kwargs=policy_kwargs,
    verbose=1)

if (exists(f"{model_name}")):
    model.set_parameters(model_name)

done = False

while not done:
    model.learn(n_timesteps)
    model.save(model_name)
    train_more = input("Continue training? [Y/N]: ")
    if not (train_more in "yY"):
        done = True
    
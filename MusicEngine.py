import os
import torch
from MusicEnv import MusicEnv
from os.path import exists
from stable_baselines3 import PPO

env = MusicEnv()
model_name = "MusicModel.zip"

if (exists(f"{model_name}")):
    model = PPO.load(model_name, env=env)
else:
    policy_kwargs = dict(
        activation_fn=torch.nn.ReLU,
        net_arch=[64, 64, 64]
    )
    model = PPO('MlpPolicy', env, n_steps=8, batch_size=4, policy_kwargs=policy_kwargs)

done = False

while not done:
    model.learn(1)
    model.save(f"{model_name}")
    train_more = input("Continue training? [Y/N]: ")
    if not (train_more in "yY"):
        done = True
    
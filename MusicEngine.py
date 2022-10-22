import os
from MusicEnv import MusicEnv
from os.path import exists
from stable_baselines3 import PPO

env = MusicEnv()
model_name = "MusicModel"

model = PPO('MlpPolicy', env, n_steps=4, batch_size=2)
if (exists(f"{model_name}.zip")):
    model.set_parameters(model_name)

done = False

while not done:
    model.learn(1)
    model.save("MusicModel")
    train_more = input("Continue training? [Y/N]: ")
    if not (train_more in "yY"):
        done = True
    
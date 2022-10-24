## PYTHON PACKAGES - USE LATEST VERSION
- numpy
- torch
- gym
- stable-baselines3
- python-vlc
- midiutil

## APT PACKAGES - USE LATEST VERSION
- python3
- vlc
- timidity
- ffmpeg

## HOW IT WORKS - HOW TO USE
- This project uses reinforcement learning to generate music. 
- Before running, you can change the "model_name" variable to either use an existing model or a new one.
- To train the algorithm, simply run "python3 MusicEngine.py".
- Each iteration, the trainer will be given two frames, each with three notes.
- The trainer then rates the CURRENT frame on a scale of 1-10, based on how well it continues the previous frame.
- Once rated, the algorithm generates a new "current" frame, and the user rates it compared to the previous frame.
- Each frame is composed out of three notes.
- Each note has three characteristics, pitch, delay, duration.
- Both the observation and the action spaces are a frame (a 1x9 vector).
- Theoretically (with enough training), the model should be able to generate an endless song.
- Note: stable-baselines3 takes forever to train, it could easily take over 10,000+ steps to get anything good.

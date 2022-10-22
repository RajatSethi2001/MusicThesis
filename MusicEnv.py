from contextlib import contextmanager
import gym
import numpy as np
import os
import sys
import time
import vlc

from contextlib import contextmanager
from gym.spaces import Box
from midiutil import MIDIFile

features_per_note = 3
notes_per_frame = 3
features_per_frame = features_per_note * notes_per_frame

class MusicEnv(gym.Env):
    def __init__(self):
        self.observation_space = Box(low=0.0, high=1.0, shape=(1, features_per_frame), dtype=np.float32)
        self.action_space = Box(low=0.0, high=1.0, shape=(1, features_per_frame), dtype=np.float32)
        self.prev_frame = tuple([0 for _ in range(features_per_frame)])
        self.current_frame = tuple([0 for _ in range(features_per_frame)])
        self.vlc_instance = vlc.Instance()
        self.player = self.vlc_instance.media_player_new()
        self.player.audio_set_volume(100)

    def step(self, action):
        self.prev_frame = self.current_frame
        self.current_frame = tuple(action[0])
        self.render()
        reward = None
        while reward is None or reward < 0 or reward > 10:
            try:
                reward = int(input("Rate the continuation [0-10]: "))
                if reward < 0 or reward > 10:
                    print("Input out of range.")
            except:
                print("Invalid input.")

        # input("Please close out of the MIDI file, then press any key.")
        return self.current_frame, self.scale(reward, 0, 10), False, {}

    def reset(self):
        self.prev_frame = tuple([0 for _ in range(features_per_frame)])
        self.current_frame = ([0 for _ in range(features_per_frame)])
        return self.prev_frame

    def render(self):
        frame_file = self.convert_frames_to_midi([self.prev_frame, self.current_frame])
        
        media = self.vlc_instance.media_new(frame_file)
        self.player.set_media(media)
        self.player.play()
        time.sleep(1.5)
        duration = self.player.get_length() / 1000
        time.sleep(duration)

    def convert_frames_to_midi(self, frames):
        track = 0
        channel = 0
        volume = 100

        mf = MIDIFile()
        mf.addTempo(track, 0, 120)

        total_delay = 0
        for frame in range(len(frames)):
            frame_delay = 0
            for note in range(notes_per_frame):
                pitch = 0
                delay = 0
                duration = 0
                for feature in range(features_per_note):
                    index = note * features_per_note + feature
                    value = frames[frame][index]
                    if feature == 0:
                        pitch = int(self.unscale(value, 0, 127))
                    elif feature == 1:
                        delay = int(self.unscale(value, 0, 15))
                    elif feature == 2:
                        duration = int(self.unscale(value, 0, 15))
                    else:
                        raise Exception("Too many features per note.")
                if (delay + duration > frame_delay):
                    frame_delay = delay + duration
                print(f"Frame {frame + 1} - Note {note + 1}: Pitch {pitch} - Delay {delay} - Duration {duration}")
                mf.addNote(track, frame * notes_per_frame + note, pitch, total_delay + delay, duration, volume)
            total_delay += frame_delay
            print()
        
        midi_file = "output.mid"
        with open(midi_file, "wb") as outf:
            mf.writeFile(outf)
        
        mp3_file = "output.mp3"
        os.system(f"timidity {midi_file} -Ow -o - --quiet=2 | ffmpeg -i - -acodec libmp3lame -ab 64k -y -v 0 {mp3_file}")
        return mp3_file
    
    def scale(self, value, current_min, current_max):
        return (value - current_min) / (current_max - current_min)

    def unscale(self, value, new_min, new_max):
        new_value = value * (new_max - new_min) + new_min
        new_value = max(new_value, new_min)
        new_value = min(new_value, new_max)
        return new_value
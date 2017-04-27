import asyncio
import datetime
import ctypes

import vlc
from vlc import *
import glob

def callbackmethod(callback):
    """Now obsolete @callbackmethod decorator."""
    return callback

class Player:
    songs = []
    volume = 50
    songs_i = 0

    @callbackmethod
    def end_callback(self, bla):
        print('!', flush=True, end=' ')
        self.play()
    
    def __init__(self, songs, volume = 50):
        self.songs = songs
        self.volume = volume
        self.songs_i = 0
        
    def play_song(self, song):
        head, tail = os.path.split(song)
        print("[Playing {0}]".format(tail), flush=True, end=' ')
        
        self.i=vlc.Instance()
        self.p=self.i.media_player_new()
        self.event_manager = self.p.event_manager()
        self.event_manager.event_attach(EventType.MediaPlayerEndReached, self.end_callback)

        self.m=self.i.media_new(song)
        self.p.set_media(self.m)
        self.p.audio_set_volume(self.volume)
        self.p.play()
    
    def play(self):
        self.songs_i = self.songs_i + 1
        if self.songs_i >= len(self.songs):
            self.songs_i = 0
        
        self.play_song(self.songs[self.songs_i])
    
    def stop(self):
        self.p.stop()

class Sleepy:
    loop = None

    def __init__(self, running_path):
        self.running_path = running_path
        self.loop = asyncio.get_event_loop()
    
    async def hibernate_for(self, how_long):
        end_time = self.loop.time() + how_long
        while True:
            print('.', flush=True, end=' ')
            if (self.loop.time() + 1.0) >= end_time:
                break
            await asyncio.sleep(1)
    
    def play(self, folder_name, how_long, volume):
        self.loop.run_until_complete(self.play_folder(folder_name, how_long, volume))
    
    def go(self):
        self.loop.close()
    
    def go(self, audios):
        for audio in audios:
            self.play(audio['folder'], audio['time'], audio['volume'])
        self.loop.close()

    async def play_folder(self, folder_name, how_long, volume):
        print("[Going to play this folder for {0} hours]".format(how_long / 60))
        player = Player(
            self.get_all_songs_in_folder(self.running_path + "/sounds/" + folder_name, 'wav') + 
            self.get_all_songs_in_folder(self.running_path + "/sounds/" + folder_name, 'mp3'),
            volume)
        player.play()
        await self.hibernate_for(how_long)
        player.stop()
        print("")
        print("[Done with this folder]")
        print("")


    def get_all_songs_in_folder(self, folder, ext):
        songs = []
        path = folder + '\*.' + ext
        for name in glob.glob(path):
            songs.append(name)
            continue
        
        return songs
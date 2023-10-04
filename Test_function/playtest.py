from pydub import AudioSegment
from pydub.playback import play

# soundfile='../config/testmus1.wav'
soundfile='test10.wav'

song=AudioSegment.from_wav(soundfile)
play(song)
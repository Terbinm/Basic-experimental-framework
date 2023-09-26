#讀取config
from function.ConfigLoader import ConfigLoader
config_data = ConfigLoader('config').config_dict


#開始錄音
from function.ThreadingRecording import AudioExperiment
Experiment_Sound = AudioExperiment(config_data).run_experiment
print(Experiment_Sound)
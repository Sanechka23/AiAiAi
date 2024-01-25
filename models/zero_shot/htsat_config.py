# Ke Chen
# knutchen@ucsd.edu
# Zero-shot Audio Source Separation via Query-based Learning from Weakly-labeled Data
# The configuration file of ST-SED model or HTS-AT model

exp_name = "exp_htsat_2048d" # the saved ckpt prefix name of the model 

dataset_type = "audioset" 

loss_type = "clip_bce"
balanced_data = True

esc_fold = 0 # just for esc dataset, select the fold you need for evaluation and (+1) validation

debug = False

random_seed = 970131 # 19970318 970131 12412 127777 1009 34047
batch_size = 32 * 4 # batch size per GPU x GPU number , default is 32 x 4 = 128
learning_rate = 1e-3 # 1e-4 also workable 
max_epoch = 100
num_workers = 3

lr_scheduler_epoch = [10,20,30]
lr_rate = [0.02, 0.05, 0.1]


# for model's design
enable_tscam = True # enbale the token-semantic layer

# for signal processing
sample_rate = 32000 # 16000 for scv2, 32000 for audioset and esc-50
clip_samples = sample_rate * 10 # audio_set 10-sec clip
window_size = 1024
hop_size = 320 # 160 for scv2, 320 for audioset and esc-50
mel_bins = 64
fmin = 50
fmax = 14000
shift_max = int(clip_samples * 0.5)

# for data collection
classes_num = 527 # esc: 50 | audioset: 527 | scv2: 35
patch_size = (25, 4) # deprecated
crop_size = None # int(clip_samples * 0.5) deprecated

# for htsat hyperparamater
htsat_window_size = 8
htsat_spec_size =  256
htsat_patch_size = 4 
htsat_stride = (4, 4)
htsat_num_head = [4,8,16,32]
htsat_dim = 256 # for 2048-d model
htsat_depth = [2,2,6,2]

swin_pretrain_path = None

# Some Deprecated Optimization in the model design, check the model code for details
htsat_attn_heatmap = False
htsat_hier_output = False 
htsat_use_max = False

# map 527 classes into 10 classes
fl_audioset_mapping = [
    [0,1,2,3,4,5,6,7],
    [366, 367, 368],
    [364],
    [288, 289, 290, 291, 292, 293, 294, 295, 296, 297],
    [369],
    [382],
    [310, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402],
    [81, 82, 83, 84, 85],
    [74, 75, 76, 77, 78, 79],
    [377]
]
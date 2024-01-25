import torch
import torchaudio
from torchaudio.pipelines import HDEMUCS_HIGH_MUSDB_PLUS
from spleeter.separator import Separator
from torchaudio.transforms import Fade

def separate_sources(model, mix, segment=10.0, overlap=0.1, device = None, sample_rate = None):
    """
    Apply model to a given mixture. Use fade, and add segments together in order to add model segment by segment.

    Args:
        segment (int): segment length in seconds
        device (torch.device, str, or None): if provided, device on which to
            execute the computation, otherwise `mix.device` is assumed.
            When `device` is different from `mix.device`, only local computations will
            be on `device`, while the entire tracks will be stored on `mix.device`.
    """
    if device is None:
        device = mix.device
    else:
        device = torch.device(device)

    batch, channels, length = mix.shape

    chunk_len = int(sample_rate * segment * (1 + overlap))
    start = 0
    end = chunk_len
    overlap_frames = overlap * sample_rate
    fade = Fade(fade_in_len=0, fade_out_len=int(overlap_frames), fade_shape="linear")

    final = torch.zeros(batch, len(model.sources), channels, length, device=device)

    while start < length - overlap_frames:
        chunk = mix[:, :, start:end]
        with torch.no_grad():
            out = model.forward(chunk)
        out = fade(out)
        final[:, :, :, start:end] += out
        if start == 0:
            fade.fade_in_len = int(overlap_frames)
            start += int(chunk_len - overlap_frames)
        else:
            start += chunk_len
        end += chunk_len
        if end >= length:
            fade.fade_out_len = 0
    return final

def run_combined_model(SONG_PATH):
    #remove_extension = lambda s : s[:s.rfind('.')]
    #get_extension = lambda s : s[s.rfind('.')+1:]

    CONFIG_PATH = "models/combined_model/spleeter_config.json"
    #SONG_PATH = "music/Lykke_Li_I_Follow_Rivers_The_Magician_Remix.mp3"
    DIR_PATH = "predict_outputs"

    #SONG_PATH_WITHOUT_EXT = remove_extension(SONG_PATH)
    #EXT = get_extension(SONG_PATH)
    EXT = "mp3"

    DRUMS_PATH = DIR_PATH + "/drums." + EXT
    VOCALS_PATH = DIR_PATH + "/vocals." + EXT
    BASS_PATH = DIR_PATH + "/bass." + EXT

    separator = Separator(CONFIG_PATH)
    bundle = HDEMUCS_HIGH_MUSDB_PLUS
    model = bundle.get_model()
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)
    sample_rate = bundle.sample_rate


    # ffmpeg должна быть инициализирована, чтобы была возможность подгружать mp3 файлы
    torchaudio._extension._init_ffmpeg()
    #print(f"ffmpeg initialized : {torchaudio._extension._FFMPEG_INITIALIZED}")

    waveform, sample_rate = torchaudio.load(SONG_PATH) 
    waveform = waveform.to(device)
    mixture = waveform

    # parameters
    segment: int = 10
    overlap = 0.1

    ref = waveform.mean(0)
    waveform = (waveform - ref.mean()) / ref.std()  # normalization

    sources = separate_sources(
        model,
        waveform[None],
        device=device,
        segment=segment,
        overlap=overlap,
        sample_rate = sample_rate
    )[0]

    sources = sources * ref.std() + ref.mean()

    sources_list = model.sources
    sources = list(sources)

    audios = dict(zip(sources_list, sources))

    torchaudio.save(VOCALS_PATH, audios["vocals"].cpu(), sample_rate)
    torchaudio.save(DRUMS_PATH, audios["drums"].cpu(), sample_rate)
    torchaudio.save(BASS_PATH, audios["bass"].cpu(), sample_rate)

    separator.separate_to_file(SONG_PATH, DIR_PATH, filename_format="{instrument}.mp3")

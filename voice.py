import torch
from transformers import VitsModel, AutoTokenizer
from scipy.io.wavfile import write


MODEL_NAME = "facebook/mms-tts-eng"


def generate_speech(text, output_path):
    print("Loading TTS model...")

    model = VitsModel.from_pretrained(MODEL_NAME)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    print("TTS model loaded!")

    inputs = tokenizer(
        text,
        return_tensors="pt"
    )

    with torch.no_grad():
        output = model(**inputs).waveform

    waveform = output.squeeze().cpu().numpy()

    write(
        output_path,
        model.config.sampling_rate,
        waveform
    )

    return output_path
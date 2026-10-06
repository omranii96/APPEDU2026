"""Local French TTS (Piper voices through sherpa-onnx) and Whisper transcription for QA."""
import os
import numpy as np
import sherpa_onnx

MODELS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")


def tts(voice="tom"):
    name = {"tom": "fr_FR-tom-medium", "pierre": "fr_FR-upmc-medium"}[voice]
    d = os.path.join(MODELS, f"vits-piper-{name}")
    cfg = sherpa_onnx.OfflineTtsConfig(
        model=sherpa_onnx.OfflineTtsModelConfig(
            vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                model=os.path.join(d, f"{name}.onnx"),
                tokens=os.path.join(d, "tokens.txt"),
                data_dir=os.path.join(d, "espeak-ng-data"),
                noise_scale=0.6,
                noise_scale_w=0.75,
                length_scale=1.0,
            ),
            num_threads=4,
        ),
        max_num_sentences=1,
    )
    return sherpa_onnx.OfflineTts(cfg)


def say(engine, text, sid=0, speed=1.0):
    a = engine.generate(text, sid=sid, speed=speed)
    return np.array(a.samples, dtype=np.float32), a.sample_rate


def asr():
    d = os.path.join(MODELS, "sherpa-onnx-whisper-small")
    return sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=os.path.join(d, "small-encoder.int8.onnx"),
        decoder=os.path.join(d, "small-decoder.int8.onnx"),
        tokens=os.path.join(d, "small-tokens.txt"),
        language="fr",
        task="transcribe",
        num_threads=4,
    )


def transcribe(rec, samples, sr):
    s = rec.create_stream()
    s.accept_waveform(sr, samples)
    rec.decode_stream(s)
    return s.result.text.strip()

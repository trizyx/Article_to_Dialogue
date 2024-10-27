import grpc
import os
import wave
import sys

sys.path.append(os.path.abspath("cueta_repo/voicekitexamples_fold/python/"))
sys.path.append(os.path.abspath("cueta_repo/voicekitexamples_fold/python/tinkoff"))
sys.path.insert(0, "cueta_repo/voicekitexamples_fold/python/tinkoff")
sys.path.append("..")
from voicekitexamples_fold.python.auth import authorization_metadata
from voicekitexamples_fold.python.tinkoff.cloud.tts.v1 import tts_pb2_grpc, tts_pb2

endpoint = os.environ.get("VOICEKIT_ENDPOINT") or "api.tinkoff.ai:443"
api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InIxUGNSUGsvMVo3WG9QSGxIS3d2cmdWUkxnQ1ZFTnByRHZPK1ArODM2NHM9VFRTX1RFQU0ifQ.eyJpc3MiOiJ0ZXN0X2lzc3VlciIsInN1YiI6InRlc3RfdXNlciIsImF1ZCI6InRpbmtvZmYuY2xvdWQudHRzIiwiZXhwIjoxNzMwMDM0Nzc1LjB9.uxrnKrgaCHxlG4DvB7ekslZ9dtSn-eDc2hw82fAJhFM'
sample_rate = 48000


def voice_synth(wav_output_path, prompt_path=None, prompt_text=None):
    if prompt_path is not None:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt = f.read()
    else:
        prompt = prompt_text

    def build_request():
        return tts_pb2.SynthesizeSpeechRequest(
            input=tts_pb2.SynthesisInput(
                ssml=prompt
            ),
            audio_config=tts_pb2.AudioConfig(
                audio_encoding=tts_pb2.LINEAR16,
                sample_rate_hertz=sample_rate,
            ),
        )

    with wave.open(wav_output_path, "wb") as f:
        f.setframerate(sample_rate)
        f.setnchannels(1)
        f.setsampwidth(2)

        stub = tts_pb2_grpc.TextToSpeechStub(grpc.secure_channel(endpoint, grpc.ssl_channel_credentials()))
        request = build_request()
        metadata = [("authorization", f"Bearer {api_key}")]
        responses = stub.StreamingSynthesize(request, metadata=metadata)
        for stream_response in responses:
            f.writeframes(stream_response.audio_chunk)


# ssml_prompt_path = 'ssml_promts/economics_dialod_promt.txt'
# wav_output_path = 'audio_files/economics.wav'
# voice_synth(ssml_prompt_path, wav_output_path)

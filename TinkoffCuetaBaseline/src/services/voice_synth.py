import os
import wave
import sys

import grpc
import pyaudio


from config.config import config


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


sys.path.append(os.path.abspath(f"{BASE_DIR}/voicekit-examples/python/"))
sys.path.append(os.path.abspath(f"{BASE_DIR}/voicekit-examples/python/tinkoff"))
sys.path.insert(0, f"{BASE_DIR}/voicekit-examples/python/tinkoff")
sys.path.append("..")

from src.services.voicekitexamples.python.auth import authorization_metadata
from src.services.voicekitexamples.python.tinkoff.cloud.tts.v1 import tts_pb2_grpc, tts_pb2

api_key = config.api_synth
AUDIO_DIR = os.path.dirname(os.path.abspath(__file__)).replace('services', 'routes/final_file/synthesized.wav')

sample_rate = 48000

def voice_synth(prompt, api_key):
    prompt = insert_prosody_tags(prompt)
    prompt = add_breaks_before_words(prompt)
    prompt = add_breaks_punctuations(prompt)
    prompt = make_kovalev_human_like_faster(prompt)

    endpoint = os.environ.get("VOICEKIT_ENDPOINT") or "api.tinkoff.ai:443"
    sample_rate = 48000
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
    with wave.open(AUDIO_DIR, "wb") as f:
        f.setframerate(sample_rate)
        f.setnchannels(1)
        f.setsampwidth(2)

        stub = tts_pb2_grpc.TextToSpeechStub(grpc.secure_channel(endpoint, grpc.ssl_channel_credentials()))
        request = build_request()
        metadata = [("authorization", f"Bearer {api_key}")]
        responses = stub.StreamingSynthesize(request, metadata=metadata)

        for stream_response in responses:
            f.writeframes(stream_response.audio_chunk)


import re

def add_breaks_before_words(text, words=["объясни", "Помоги", "помоги", "помоги понять", "разъясни", "поясни", "расскажи",
    "объясни это", "помоги разобраться", "расскажи понятнее", "разложи на простые",
    "поможешь понять?", "объясни, что тут", "разберись со мной", "поясни, о чём",
    "расскажи проще", "поможешь объяснить?", "объясни подробнее", "подскажи главное",
    "помоги мне понять", "поясни главное", "разъясни это", "помоги понять смысл",
    "расшифруй", "покажи суть", "объясни значимость", "Объясни", "Помоги", "Помоги понять", "Объясни", "Разъясни", "Поясни", "Расскажи",
    "Объясни это", "Помоги разобраться", "Расскажи понятнее", "Разложи на простые",
    "Поможешь понять?", "Объясни, что тут", "Разберись со мной", "Поясни, о чём",
    "Расскажи проще", "Поможешь объяснить?", "Объясни подробнее", "Подскажи главное",
    "Помоги мне понять", "Поясни главное", "Разъясни это", "Помоги понять смысл",
    "Расшифруй", "Покажи суть", "Объясни значимость", "Привет", " привет", "привет", "Да", "да"], break_tag='<break time="300ms"/>'):
    pattern = r'\b(' + '|'.join(map(re.escape, words)) + r')\b'
    def insert_break(match):
        return f'{break_tag} {match.group(0)}'
    modified_text = re.sub(pattern, insert_break, text, flags=re.IGNORECASE)
    
    return modified_text


def add_breaks_punctuations(text, words=["."], break_tag='<break time="150ms"/>'):
    # Create a pattern that matches the specified punctuation marks
    pattern = r'(' + '|'.join(map(re.escape, words)) + r')'
    def insert_break(match):
        return f'{break_tag} {match.group(0)}'
    
    modified_text = re.sub(pattern, insert_break, text, flags=re.IGNORECASE)
    
    return modified_text


import random

def insert_prosody_tags(text, insert_probability=1):
    def prosody_insertion(match):
        voice_tag = match.group(1)
        content = match.group(2)
        sentences = re.split(r'(?<=[.!?])\s+', content)
        
        for i in range(len(sentences)):
            if random.random() < insert_probability:
                # Split the sentence by spaces but retain existing tags
                words = re.findall(r'<[^>]+>|[^<>\s]+', sentences[i])
                eligible_indices = [j for j, w in enumerate(words) if not re.match(r'<[^>]+>', w)]
                if len(eligible_indices) > 3:
                    num_words = random.randint(1, min(4, len(eligible_indices)))
                    selected_indices = sorted(random.sample(eligible_indices, num_words))
                    for index in selected_indices:
                        words[index] = f'<prosody pitch="102%" rate="75%">{words[index]}</prosody>'
                    sentences[i] = ' '.join(words)
        modified_content = ' '.join(sentences)
        return f'{voice_tag}{modified_content}'
    
    pattern = r'(<voice[^>]*>)(.*?</voice>)'
    modified_text = re.sub(pattern, prosody_insertion, text, flags=re.DOTALL)
    if not re.search(r'<speak>', text, re.IGNORECASE):
        final_ssml = f"<speak>{modified_text}</speak>"
    else:
        final_ssml = modified_text
    
    return final_ssml


import xml.etree.ElementTree as ET

def make_kovalev_human_like_faster(ssml_content):
    tree = ET.ElementTree(ET.fromstring(ssml_content))
    root = tree.getroot()
    
    desired_pitch = "90%"
    desired_rate = "110%"
    
    for voice in root.findall('.//voice'):
        if voice.get('name') == 'kovalev':
            for prosody in voice.findall('.//prosody'):
                prosody.set('pitch', desired_pitch)
                prosody.set('rate', desired_rate)

            for elem in voice.iter():
                if elem.tag not in ['prosody', 'emphasis', 's', 'p']:
                    continue
                if 'prosody' not in elem.tag:

                    parent = elem
                    for child in list(parent):
                        if child.tag == 'prosody':
                            child.set('pitch', desired_pitch)
                            child.set('rate', desired_rate)

            global_prosody = ET.Element('prosody', attrib={'pitch': desired_pitch, 'rate': desired_rate})

            for child in list(voice):
                voice.remove(child)
                global_prosody.append(child)
            voice.append(global_prosody)
    

    for break_tag in root.findall('.//voice[@name="kovalev"]//break'):
        current_time = break_tag.get('time')
        if current_time.endswith('ms'):
            time_ms = int(current_time.replace('ms', ''))
            new_time_ms = max(time_ms - 200, 100)
            break_tag.set('time', f"{new_time_ms}ms")
        elif current_time.endswith('s'):
            time_s = float(current_time.replace('s', ''))
            new_time_s = max(time_s - 0.2, 0.1)
            break_tag.set('time', f"{new_time_s}s")
    return ET.tostring(root, encoding='unicode')


token = api_key
prompt = """<speak>
    <voice name="sveta">
        Дочь: <break time="0.3s"/> Пап, о чем эта статья?
    </voice>
    <voice name="kovalev">
        Отец: <break time="0.5s"/> Эта статья рассказывает о том, как компании в Китае продают свои акции на аукционах, чтобы собрать деньги. Основная мысль в том, что компании заранее ставят цель по доходу, которую хотят получить, и определяют минимальную цену за акцию.
    </voice>
    <voice name="sveta">
        Дочь: <break time="0.3s"/> Почему они ставят цель по доходу заранее?
    </voice>
    <voice name="kovalev">
        Отец: <break time="0.5s"/> Хороший вопрос. Установив такую цель, компания может лучше контролировать процесс продажи. Если они знают, сколько денег хотят получить, это помогает им понимать, сколько акций нужно продать и по какой цене.
    </voice>
    <voice name="sveta">
        Дочь: <break time="0.3s"/> А как работает сам аукцион?
    </voice>
    <voice name="kovalev">
        Отец: <break time="0.5s"/> Всё начинается с того, что компания объявляет минимальную цену, ниже которой она не будет продавать акции. Затем инвесторы делают ставки, называя цены, по которым они готовы покупать акции. Компания выбирает самую высокую цену, при которой ещё удаётся достичь нужного дохода, и продаёт акции по этой цене всем, кто сделал ставки выше или на уровне этой цены.
    </voice>
    <voice name="sveta">
        Дочь: <break time="0.3s"/> Значит, все платят одну и ту же цену?
    </voice>
    <voice name="kovalev">
        Отец: <break time="0.5s"/> Да, это называется «аукцион с единой ценой». Все платят одинаковую цену, даже если они были готовы заплатить больше. Это сделано для того, чтобы участники не боялись переплатить.
    </voice>
    <voice name="sveta">
        Дочь: <break time="0.3s"/> А что, если кто-то ставит ниже минимальной цены?
    </voice>
    <voice name="kovalev">
        Отец: <break time="0.5s"/> Тогда их ставка просто не учитывается. Компания устанавливает минимальную цену, чтобы защитить себя и не продать акции слишком дешево.
    </voice>
    <voice name="sveta">
        Дочь: <break time="0.3s"/> Почему эта система лучше, чем обычный аукцион?
    </voice>
    <voice name="kovalev">
        Отец: <break time="0.5s"/> Потому что так компания получает почти все деньги, которые рассчитывала, даже если некоторые инвесторы пытаются занизить цены. Это также побуждает участников аукциона делать более честные ставки, поскольку они знают, что слишком низкая ставка их исключит.
    </voice>
    <voice name="sveta">
        Дочь: <break time="0.3s"/> Интересно, а как они проверяли, что эта система работает лучше?
    </voice>
    <voice name="kovalev">
        Отец: <break time="0.5s"/> Они проанализировали данные с таких аукционов и сравнили, как часто итоговая цена была близка к той, которую компания хотела получить. Оказалось, что с заранее установленной целью дохода компании обычно получают почти столько, сколько планировали.
    </voice>
    <voice name="sveta">
        Дочь: <break time="0.3s"/> Значит, такая система помогает компании получать больше прибыли?
    </voice>
    <voice name="kovalev">
        Отец: <break time="0.5s"/> Всё верно. Благодаря целям по доходу и единой цене компании почти всегда получают желаемый результат. Так что для них это надёжный способ продать акции.
    </voice>
    <voice name="sveta">
        Дочь: <break time="0.3s"/> Понятно, а почему другие страны так не делают?
    </voice>
    <voice name="kovalev">
        Отец: <break time="0.5s"/> Возможно, из-за сложности реализации такой системы или из-за опасений, что это может запутать инвесторов. Но Китай нашёл способ сделать это эффективно, и результаты пока что положительные.
    </voice>
    <voice name="sveta">
        Дочь: <break time="0.3s"/> Значит, это выгодно для китайских компаний?
    </voice>
    <voice name="kovalev">
        Отец: <break time="0.5s"/> Да, это помогает им контролировать свои продажи акций и собирать нужные средства, избегая резких колебаний цены. Это особенно важно для крупных компаний.
    </voice>
    <voice name="sveta">
        Дочь: <break time="0.3s"/> Спасибо, теперь всё ясно!
    </voice>
    <voice name="kovalev">
        Отец: <break time="0.5s"/> Пожалуйста! Всегда рад помочь разобраться в сложных вещах.
    </voice>
</speak>
"""
# voice_synth(prompt, token)
    
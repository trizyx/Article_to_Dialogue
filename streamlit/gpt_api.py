from openai import OpenAI
from pathlib import Path
from tqdm import tqdm
import os

OPENAI_API_KEY = "sk-WtQcuu7ZV6tXfUOhapb2JzORObV42kRF"
# OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.proxyapi.ru/openai/v1",
)


def check_article(check_promt, article_input_path=None, article_text=None):
    if article_input_path is not None:
        with open(article_input_path, "r", encoding='utf-8') as file:
            file_content = file.read()  # Считываем текст файла
    else:
        file_content = article_text

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,
        messages=[
            {"role": "user",
             "content": f"{check_promt}\n\nСодержимое файла:\n{file_content}"}
        ]
    )

    return response.choices[0].message.content


def create_dialog_gtp04mini(dialog_promt, dialog_input_path=None, dialog_text=None):
    if dialog_input_path is not None:
        with open(dialog_input_path, "r", encoding='utf-8') as file:
            file_content = file.read()  # Считываем текст файла
    else:
        file_content = dialog_text

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.6,
        messages=[
            {"role": "user",
             "content": f"{dialog_promt}\n\nСодержимое файла:\n{file_content}"}
        ]
    )

    return response.choices[0].message.content


def create_ssml_gpt04mini(ssml_promt, ssml_input_path=None, ssml_text=None):
    if ssml_input_path is not None:
        with open(ssml_input_path, "r", encoding='utf-8') as file:
            file_content = file.read()
    else:
        file_content = ssml_text
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user",
             "content": f"{ssml_promt}\n\nСодержимое файла:\n{file_content}"}
        ]
    )
    return response.choices[0].message.content


check_promt = """
Тебе дан текст, ты должен проверить, является ли он какой-то статьей, новостью или публикацией. Если он осмысленный, выведи "OK", если это бессвязный текст или содержит что-то крайне неприличное, выведи, "<причина c небольшим пояснением>"
"""

dialog_promt = """Преобразуй данную статью в формате диалога между отцом и дочерью-подростком. Отец должен объяснять суть текста простыми, понятными словами, избегая сложных терминов, а также отвечать на вопросы дочери, которые помогают раскрыть и уточнить основные идеи. Начинай с краткого объяснения темы, а затем используй диалог, чтобы глубже раскрыть содержание, акцентируя внимание на ключевых моментах. Диалог должен быть сбалансированным: дочери — вопросы, отцу — ответы, без потери важной информации.

Пример структуры диалога:
Дочь: "Пап, о чем эта статья?"
Отец: "Эта статья говорит о ..."
Дочь: "А что это за задача?"
Отец: "...".

Другой пример структуры диалога:
Дочь: "Пап, привет, я прочитала статью о ..., но ничего не поняла, объясни, пожалуйста"
Отец: "Эта статья говорит о ..."
Дочь: "Ага, а что такое ..."
Отец: "...".

Задача: Сделать объяснения короткими, но исчерпывающими. Заверши диалог, подытожив главные выводы статьи. Диалоги не должны копировать пример. Не выводи ничего кроме диалога"
"""
ssml_promt = """Прочитай загруженный txt файл и создай идеальный SSML-код, который точно озвучит диалог между дочкой-подростком ('sveta') и её отцом ('kovalev'), объясняющим ей какую-то тему. Добавь паузы, замедление или ускорение речи, изменения тембра, чтобы передать соответствующие эмоции и интонации.
<speak>
    <break time="600ms"/>
<voice name="sveta">
        <p><s><prosody pitch="97%" rate="99%">А как это работает? </s>В чем суть этого аукциона?</prosody></p>
    </voice>
    <break time="600ms"/>
 <voice name="kovalev">
        <p><s><prosody pitch="90%" rate="95%">Во время аукциона участники предлагают свои цены за акции.</prosody></s> <prosody pitch="93%" rate="96%">Главное, что компании устанавливают <emphasis level="moderate">резервную цену</emphasis> – это минимальная цена, по которой они готовы продать акции.</prosody></p> <s>Они пытаются собрать сумму, которую объявили, путем продажи акций по этой цене или выше.</s>
    </voice>
    <break time="500ms"/>
</speak>
<s> и <p> - задают предложение и абзац в тексте соответственно:
Для <s> пауза составляет 200 ms - ОБЯЗАТЕЛЬНО ДОБАВЛЯЙ В КОНЦЕ ПРЕДЛОЖЕНИЙ
Для <p> пауза составляет 400 ms - добавляй перед знаком "--" и между абзацами длинной реплики 
<break time="500ms"/> - добавляй после окончания реплик персонажа, всегда немного разные от 400 до 700.
ты можешь изменять параметры только в соответствии с примером
rate от 90% до 100% для kovalev
rate от 95% до 100% для sveta

pitch от 90% до 100% для kovalev
pitch от 95% до 100% для sveta
в разных репликах немного разные, чтобы звучало естественно
<emphasis level="moderate"></emphasis> используй для выделения ключевых фраз в некоторых предложениях

Выведи только сгенерированный SSML-код без xml в начале."""

# for article in list(Path("dialogs/").glob("*.txt")):
#     # article = Path(article)
#     # print(f"Processing article: {article.stem}")
#     # article_input_path = f"articles\\{article.stem}.txt"
#     # dialod_output_path = f"dialogs\\{article.stem}_dialod.txt"
#     # print(f"Dialogue path: {dialod_output_path}")
#     # dialog_response = create_dialog_gtp04mini(dialog_promt, article_input_path)
#     # with open(dialod_output_path, 'w', encoding='utf-8') as f:
#     #     f.write(dialog_response)
#     print(article)
#     ssml_output_path = f"ssml_promts\\{article.stem}_promt.txt"
#     print(f"Ssml path: {ssml_output_path}")
#     dialod_output_path = article
#     ssml_response = create_ssml_gtp04mini(ssml_promt, dialod_output_path)
#     with open(ssml_output_path, 'w', encoding='utf-8') as f:
#         f.write(ssml_response)
#
#     print("\n\n")

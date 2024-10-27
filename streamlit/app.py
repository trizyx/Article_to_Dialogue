import os
import sqlite3
import tempfile

import streamlit as st
import validators
from newspaper.article import ArticleException

from gpt_api import create_dialog_gtp04mini, create_ssml_gpt04mini, dialog_promt, ssml_promt, check_article, check_promt
from llama import create_dialog_llama
from parser import pdf_to_txt, url_to_txt
from voice_api import voice_synth

# Инициализация базы данных для хранения истории
conn = sqlite3.connect('dialog_history.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS history 
             (id INTEGER PRIMARY KEY, source TEXT, dialog TEXT, audio_path TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()


# Функция для сохранения истории диалогов
def save_to_history(source, dialog, audio_path):
    c.execute("INSERT INTO history (source, dialog, audio_path) VALUES (?, ?, ?)", (source, dialog, audio_path))
    conn.commit()


api_choice = st.sidebar.select_slider(
    "Выберите модель для генерации диалога:",
    options=["ChatGPT API", "LLaMA Local"]
)

# Описание проекта
st.title("👨‍👧 Преобразование текста в диалог с синтезом речи")
st.write(
    "Этот сервис предназначен для автоматического преобразования новостных и обзорных текстов в "
    "диалоговый формат между отцом и дочерью. Тексты сложных тем преобразуются в понятный диалог, "
    "который затем озвучивается, чтобы подростки могли лучше понимать важные темы. "
    "Вы можете загрузить текстовый файл, PDF, или указать URL-адрес статьи."
)

# Секция для загрузки файла или ввода URL
file = st.file_uploader("📄 Загрузите файл (.txt или .pdf)", type=["txt", "pdf"])
url = st.text_input("🌐 Или введите URL статьи")

# Размещаем кнопки в ряд
col1, col2 = st.columns(2)

# Кнопка генерации диалога
with col1:
    generate_button = st.button("Создать диалог")

# Кнопка для просмотра истории
with col2:
    history_button = st.button("Показать историю диалогов")

# Логика кнопки генерации диалога с прогресс-баром и аудио
if generate_button:
    if not file and not url:
        st.warning("Пожалуйста, загрузите файл или введите URL для обработки.")

    if file or url:
        st.info("⏳ Идет проверка возможности генерации диалога...")

        with tempfile.TemporaryDirectory() as temp_dir:
            text_path = None

            # Этап 1: Обработка файла или URL
            if file:
                if file.type == "application/pdf":
                    pdf_path = os.path.join(temp_dir, file.name)
                    with open(pdf_path, "wb") as f:
                        f.write(file.read())
                    text_path = os.path.join(temp_dir, "uploaded_text.txt")
                    pdf_to_txt(pdf_path, text_path)
                elif file.type == "text/plain":
                    text_path = os.path.join(temp_dir, file.name)
                    with open(text_path, "w", encoding='utf-8') as f:
                        f.write(file.read().decode('utf-8'))
            elif url:
                if validators.url(url):
                    text_path = os.path.join(temp_dir, "url_text.txt")
                    try:
                        url_to_txt(url, text_path)
                    except ArticleException as e:
                        st.error(f"Ошибка загрузки статьи: {e}. Проверьте корректность URL.")
                        text_path = None  # Пропустить обработку, если URL недоступен

            # Чтение текста и проверка через check_article
            if text_path:
                with open(text_path, "r", encoding='utf-8') as f:
                    article_text = f.read()

                # Запрос к check_article
                check_result = check_article(check_promt, article_text=article_text)

                if check_result.startswith("OK"):
                    # Продолжаем генерацию диалога, если "OK"
                    st.info("✅ Текст проверен, начинается генерация диалога.")
                    progress = st.progress(0.25)

                    # Этап 2: Генерация диалога
                    if api_choice == "ChatGPT API":
                        dialog_text = create_dialog_gtp04mini(dialog_promt, dialog_input_path=text_path)
                        ssml_text = create_ssml_gpt04mini(ssml_promt, ssml_text=dialog_text)
                        st.success("✅ Диалог успешно создан!")
                        st.subheader("Сгенерированный диалог")
                        st.write(dialog_text)
                    else:
                        server_url = "https://2f3d-35-198-228-94.ngrok-free.app/"  # Укажите URL вашего сервера LLaMA
                        response = create_dialog_llama(server_url, article_text)
                        print(response)
                        dialog_text = "sorry, no dialogue"
                        ssml_text = response['dialogue']
                        st.success("✅ Диалог успешно создан!")

                    # Этап 3: Синтез речи с обработкой ошибок
                    audio_path = os.path.join(temp_dir, "output_audio.wav")
                    try:
                        st.text("🎙️ Синтез речи")
                        progress.progress(0.75)
                        voice_synth(wav_output_path=audio_path, prompt_text=ssml_text)
                        st.text("✅ Завершение обработки")
                        progress.progress(1.0)

                        # Воспроизведение аудио на сайте
                        st.subheader("Прослушать диалог")
                        st.audio(audio_path, format="audio/wav")

                        # Кнопка для скачивания аудиофайла
                        with open(audio_path, "rb") as f:
                            st.download_button(label="📥 Скачать аудио", data=f, file_name="dialog_audio.wav",
                                               mime="audio/wav")

                    except Exception as e:
                        # Если синтез не удается, выводим сообщение об ошибке
                        st.error(f"Ошибка синтеза речи: {e}")
                        st.warning("Диалог отображен, но синтез речи недоступен.")

                    # Сохранение диалога в историю
                    source = file.name if file else url
                    save_to_history(source, dialog_text, audio_path if os.path.exists(audio_path) else None)

                else:
                    # Если check_article возвращает "NO", не генерируем диалог и выводим сообщение
                    st.error(f"Этот текст нельзя представить в виде диалога: {check_result}")

# Логика кнопки истории
if history_button:
    c.execute("SELECT * FROM history ORDER BY timestamp DESC")
    rows = c.fetchall()
    for row in rows:
        st.write(f"Источник: {row[1]}, Дата: {row[4]}")
        st.write("Диалог:")
        st.write(row[2])
        audio_path = row[3]
        if audio_path and os.path.exists(audio_path):
            # Воспроизведение и скачивание аудио из истории
            st.subheader("Прослушать диалог")
            st.audio(audio_path, format="audio/wav")
            with open(audio_path, "rb") as f:
                st.download_button(label="📥 Скачать аудио", data=f, file_name="dialog_audio.wav", mime="audio/wav")
        st.divider()

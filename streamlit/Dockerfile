FROM python:3.10

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PATH "/app/scripts:${PATH}"

RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y \
    gcc \
    portaudio19-dev \
    python3-pyaudio \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt


# RUN pip3 install setuptools wheel packaging
# RUN pip3 install torch --index-url https://download.pytorch.org/whl/cpu
# RUN pip3 install xformers
# RUN pip3 install unsloth --no-cache-dir
RUN pip3 install -r requirements.txt
RUN pip3 install newspaper3k

COPY . /app

CMD [ "streamlit", "run", "app.py" ]
FROM debian

RUN  apt update
RUN  apt install -y \
     sudo \
     python3 \
     python3-pip \
     python3-venv

COPY app/requirements.txt /app/requirements.txt
COPY .env /.env

RUN  python3 -m venv /opt/venv
ENV  PATH="/opt/venv/bin:$PATH"
RUN  pip install -Ur app/requirements.txt

COPY app /app

EXPOSE 5000

CMD  [ "/bin/bash" ]


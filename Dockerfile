FROM debian

RUN  apt update && apt upgrade -y
RUN  apt install -y \
     sudo \
     python3 \
     python3-pip \
     python3-venv

COPY app /app
COPY .env /.env

RUN  python3 -m venv /opt/venv
ENV  PATH="/opt/venv/bin:$PATH"
RUN  pip install -Ur app/requirements.txt

EXPOSE 5000

CMD  [ "/bin/bash" ]


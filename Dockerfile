FROM python:3.10.12

ARG BASIC_AUTH_USERNAME_ARG
ARG BASIC_AUTH_PASSWORD_ARG

ENV BASIC_AUTH_USERNAME=${BASIC_AUTH_USERNAME_ARG}
ENV BASIC_AUTH_PASSWORD=${BASIC_AUTH_PASSWORD_ARG}

COPY ./requirements.txt /usr/requirements.txt

WORKDIR /usr

RUN pip3 install -r requirements.txt

COPY ./project /usr/project
COPY ./models /usr/models

ENTRYPOINT ["python3"]

CMD ["project/main.py"]

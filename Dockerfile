FROM python:3.10-alpine3.15
LABEL maintainer=jon@kosli.com

ARG APP_DIR
ARG APP_PORT
ARG APP_USER

ENV APP_DIR=/${APP_DIR}
ENV APP_PORT=${APP_PORT}
ENV PYTHONPATH=${APP_DIR}/server
ENV TERM=xterm-256color

RUN apk --update --upgrade add bash tini \
 && apk --no-cache upgrade musl \
 && apk update \
 && adduser -D ${APP_USER}

COPY server/requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

WORKDIR ${APP_DIR}
COPY . .
RUN chown -R ${APP_USER} ${APP_DIR}
USER ${APP_USER}

ENTRYPOINT [ "/sbin/tini", "-g", "--" ]
CMD ${APP_DIR}/server/gunicorn.sh

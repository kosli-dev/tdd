FROM python:3.11.0-alpine3.16
LABEL maintainer=jon@kosli.com

ARG XY_CONTAINER_ROOT_DIR \
    XY_CONTAINER_PORT \
    XY_USER_NAME \
    XY_WORKER_COUNT \
    XY_GIT_COMMIT_SHA

RUN apk --update --upgrade add bash jq tini \
 && apk update \
 && adduser -D -g "" ${XY_USER_NAME}

USER ${XY_USER_NAME}

COPY source/requirements.txt /tmp/requirements.txt

RUN pip3 install --requirement /tmp/requirements.txt --user

ENV XY_CONTAINER_ROOT_DIR=${XY_CONTAINER_ROOT_DIR} \
    XY_CONTAINER_PORT=${XY_CONTAINER_PORT} \
    XY_WORKER_COUNT=${XY_WORKER_COUNT} \
    XY_GIT_COMMIT_SHA=${XY_GIT_COMMIT_SHA} \
    PYTHONPATH=${XY_CONTAINER_ROOT_DIR}/source \
    PYTHONPYCACHEPREFIX=/tmp/py_caches \
    TERM=xterm-256color \
    PATH="/home/xy/.local/bin:${PATH}"

WORKDIR ${XY_CONTAINER_ROOT_DIR}
COPY . .

EXPOSE "${XY_CONTAINER_PORT}"

ENTRYPOINT [ "/sbin/tini", "-g", "--" ]

CMD ${XY_CONTAINER_ROOT_DIR}/source/gunicorn.sh

FROM python:3.11.0-alpine3.16
LABEL maintainer=jon@kosli.com

COPY server/requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

ARG XY_CONTAINER_ROOT_DIR \
    XY_CONTAINER_PORT \
    XY_USER_NAME \
    XY_WORKER_COUNT \
    XY_GIT_COMMIT_SHA

ENV XY_CONTAINER_ROOT_DIR=${XY_CONTAINER_ROOT_DIR} \
    XY_CONTAINER_PORT=${XY_CONTAINER_PORT} \
    XY_WORKER_COUNT=${XY_WORKER_COUNT} \
    XY_GIT_COMMIT_SHA=${XY_GIT_COMMIT_SHA} \
    PYTHONPATH=${XY_CONTAINER_ROOT_DIR}/server \
    PYTHONPYCACHEPREFIX=/tmp/py_caches \
    TERM=xterm-256color

WORKDIR ${XY_CONTAINER_ROOT_DIR}
COPY . .
RUN apk --update --upgrade add bash jq tini && \
    apk update && \
    adduser -D -g "" ${XY_USER_NAME} && \
    chown -R ${XY_USER_NAME} ${XY_CONTAINER_ROOT_DIR}

USER ${XY_USER_NAME}
EXPOSE "${XY_CONTAINER_PORT}"
ENTRYPOINT [ "/sbin/tini", "-g", "--" ]
CMD ${XY_CONTAINER_ROOT_DIR}/server/gunicorn.sh

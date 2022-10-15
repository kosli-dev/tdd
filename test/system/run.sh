#!/bin/bash -Eeu

pytest \
    --workers auto \
    --no-cov \
    --capture=no \
    --color=yes \
    --ignore=test/unit \
    --pythonwarnings=error \
    --tb=short \
    --quiet \
    --random-order-bucket=global \
        ${XY_DIR}/test/system/

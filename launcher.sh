#!/usr/bin/env bash
# created by xxy1991

CFG_URI='https://cfg.ori.fyi'
PIP_MIRROR='https://mirrors.aliyun.com/pypi/simple'

# check_py3()
check_py3() {
    apt-get -yqq update

    # PYTHON_VER=$(python3 -V 2>&1 | awk '{print $2}')
    # if ! [[ $PYTHON_VER == 3* ]]; then
    #     apt-get install -yqq --no-install-recommends python3
    # fi
    # PIP_VER=$(pip3 -V 2>&1 | awk '{print $2}')
    # if ! [[ $PIP_VER == 9* ]]; then
    #     apt-get install -yqq --no-install-recommends python3-pip
    # fi
    apt-get install -yqq --no-install-recommends pipx

    # apt-get install -yqq wget ca-certificates curl lsb-release pax python3-venv
    apt-get install -yqq wget ca-certificates curl lsb-release pax
    # python3 -m pip install -q -i "$PIP_MIRROR" --upgrade pip
    # pip3 install -q -i "$PIP_MIRROR" sortedcontainers requests invoke jinja2
}

# exec_script(str agrs)
exec_script() {
    # python3 -m easyops.netboot "$@"
    easyops "$@"
}

check_py3

# pip3 install --no-deps --ignore-installed easyops-1.2.0-py3-none-any.whl
pipx install ./easyops-1.2.0-py3-none-any.whl
export PATH="/root/.local/bin:$PATH"

exec_script "$@"

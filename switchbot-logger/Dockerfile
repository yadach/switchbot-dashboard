FROM python:3.9.2

# Install Bluetooth modules
RUN apt update -y \
  && apt install -y bluez libglib2.0-dev

# Install python setup modules
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
  && python3 get-pip.py \
  && python3 -m pip install --no-cache-dir --upgrade pip \
  && python3 -m pip install --no-cache-dir setuptools \
  && python3 -m pip install --no-cache-dir poetry \
  && rm -rf ~/.cache/pip ./get-pip.py

# Install python library
COPY . /opt/app/
WORKDIR /opt/app
RUN poetry config virtualenvs.in-project true \
  && poetry install \
  && setcap 'cap_net_raw,cap_net_admin+eip' /opt/app/.venv/lib/python3.9/site-packages/bluepy/bluepy-helper

# Default CMD
ENTRYPOINT ["poetry", "run", "python", "switchbot_logger/bin/scan_and_log.py"]
CMD ["--mac"]

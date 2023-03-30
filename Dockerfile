FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt ./


RUN set -ex \
    && sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y gcc libmariadb-dev-compat --no-install-recommends apt-utils \
    && apt install --reinstall build-essential -y \
    && pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /root/.cache/pip


EXPOSE 1891

CMD ["supervisord", "-c", "supervisord.conf"]

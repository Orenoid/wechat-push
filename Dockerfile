FROM python:3.6-alpine as test

WORKDIR /home/project-name

COPY app app
COPY migrations migrations
COPY tests tests
COPY  .coveragerc uwsgi.ini config.py manage.py requirements.txt  ./

# 修改apk镜像源, 3.6版本会有个bug，具体原因不详，换3.9就可以构建了
RUN echo https://mirrors.aliyun.com/alpine/v3.9/main > /etc/apk/repositories; \
    echo https://mirrors.aliyun.com/alpine/v3.9/community >> /etc/apk/repositories

RUN set -e; \
    apk add --no-cache --virtual .build-deps \
    gcc \
    libc-dev \
    linux-headers \
    ; \
    pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/; \
    apk del .build-deps;

ENTRYPOINT [ "pytest" ]

FROM test as prod

VOLUME [ "/home/project-name/logs" ]

EXPOSE 6000
ARG DEV_DATABASE_URL
RUN python manage.py db upgrade
ENTRYPOINT ["uwsgi"]
CMD ["-i", "uwsgi.ini"]
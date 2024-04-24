flask + flask_restx api + chatgpt3.5

使用 flask + uwsgi + supervisord + docker 部署 NGINX不赘述

要想启动成功需要注意supervisord.conf 添加

```angular2html
[supervisord]
nodaemon=true
```

docker命令

```angular2html
build
docker build -t chat .

run
docker run -it -d -p 1891:1891 -v /www/server/chatgpt-sys/:/app/ --name chat-v2 chat  supervisord -c supervisord.conf
run 时可添加命令
--sysctl net.core.somaxconn=6096  --restart=always
```

直接杀死supervisor

supervisorctl shutdown

啊啊啊

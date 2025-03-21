# !/bin/bash
echo -e "\n033[31m 重启脚本开始执行 \033[0m"

ps -ef|grep dsx_uwsgi.ini | grep -v grep

sleep 0.5

echo -e "\n033[31m 重启uwsgi \033[0m"
ps -ef|grep dsx_uwsgi.ini | grep -v grep|awk '{print $2}'|xargs kill -9

sleep 0.5

echo -e '\n033[31m 重启uwsgi \033[0m]]'
/envs/customer/bin/uwsgi --ini dsx_uwsgi.ini & >/dev/null

sleep 1

ps -ef|grep dsx_uwsgi.ini | grep -v grep
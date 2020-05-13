#!/bin/bash
server="gevent_server.py"
# server="tornado_server.py"
case "$@" in
start)
  $(python ${server} >>server.logs 2>&1 &)
  ;;
stop)
  kill -9 $(ps aux | grep python | grep -v grep | awk '{print $1}' | xargs)
  ;;

restart)
  kill -9 $(ps aux | grep python | grep -v grep | awk '{print $1}' | xargs)
  sleep 1
  $(python ${server} >>server.logs 2>&1 &)
  ;;
*)
  echo 'unknown arguments args(start|stop|restart)'
  exit 1
  ;;
esac

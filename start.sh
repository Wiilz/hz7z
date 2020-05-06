#!/bin/bash
case "$@" in
start)
  $(python server.py >>tornado.logs 2>&1 &)
  ;;
stop)
  kill -9 $(ps aux | grep python | grep -v grep | awk '{print $1}' | xargs)
  ;;

restart)
  kill -9 $(ps aux | grep python | grep -v grep | awk '{print $1}' | xargs)
  sleep 1
  $(python server.py >>tornado.logs 2>&1 &)
  ;;
*)
  echo 'unknown arguments args(start|stop|restart)'
  exit 1
  ;;
esac

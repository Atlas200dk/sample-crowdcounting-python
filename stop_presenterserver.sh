#!/bin/sh

i=$(ps -ef | grep presenter | grep crowd_counting | grep -o '[0-9]\+' | head -n1)
if [ -z "$i" ] ;then
echo presenter sever not in process!
fi
kill -9 $i 2>/dev/null
echo presenter sever stop success!

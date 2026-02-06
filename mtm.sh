#!/bin/bash

# Optionen
# -d <YYYY-MM-DD>
# -t <hh:mm>
# -x +/- n in sek + save to db
# -s show data

DB_FILE_NAME='./muehle.db'
if [ ! -e "$DB_FILE_NAME" ]; then
  sqlite3 "$DB_FILE_NAME" < muehle.sql
fi

# Vorbelegung der Werte für das Datum und die Uhrzeit
datenow=`date +%Y-%m-%d`

tmenow=`date +%H:%M:%S`


# mehrere mögliche Trenner zwischen YYYY MM DD werden durch '-' ersetzt
function parsedate {
  echo $1 | sed 's/[\.,]/-/g'
};

# wir brauchen auch parsetime - Trenner ist ein Doppelpunkt und Sekunden werden angefuegt
# SQL verlangt hh:mm:ss
function parsetime {
  pt=`echo $1 | sed 's/[\.,-]/:/g'`
  if [ ${#pt} -lt 8 ]; then
    echo $pt:00
  else
    echo $pt
  fi
};

# Schalter zum Abspeichern der Werte / zum Anzeigen der Werte
saveit=0
showit=0
eraseit=0
while getopts d:t:x:se: opt
do
   case $opt in
       d) datenow=`parsedate $OPTARG` ;;
       t) tmenow=`parsetime $OPTARG` ;;
       x) gang=$OPTARG
          saveit=1 ;;
       s) showit=1 ;;
       e) eraseit=$OPTARG ;;
   esac
done

if [ $saveit -eq 1 ]; then  
  sqlite3 muehle.db "INSERT OR IGNORE INTO muehle (date, time, timedelta) \
                   VALUES (\"$datenow\",\"$tmenow\", \"$gang\");"
fi

if [ $showit -eq 1 ]; then
  sqlite3 muehle.db "SELECT * FROM muehle;"
fi

if [ $eraseit -ne 0 ]; then
  sqlite3 muehle.db "DELETE FROM muehle WHERE id=$eraseit;"
fi


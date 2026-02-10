#!/bin/bash

# Optionen
# -d <YYYY-MM-DD>
# -t <hh:mm>
# -x +/- n in sek + save to db
# -s show data
# -e erase line number n

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

# eingegebenes Komma wird zum Punkt
function parsegang {
  echo `echo $1 | sed 's/[,_]/\./g'`
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
       x) gang=`parsegang $OPTARG`
          saveit=1 ;;
       s) showit=1 ;;
       e) eraseit=$OPTARG ;;
   esac
done

if [ $saveit -eq 1 ]; then  
  sqlite3 muehle.db "INSERT OR IGNORE INTO muehle (date, time, timedelta) \
                   VALUES (\"$datenow\",\"$tmenow\", \"$gang\");"
fi

# Ausgabe formatiert, Floatwerte auf eine Stelle nach dem Komma begrenzt,
# alles Rechtsbuendig und mit ein bissl Abstand.
if [ $showit -eq 1 ]; then
  sqlite3  muehle.db "WITH gesamt AS (SELECT printf ('%5s', ROW_NUMBER() OVER()) AS num,\
                                          printf ('%15s', date) AS tag,\
                                          printf ('%12s', time) AS lt,\
                                          printf ('%8.1f', timedelta) AS lt_delta\
                                      FROM muehle) \
                                      SELECT num, tag, lt, lt_delta,\
                                          printf ('%8.1f', lt_delta - LAG(lt_delta) OVER()) AS zum_vortag\
                                      FROM gesamt;"
fi

#TODO: das muss angepasst werden, wir arbeiten nicht nach der id sondern nach der ROW_NUMBER()"
if [ $eraseit -ne 0 ]; then
  sqlite3 muehle.db "WITH nummer AS (SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS rowNum FROM muehle) \
                     DELETE FROM muehle WHERE id IN (SELECT id FROM nummer WHERE rowNum=$eraseit);"    
fi


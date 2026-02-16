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
while getopts :s:d:t:x:e: opt
do
   case $opt in
       d) datenow=`parsedate $OPTARG` ;;
       t) tmenow=`parsetime $OPTARG` ;;
       x) gang=`parsegang $OPTARG`
          saveit=1 ;;
       s) showit=$OPTARG ;;
       e) eraseit=$OPTARG ;;
       :) showit=1 ;;
   esac
done

if [ $saveit -eq 1 ]; then  
  sqlite3 muehle.db "INSERT OR IGNORE INTO muehle (date, time, timedelta) \
                   VALUES (\"$datenow\",\"$tmenow\", \"$gang\");"
fi

# TODO: berechnung der seitennzahl lines / 15 geht noch nicht. anzeige der 
# letzten 15 zeilen geht.
# angedacht ist: -s <seite> 
#  ...FROM gesamt ORDER BY num ASC LIMIT 15 OFFSET $lines - 15 * $OPTARG
# ...oder so:


# Ausgabe formatiert, Floatwerte auf eine Stelle nach dem Komma begrenzt,
# alles Rechtsbuendig und mit ein bissl Abstand. Wir berechnen die Anzahl 
# der Tabellenseiten, da nur immer max 15 Seiten der gesamten Tabelle ausgegeben
# werden. Die Speicherseitenmagie weiter unten kommt daher weil z.B. 1,8 Tabellen-
# seiten zu 1 Tabellenseite gerundet werden. 
if [ $showit -gt 0 ]; then
  # wir berechnen wie viel Seiten es a 15 Zeilen gibt 
  lines=`sqlite3 muehle.db "SELECT COUNT(*) FROM muehle;"`
  speicherseiten=$(( $lines / 15 ))
  modulo=`echo "$lines % 15" | bc`
  if [ $modulo > 0 ]; then
    speicherseiten=`expr $speicherseiten + 1`
  fi
  if [ $showit -gt $speicherseiten ]; then
    echo "ungültige Seitenzahl"
    exit 1
  fi

  sqlite3 muehle.db ".mode box" "WITH gesamt AS (SELECT printf ('%5s', ROW_NUMBER() OVER(ORDER BY date, time)) AS num,\
                                          printf ('%15s', date) AS tag,\
                                          printf ('%12s', time) AS lt,\
                                          printf ('%8.1f', timedelta) AS lt_delta\
                                      FROM muehle) \
                                      SELECT num, tag, lt, lt_delta,\
                                          printf ('%8.1f', lt_delta - LAG(lt_delta) OVER()) AS zum_vortag\
                                      FROM gesamt ORDER BY num ASC LIMIT 15 OFFSET $lines - 15 * $showit;"
  echo "Tabellenseiten: $speicherseiten" 
  echo "mtm: usage: -s <seite>"
fi

# wir loeschen Eintraege korrekt nach ROW_NUMBER
if [ $eraseit -ne 0 ]; then
  sqlite3 muehle.db "WITH nummer AS (SELECT id, ROW_NUMBER() OVER (ORDER BY date, time) AS rowNum FROM muehle) \
                     DELETE FROM muehle WHERE id IN (SELECT id FROM nummer WHERE rowNum=$eraseit);"    
fi


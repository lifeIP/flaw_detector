

DATETIME_START=$(date "+%d/%m/%y    %H:%M:%S")
echo ">>>> Запуск программы в $DATETIME_START" > ./terminal.log

./.venv/bin/python ./main.py &>> "./terminal.log"

DATETIME_END=$(date "+%d/%m/%y    %H:%M:%S")
echo ">>>> Закрытие программы в $DATETIME_END" >> ./terminal.log

DATETIME=$(date "+%dd%mm%yy%Hh%Mm%Ss")
ZIPNAME="./logs/$DATETIME.zip"
zip -r $ZIPNAME terminal.log
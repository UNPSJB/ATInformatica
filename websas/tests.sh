while true
do
    python manage.py test --settings=websas.test-settings
    if [ $? -ne 0 ]; 
    then
        paplay /usr/share/sounds/freedesktop/stereo/bell.oga 2> /dev/null
    else
        paplay /usr/share/sounds/freedesktop/stereo/complete.oga 2> /dev/null
    fi
    inotifywait -e modify ./**/*.py
done

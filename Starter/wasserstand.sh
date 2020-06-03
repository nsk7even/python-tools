cd `dirname "$(readlink -f "$0")"`
python3 -u ../scrape.py | zenity --text-info --width=1000 --height=300 --font=courier --title=Wasserstand

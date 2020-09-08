cd `dirname "$(readlink -f "$0")"`
python3 -u ../scrape.py | zenity --text-info --width=1100 --height=400 --font=courier --title=Wasserstand


rules=pk_rules
romanization=pk_romanization
classes=pk_classes
sound_changer=../../../sound_changer.py

python3 $sound_changer ../pkt_lex_stressed $rules -c $classes -o pk_changed

# python3 $sound_changer pk_changed $romanization -o pk_romanized
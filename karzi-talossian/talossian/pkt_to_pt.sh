
rules=pt_rules
romanization=pt_romanization
classes=pt_classes
sound_changer=../../../sound_changer.py

python3 $sound_changer ../pkt_lex_stressed $rules -c $classes -o pt_changed

python3 $sound_changer pt_changed $romanization -o pt_romanized
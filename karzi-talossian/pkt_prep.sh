
deromanization_rules=pkt_deromanization
sound_changer=../../sound_changer.py
stresser=pkt_stress_applier.py

echo 'Processing full lexicon...'

python3 $sound_changer "Proto-Karzi-Talossian Dictionary - lex.csv" $deromanization_rules -o pkt_lex
python3 $stresser pkt_lex

echo "done"

echo 'Processing nouns...'

python3 $sound_changer "Proto-Karzi-Talossian Dictionary - nouns.csv" $deromanization_rules -o pkt_nouns
python3 $stresser pkt_nouns

echo "done"

echo 'Processing verbs...'

python3 $sound_changer "Proto-Karzi-Talossian Dictionary - verbs.csv" $deromanization_rules -o pkt_verbs
python3 $stresser pkt_verbs

echo "done"


import re

from typing import List
from itertools import chain


def get_syllables(word: str) -> List[str]:
    syllables = []
    while word:
        # search for syllables from the end of the word because it's easier
        # otherwise disambiguating final n/m from initial n/m would
        # make things more complicated
        syllable = re.search("([^aeɛiou]|ts|tʃ)[aeɛiou][nm]?$", word)
        # calling group() gets the actual text matched
        syllables.append(syllable.group())
        word = word[:syllable.start()]
    
    # because the syllables were added in reverse order, just switch them around here
    return syllables.reverse()


strong_onsets = ['ts', 'tʃ']
nasals = ['n', 'm']

def is_strong(syllable: str) -> bool:
    return any(syllable.startswith(sound) for sound in strong_onsets)\
            or any(syllable.endswith(sound) for sound in nasals)

def stress_syallble(syllable: str) -> str:
    # insert an apostrophe before the vowel
    return re.sub(r'([aeɛiou])', r"'\1", syllable)

def secondary_stress(syllables: List[str]) -> List[str]:
    # this function assumes the list starts just after primary stress
    second_to_last_stressed = False
    last_stressed = True
    
    ret = []
    for syllable in syllables:
        if last_stressed:
            # can't have 2 consecutive stressed syllables
            current_stressed = False
        elif not second_to_last_stressed:
            # no more than 2 consecutive unstressed syllables may occur
            current_stressed = True
        elif is_strong(syllable):
            current_stressed = True
        else:
            current_stressed = False

        if current_stressed:
            syllable = apply_stress(syllable)
        
        ret.append(syllable)

        second_to_last_stressed = last_stressed
        last_stressed = current_stressed
    
    return ret


def apply_stress(word: str) ->str:
    syllables = get_syllables(word)
    for syllable in syllables:
        if is_strong(syllable):
            # primary stress lands on the first "strong" syllable, if there is one
            primary_stress = stress_syallble(syllable)

            i = syllables.index(syllable)
            before = syllables[:i]
            after = syllables[i+1:]
            break
    else:
        # otherwise it's just on the first syllable
        primary_stress = stress_syallble(syllables[0])
        before = []
        after = syllables[1:]
    
    # the secondary stress rules are symmetric
    before = secondary_stress(before.reverse()).reverse()
    after = secondary_stress(after)

    # rejoin all of the syllables to return 1 string
    return list(chain(before, [primary_stress], after)).join()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('lex_file', action = "store", type = argparse.FileType("r", encoding = "utf-8"))
    parser.add_argument('-o', '--out', dest = 'out_file', action = "store", type = argparse.FileType("w", encoding = "utf-8"), default = None)

    args = parser.parse_args(['karzi-talossian/pkt_lex'])

    if not args.out_file:
        args.out_file = open(args.lex_file.name + "_stressed", 'w')
    
    for line in args.lex_file:
        word = line.strip()
        args.out_file.write(apply_stress(word))


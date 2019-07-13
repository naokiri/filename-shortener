"""
    No special care of other processes touching the filesystem. Only for local personal use.

    スキャンした本のNAS引越しでファイル名も暗号化されるようなドライブに引越したところ、ファイル名長さ制限にひっかかったのをアドホックに修正するために作成
"""
from functools import reduce
from pathlib import Path
import re
from typing import Set, Callable

from secret import more_removing_words


def ask_y_n(msg: str) -> bool:
    while True:
        ans = input(msg + "y/n? ").lower()
        if ans == "y":
            return True
        elif ans == "n":
            return False
        else:
            print("respond with 'y' or 'n'")


space_pattern = re.compile(r'\s')


def replace_spaces(name: str) -> str:
    return space_pattern.sub(" ", name)


def replace_wide_brackets(name: str) -> str:
    return (name.replace("（", "(")
            .replace("）", ")")
            .replace("［", "[")
            .replace("］", "]")
            .replace("｛", "{")
            .replace("｝", "}")
            )


remove_paren_in_bracket_pattern = re.compile(r'\[(\S*)\s\(.*\)\]')


def remove_paren_in_bracket(name: str) -> str:
    return remove_paren_appended_pattern.sub("[\g<1>]", name)


remove_paren_appended_pattern = re.compile(r'(\S*)\s?[([]\S*[)\]](\.\S{3,4})')


def remove_paren_appended(name: str) -> str:
    return remove_paren_appended_pattern.sub("\g<1>\g<2>", name)


remove_words = {
    "電子透かし済"
}


def remove_words_func(more_banned_words: Set[str] = None) -> Callable[[str], str]:
    if more_banned_words:
        all_removing_words = remove_words.union(more_banned_words)
    else:
        all_removing_words = remove_words
    pattern_string = "[([{【〈《](" + '|'.join(list(all_removing_words)) + ")[)\\]}】〉》]"
    remove_words_pattern = re.compile(pattern_string)
    return lambda name: remove_words_pattern.sub("", name).strip()


def strip(name: str) -> str:
    return name.strip()


def apply_all(name: str) -> str:
    funs = [replace_spaces, replace_wide_brackets, remove_paren_appended, remove_paren_in_bracket,
            remove_words_func(more_removing_words), strip]

    return reduce(lambda x, f: f(x), funs, name)


def main():
    answer = ask_y_n("Shorten names under [{}] ?".format(Path.cwd().name))
    if not answer:
        return

    for entry in Path.cwd().glob("**/*"):
        if entry.is_file():
            old_name = entry.name
            new_name = apply_all(old_name)
            if len(new_name.encode('utf-8')) > 255:
                print("{} is longer than 255byte?".format(new_name))
            entry.rename(new_name)


if __name__ == "__main__":
    main()

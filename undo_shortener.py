from pathlib import Path

from filename_shortener import ask_y_n
import re


def main():
    logpath = Path.cwd().joinpath("rename_result.txt")
    if not logpath.exists():
        print("No logfile found under {}".format(Path.cwd().as_uri()))
        exit()

    ans = ask_y_n("Undo here? {} ".format(Path.cwd().as_uri()))
    if not ans:
        exit()

    pattern = re.compile(r'\t(.*) --> (.*)')

    with logpath.open(mode="r") as logfile:
        line = logfile.readline().strip()
        while line:
            # print(line)
            if line.startswith("Success") or line.startswith("Warning"):
                match_result = pattern.search(line)
                if match_result:
                    current = match_result.group(2)
                    original = match_result.group(1)
                    print("Undo {} to {}".format(current, original))
                    current_file = Path(current)
                    if not current_file.exists():
                        print("Error doesn't exist {}".format(current))
                    else:
                        current_file.rename(original)
                else:
                    print("Error processing {}".format(line))
            line = logfile.readline().strip()
            #line = None


if __name__ == "__main__":
    main()

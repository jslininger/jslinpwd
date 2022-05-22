import subprocess
import sys
import secrets
import string
import random
from fuzzywuzzy import fuzz

def init() -> dict:
    gpgout = subprocess.Popen(["gpg", "-d", "/home/jslin/Music/x.txt.gpg"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = gpgout.communicate()
    if stderr is not None:
        print(stderr)
        return None
    result = {}
    lines = stdout.decode("utf-8").split("\n")
    for i in range(2, len(lines)): # gpg outputs two extra lines of info on the top that is irrelevant
        words = lines[i].rstrip().split(";")
        if len(words) < 2:
            break
        site, pwd = words
        result[site.lower()] = pwd
    return result

def generatepwd() -> str:
    alphabet = string.ascii_letters + string.digits + "!#?$@"
    size = 15 #random.randrange(15, 30)
    while True:
        pwd = ''.join(secrets.choice(alphabet) for i in range(size))
        if (any(c.islower() for c in pwd)
                and any(c.isupper() for c in pwd)
                and sum(c.isdigit() for c in pwd) >= 3
                and sum(c in "!#?$@" for c in pwd) >= 1):
            return pwd
    #return ''.join(secrets.choice(alphabet) for i in range(size))

def recreategpg(pwds):
    # write pwds to x.txt, one per line, format "site;pwd\n", no extra newlines on top, bottom can have extra
    # encrypt using gpg
    # delete x.txt
    tempfile = open("/home/jslin/Music/x.txt", 'w')
    for site, pwd in sorted(pwds.items()):
        tempfile.write(site + ";" + pwd + "\n")
    tempfile.close()
    subprocess.call(["rm", "/home/jslin/Music/x.txt.gpg"])
    subprocess.call(["gpg", "-r", "jslin", "--encrypt", "/home/jslin/Music/x.txt"])
    subprocess.call(["rm", "/home/jslin/Music/x.txt"])
    return

def run():
    # if len(sys.argv) > 3:
    #     print("Error: please provide a valid number of commands")
    #     return
    pwds = init()
    if pwds is None:
        print("The above errors prevented gpg from running properly\n")
        return
    if len(sys.argv) == 1:
        for site, pwd in pwds.items():
            print(site.lower() + "; " + pwd)
        return
    code = sys.argv[1].lower()
    if code == "-r":
        try:
            pwds.pop(sys.argv[2].lower())
            recreategpg(pwds)
        except KeyError:
            print("Error: input does not exist in file")
    elif code == "-d":
        # site = sys.argv[2].lower()
        for i in range(2, len(sys.argv)):
            site = sys.argv[i].lower()
            try:    
                print(site + ": " + pwds[site])
            except IndexError:
                print("Error: not enough arguments for decrypt")
                return
            except KeyError:
                # print("Error: input does not exist in file")
                ratio = 0
                closest = ""
                for realsite in pwds:
                    r = fuzz.partial_ratio(site, realsite)
                    if r > ratio:
                        ratio = r
                        closest = realsite
                print(closest + ": " + pwds[closest])
        return
    elif code == "-e":
        try:
            pwds[sys.argv[2].lower()] = generatepwd()
        except IndexError:
            print("Error: not enough arguments for encrypt")
            return
        recreategpg(pwds)
        print(pwds[sys.argv[2].lower()])
        return
    else:
        print("Error: invalid command:", code)
        return


if __name__ == '__main__':
    run()
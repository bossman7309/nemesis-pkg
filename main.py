from sys import argv, exit
from requests import get
from subprocess import check_output 
from os.path import isfile
from os.path import isdir 
from os import mkdir 
from os import chdir
from shutil import copy
from requests.exceptions import MissingSchema, ConnectionError

ANSI_CODES = [
    "\x1b[31m",
    "\x1b[32m",
    "\x1b[33m",
    "\x1b[34m",
    "\x1b[0m"
]

mainpage = """nemesis-pkg:
============
usage:- nemesis-pkg {operation} {args}
============
operations:-
i: installs a package.. nemesis-pkg i {pkg1} {pkg2}
r: removes a package... nemesis-pkg r {pkg1} {pkg2}
lsi: lists system installed packages.. nemesis-pkg lsi {pkg}
lri: lists packages in repository... nemesis-pkg lri {pkg}
ug: upgrade packages... nemesis-pkg ug
ud: update the package database... nemesis-pkg ud
h: shows info on operations and usage.. nemesis-pkg h
v: show nemesis-pkg version"""

operations = ["i" , "r" , "lsi" , "lri" , "ug" , "ud" , "h" , "v"]
path_pkglist = "/etc/nemesis-pkg/PKGLIST"
path_ipkglist = "/etc/nemesis-pkg/IPKGLIST"
current_user = check_output(["whoami"])
pkglist_src = "https://raw.githubusercontent.com/Nemesis-OS/packages/main/PKGLIST"
cmd_args = []

def update_database():
    if isfile(path_pkglist) == True:
        local_PKGLIST = True
        pass
    else:
        local_PKGLIST = False
        print(f"{ANSI_CODES[2]}warning{ANSI_CODES[4]}: database file is not found on path so downloading it")
        print(f"{ANSI_CODES[3]}info{ANSI_CODES[4]}: creating database file")
        if isdir("/etc/nemesis-pkg") == False:
            mkdir("/etc/nemesis-pkg")
        pass

    print(f"{ANSI_CODES[3]}info{ANSI_CODES[4]}: downloading database..")
    try:
        new_PKGLIST = get(pkglist_src)
    except ConnectionError:
        print(f"{ANSI_CODES[0]}error{ANSI_CODES[4]}: file failed to download due to connectivity issue")
        exit(1)
    except MissingSchemasingSchema:
        print(f"{ANSI_CODES[0]}error{ANSI_CODES[4]}: file failed to download due to some exceptions")
        exit(1)

    if new_PKGLIST != None and local_PKGLIST == False:
        print(f"{ANSI_CODES[3]}info{ANSI_CODES[4]}: creating PKGLIST..")
        local_PKGLIST = open(path_pkglist, 'w')
        local_PKGLIST.write(str(new_PKGLIST.content.decode("utf-8")))
        local_PKGLIST.close()
    else:
        local_PKGLIST = open(path_pkglist, 'r+')
        if local_PKGLIST.read() != str(new_PKGLIST.content.decode("utf-8")):
            print(f"{ANSI_CODES[3]}info{ANSI_CODES[4]}: replacing PKGLIST with the new one")
            local_PKGLIST.seek(0)
            local_PKGLIST.write(str(new_PKGLIST.content.decode("utf-8")))
            local_PKGLIST.truncate()
            local_PKGLIST.close()
            pass
        else:
            print(f"{ANSI_CODES[3]}info{ANSI_CODES[4]}: you had the latest database")

    print(f"{ANSI_CODES[1]}sucess{ANSI_CODES[4]}:- the databases were updated succesfully")

def list_packages_from_repo(query: list[str]):
    print(f"{ANSI_CODES[3]}info:{ANSI_CODES[4]} syncing the databases to get latest software")
    update_database()
    PKGLIST = open(path_pkglist , "r+")
    PKGLIST_AVAILABLE = PKGLIST.read()
    PKGLIST_AVAILABLE = PKGLIST_AVAILABLE.splitlines()
    if query == []:
        print(f"{ANSI_CODES[2]}warning{ANSI_CODES[4]}: no query specified so printing the list of available packages")
        for i in PKGLIST_AVAILABLE:
            print(i)
    else:
        for i in range(0 , len(query)):
            pkgs_matching = []
            qry = list(query[i])
            for j in PKGLIST_AVAILABLE:
                if j.find(qry[i]) == -1:
                    continue
                else:
                    pkgs_matching.append(j)
                    continue
                    
            if pkgs_matching == []:
                print(f"{ANSI_CODES[0]}error{ANSI_CODES[4]}: no package was relevant to {query[i]}")
            else:
                print(f"{ANSI_CODES[2]}note{ANSI_CODES[4]}: there were some packages matching to {query[i]}..")
                for matching_pkgs in pkgs_matching:
                    print(matching_pkgs)

            continue
                   
if __name__ == "__main__":
    if current_user != b'root\n':
        print(f"{ANSI_CODES[0]}error{ANSI_CODES[4]}: user is not root")
        exit(1)
    else:
        pass
    
    try:
        if argv[1] == "h":
            print(mainpage)
        elif argv[1] == "v":
            print("nemesis-pkg 0.1(Build 2363)")
        elif argv[1] == "ud":
            update_database()
        elif argv[1] == "lri":
            for i in range(2, len(argv)):
                cmd_args.append(argv[i])
            list_packages_from_repo(cmd_args)
        else:
            print(f"{ANSI_CODES[0]}error{ANSI_CODES[4]}: invalid operation")
    except IndexError:
        print(f"{ANSI_CODES[0]}error{ANSI_CODES[4]}: no operation specified")

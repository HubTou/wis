# Installation
Depending on if you want only this tool, the full set of PNU tools, or PNU plus a selection of additional third-parties tools, use one of these commands:

pip install [pnu-wis](https://pypi.org/project/pnu-wis/)
<br>
pip install [PNU](https://pypi.org/project/PNU/)
<br>
pip install [pytnix](https://pypi.org/project/pytnix/)

:warning: This tool is not yet included in the PNU and pytnix distributions

# WIS(1)

## NAME
WIS - Bulk WhoIs Search

## SYNOPSIS
**wis**    
\[-1|--first\]
\[-c|--case\]
\[-d|--dirname DIR\]
\[-e|--exclude FILE\]
\[-f|--filename FILE\]
\[-i|--inet4\]
\[-I|--inet6\]
\[-r|--range\]
\[--debug\]
\[--help|-?\]
\[--version\]
\[--\]
KEYWORD
\[...\]

## DESCRIPTION
The **wis** utility searches for keyword(s) within WhoIs bulk database(s).

Beside saving multiple WHOIS queries, using pre-downloaded WhoIs bulk databases enables to do plain text searches on all the WhoIs records.

You can either select one specific database (in plain text or gzipped format) using the *-f|--filename FILE* option, or/and a directory containing all your databases using the *-d|--dirname DIR* option.

Use the *-c|--case* option to make your searches case sensitive.

Use the *-e|--exclude FILE* option to provide a one-excluded-case-insensitive-keyword-per-line to filter out matching records.

You'll then obtain a list of records matching at least one of your keywords, and not matching any of the excluded keywords.

If you use the *-1|--first* option, you'll instead only obtain the first line of each matching record (whether it is an inetnum, inet6num, organisatio, aut-num, role, route or mntner record).

If you use the *-i|--inet4* and/or *-I|--inet6* option(s), you'll instead obtain only matching inetnum or inet6num records reformatted as pipe-separated-values of networks:
```
starting IP address|ending IP Address|netname|descr|org|country
```
If you add the *-r|--range* option to the last ones, you'll instead obtain only matching inetnum or inet6num records reformatted as pipe-separated-values of hosts:
```
IP address|type|subnet|netname|descr|org|country
```
Where type is either "Network" for the first address in a subnet, "Broadcast" for the last address in a subnet or "IP address" for the rest.

### OPTIONS
Options | Use
------- | ---
-1\|--first|Show only the first line of each matching record
-c\|--case|Make searches case sensitive
-d\|--dirname DIR|Use databases from the DIR directory name
-e\|--exclude FILE|Exclude words from the FILE file name
-f\|--filename FILE|Use database from the FILE file name
-i\|--inet4|Show only reformatted inetnum records
-I\|--inet6|Show only reformatted inet6num records
-r\|--range|Show expanded inet(6)num ranges
--debug|Enable debug mode
--help\|-?|Print usage and a short help message and exit
--version|Print version and exit
--|Options processing terminator

## ENVIRONMENT
The WIS_DEBUG environment variable can also be set to any value to enable debug mode.

## FILES
The **wis** utility uses WhoIs bulk databases downloaded from the main [Regional Internet Registries (RIR)](https://www.iana.org/numbers).

The provided "fetch-db.sh" script can be used for doing this.

Be sure to read their respective terms of use before!

## EXIT STATUS
The **wis** utility exits 0 on success, and >0 if an error occurs.

## EXAMPLES
Assuming that you have installed the available bulk WhoIs databases (in gzipped format) in a directory named "db", and that you made a one-excluded-keyword-per-line file named "excluded.txt", use the following commands:

* to extract full WhoIs information about matching blocks:
```Shell
wis -d db -e excluded.txt keyword1 keyword2 keyword3
```

* to extract only the first line of WhoIs information about matching blocks:
```Shell
wis -d db -e excluded.txt -1 keyword1 keyword2 keyword3
```

* to extract an IPv4 network summary about matching blocks:
```Shell
wis -d db -e excluded.txt -i keyword1 keyword2 keyword3
```

* to extract an IPv4 host summary about matching blocks:
```Shell
wis -d db -e excluded.txt -ir keyword1 keyword2 keyword3
```

## SEE ALSO
[whois(1)](https://www.freebsd.org/cgi/man.cgi?query=whois)

## STANDARDS
The **wis** utility is not a standard UNIX command.

This implementation tries to follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for [Python](https://www.python.org/) code.

## PORTABILITY
To be tested under Windows.

## HISTORY
This implementation was made for the [PNU project](https://github.com/HubTou/PNU).

The initial name of the command was "AS Search", but the resulting short form seemed problematic... So I went for a **wis**er name :-)

## LICENSE
It is available under the [3-clause BSD license](https://opensource.org/licenses/BSD-3-Clause).

## AUTHORS
[Hubert Tournier](https://github.com/HubTou)

## CAVEAT
[LACNIC](https://www.lacnic.net/) (Latin America and Caribbean NIC) does not provide a very useful bulk WhoIs database...


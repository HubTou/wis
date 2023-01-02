#!/usr/bin/env python
""" Identify what has changed between 2 LACNIC bulk WHOIS databases """

import gzip
import re
import sys

################################################################################
def process_block(block, database):
    """Process a text block and eventually print it"""
    subnet = ""
    status = ""
    city = ""
    country = ""
    created = ""
    changed = ""

    if block[0].startswith("inetnum:"):
        subnet = re.sub(r"^inetnum:[ 	]*", "", block[0])
    elif block[0].startswith("inet6num:"):
        subnet = re.sub(r"^inet6num:[ 	]*", "", block[0])
    else:
        # We don't care about other types of records
        return

    for line in block[1:]:
        if line.startswith("status:"):
           status = re.sub(r"^status:[    ]*", "", line)
        elif line.startswith("city:"):
           city = re.sub(r"^city:[    ]*", "", line)
        elif line.startswith("country:"):
           country = re.sub(r"^country:[    ]*", "", line)
        elif line.startswith("created:"):
           created = re.sub(r"^created:[    ]*", "", line)
        elif line.startswith("changed:"):
           changed = re.sub(r"^changed:[    ]*", "", line)

    if subnet not in database:
        database[subnet] = {"status": status, "city": city, "country": country, "created": created, "changed": changed}
    elif database[subnet]["status"] == status \
    and database[subnet]["city"] == city \
    and database[subnet]["country"] == country \
    and database[subnet]["created"] == created \
    and database[subnet]["changed"] == changed:
        print("WARNING: Duplicate record!", database[subnet], file=sys.stderr)
        pass
    else:
        print("WARNING: Duplicate key {}".format(subnet), file=sys.stderr)
        if database[subnet]["changed"] >= changed:
            print("  Old:", database[subnet], " selected", file=sys.stderr)
            print("  New: {{'status': '{}', 'city': '{}', 'country': '{}', 'created': '{}', 'changed': '{}'}}".format(status, city, country, created, changed), file=sys.stderr)
        else:
            print("  Old:", database[subnet], file=sys.stderr)
            print("  New: {{'status': '{}', 'city': '{}', 'country': '{}', 'created': '{}', 'changed': '{}'}} selected".format(status, city, country, created, changed), file=sys.stderr)
            database[subnet]["status"] = status
            database[subnet]["city"] = city
            database[subnet]["country"] = country
            database[subnet]["created"] = created
            database[subnet]["changed"] = changed


################################################################################
def load_database(filename):
    """Process a plain text or gzipped file"""
    database = {}

    if filename.endswith(".gz"):
        file = gzip.open(filename, "rt", encoding="iso-8859-1", errors="ignore")
    else:
        file = open(filename, "rt", encoding="iso-8859-1", errors="ignore")

    block = []
    line = file.readline()
    while line:
        if line.strip() == "":
            if block:
                process_block(block, database)
                block = []
        else:
            block.append(line.strip())

        line = file.readline()

    if block:
        process_block(block, database)

    file.close()

    return database


################################################################################
def main():
    """The program's main entry point"""
    old_db = {}
    new_db = {}

    # Load databases
    if len(sys.argv) == 2:
        print("\nLoading '{}':".format(sys.argv[1]), file=sys.stderr)
        old_db = load_database(sys.argv[1])
        print("{} records".format(len(old_db)), file=sys.stderr)
    elif len(sys.argv) == 3:
        print("\nLoading '{}':".format(sys.argv[1]), file=sys.stderr)
        old_db = load_database(sys.argv[1])
        print("{} records".format(len(old_db)), file=sys.stderr)

        print("\nLoading '{}':".format(sys.argv[2]), file=sys.stderr)
        new_db = load_database(sys.argv[2])
        print("{} records".format(len(new_db)), file=sys.stderr)
    else:
        print("CRITICAL: Expecting 1 or 2 arguments, the old database name and the new one", file=sys.stderr)
        sys.exit(1)

    print("\nProcessing...", file=sys.stderr)
    if len(new_db) == 0:
        for key, value in old_db.items():
            print("=|{}|{}|{}|{}|{}|{}".format(key, value["status"], value["city"], value["country"], value["created"], value["changed"]))

    else:
        for key, value in old_db.items():
            if key not in new_db.keys():
                # deleted
                print("-|{}|{}|{}|{}|{}|{}".format(key, value["status"], value["city"], value["country"], value["created"], value["changed"]))
            elif value["changed"] == new_db[key]["changed"]:
                # same
                #print("=|{}|{}|{}|{}|{}|{}".format(key, value["status"], value["city"], value["country"], value["created"], value["changed"]))
                pass
            else:
                # modified
                print(">|{}|{}|{}|{}|{}|{}".format(key, value["status"], value["city"], value["country"], value["created"], value["changed"]))

        for key, value in new_db.items():
            if key not in old_db.keys():
                # added
                print("+|{}|{}|{}|{}|{}|{}".format(key, value["status"], value["city"], value["country"], value["created"], value["changed"]))

    sys.exit(0)


if __name__ == "__main__":
    main()

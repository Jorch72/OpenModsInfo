import os
import collections
import json
import datetime
import pytz
from feedgen.feed import FeedGenerator

FeedEntry = collections.namedtuple("FeedEntry", ["file", "mod", "version", "bundle"])

def scan_files(dir):
    result = collections.defaultdict(dict)

    for entry in os.listdir(dir):
        full_path = os.path.abspath(os.path.join(dir, entry))
        if os.path.isfile(full_path):
            for entry in parse_file(full_path):
                result[entry.bundle][entry.mod] = entry

    return result

def parse_file(path):
    print("Reading data from " + path)
    with open(path, "r") as input:
        contents = json.load(input)

        for mod in contents['mods']:
            yield FeedEntry(mod['name'], mod['id'], mod['version'], mod['date'])

if __name__ == "__main__":
    data = scan_files("../feeds/")

    fg = FeedGenerator()
    fg.id('https://openmods.info/updates')
    fg.title('OpenMods updates')
    fg.author( {'name':'OpenMods'})
    fg.language('en')
    fg.link({'href' : 'https://openmods.info'})
    fg.link({'href' : 'https://openmods.info/atom.xml', 'rel' : 'self', 'type' : 'application/atom+xml'})
    fg.link({'href' : 'https://openmods.info/rss.xml', 'rel' : 'self', 'type' : 'application/rss+xml'})
    fg.description('OpenMods update feed')
    fg.lastBuildDate(datetime.datetime.utcnow().replace(tzinfo = pytz.utc))

    for (bundle, mods) in sorted(data.items(), key = lambda (bundle, mods): bundle, reverse = True):
        bundle_date = datetime.datetime.strptime(bundle, "%Y-%m-%d").replace(tzinfo = pytz.utc)
        ue = fg.add_entry()
        ue.id("openmods.info:update:" + bundle)
        ue.title("New OpenMods update: " + bundle)
        ue.description(", ".join(sorted([e.mod + " " + e.version for e in mods.values()])), True)
        ue.link({'href' : 'https://openmods.info'})
        ue.published(bundle_date)
        ue.updated(bundle_date)

        for (mod_id, mod_data) in mods.items():
            fe = fg.add_entry()
            fe.id("openmods.info:update:" + bundle + ":" + mod_id)
            fe.title("New file: " + mod_data.file)
            fe.published(bundle_date)
            ue.updated(bundle_date)
            fe.link({'href' : "https://openmods.info/downloads/" + mod_data.file})

    fg.atom_file('../openmods.info/atom.xml')
    fg.rss_file('../openmods.info/rss.xml')


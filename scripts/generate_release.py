from mako.template import Template
import os
import os.path as path
import sys
import collections
import re
import hashlib
import datetime
import codecs

MC_VERSION = "1.7.10"

FILE_RE = re.compile("^(.+?)-(.+?)-(.+).jar$")

ReleaseFile = collections.namedtuple("ReleaseFile", ["name", "path", "version", "size", "md5", "sha256", "date"])

def hash_file(p, *gens):
    hashes = map(lambda x: x(), gens)
    size = 0
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(4096), ""):
            for hash in hashes: hash.update(chunk)
            size += len(chunk)
    return (size, map(lambda hash: hash.hexdigest(), hashes))

def process_file(p, name, dir):
    m = FILE_RE.match(name)
    assert m, "Can't parse file " + name
    mod = m.group(1)
    mc_version = m.group(2)
    assert mc_version == MC_VERSION, "File " + name + " is for invalid MC version. Expected " + MC_VERSION
    version = m.group(3)
    (size, (md5_hash, sha256_hash)) = hash_file(p, hashlib.md5, hashlib.sha256)

    date = datetime.datetime.strptime(dir, "%Y-%m-%d")

    return (mod, ReleaseFile(name, p, version, size, md5_hash, sha256_hash, date))

def load_files(dirs):
    mod_files = dict()
    for dir in dirs:
        dir_name = path.basename(path.dirname(dir))
        assert dir_name, "Path " + dir + " is not valid"
        print("Processing " + dir)
        for content in os.listdir(dir):
            p = dir + content
            if path.isfile(p):
                print("Processing " + p)
                (mod, file_info) = process_file(p, content, dir_name)
                assert mod not in mod_files, "Duplicated mod " + p
                mod_files[mod] = file_info
            else:
                print("Warn: non-file " + content + " in dir " + dir)

    return mod_files

def generate_page(dirs):
    files = load_files(dirs)

    template = Template(filename='index.template', input_encoding='utf-8')

    with codecs.open("../openmods.info/index.html", "w", "utf-8", "replace") as output:
        output.write(template.render_unicode(files = files, timestamp = datetime.datetime.now().isoformat()))

if __name__ == "__main__":
    generate_page(sys.argv[1:])

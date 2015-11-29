#!/bin/python

from mako.template import Template
import os
import os.path as path
import yaml
import codecs
import datetime
from collections import OrderedDict

def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)
    return yaml.load(stream, OrderedLoader)

def generate_for_mod(name):
    template = Template(filename='changelog.template')

    with codecs.open("../changelogs/%s.yaml" % name, "r", "utf-8") as input:
        changelog = ordered_load(input)

    with codecs.open("../openmods.info/changelog-%s.html" % name.lower(), "w", "utf-8", "replace") as output:
        output.write(template.render_unicode(versions = changelog, timestamp = datetime.datetime.now().isoformat(), name = name))

def generate():
    for p in os.listdir("../changelogs/"):
        p = os.path.join("../changelogs/", p)
        if path.isfile(p):
            base_name = os.path.basename(p)
            (name, ext) =  os.path.splitext(base_name)
            if ext == '.yaml':
                print "Processing " + p + " for mod " + name
                generate_for_mod(name)

if __name__ == "__main__":
    generate()
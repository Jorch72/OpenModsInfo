#!/bin/python

from mako.template import Template
import yaml
import markdown
import codecs
import datetime

def generate():
    template = Template(filename='faq.template')

    markdowner = markdown.Markdown(output_format = "html5")
    
    with codecs.open("faq.yaml", "r", "utf-8") as input:
        data = yaml.load(input)
    
    for category_data in data:
        for question_data in category_data['questions']:
            question_data['question'] = question_data['question'].strip()
            question_data['answer'] = markdowner.convert(question_data['answer'])
    
    with codecs.open("../openmods.info/faq.html", "w", "utf-8", "replace") as output:
        output.write(template.render_unicode(categories = data, timestamp = datetime.datetime.now().isoformat()))
        
if __name__ == "__main__":
    generate()

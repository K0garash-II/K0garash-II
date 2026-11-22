#!/usr/bin/env python3
"""Create assets/stack.svg with genuine skillicons.dev icons (one-time download).

Run from the profile directory: python3 generate_stack.py
Requires only Python 3 standard library. The generated SVG is fully self-contained.
"""
import re
import urllib.request
from pathlib import Path
import xml.etree.ElementTree as ET

SVG='http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)
url='https://skillicons.dev/icons?i=go,postgres,docker,git,linux,kafka&theme=dark'
req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (github-profile-svg-builder)'})
try:
    with urllib.request.urlopen(req, timeout=25) as response:
        body=response.read()
    original=ET.fromstring(body)
except Exception as exc:
    raise SystemExit(f'Unable to download Skill Icons (stack.svg was not changed): {exc}')
if original.tag.rsplit('}',1)[-1].lower()!='svg':
    raise SystemExit('Skill Icons did not return a valid SVG (stack.svg was not changed).')

def number(value):
    m=re.search(r'[-+]?(?:\d*\.)?\d+',value or '')
    return float(m.group(0)) if m else None
vb=[float(n) for n in re.split(r'[ ,]+',original.get('viewBox','').strip()) if n]
if len(vb)==4:
    aspect=vb[2]/vb[3]
else:
    w=number(original.get('width'))
    h=number(original.get('height'))
    if not w or not h:
        raise SystemExit('Skill Icons image is missing dimensions; stack.svg was not changed.')
    aspect=w/h
height=48
width=height*aspect
if width>820 or width<=0:
    raise SystemExit('Unexpected Skill Icons dimensions; stack.svg was not changed.')
original.set('x',f'{(900-width)/2:.2f}')
original.set('y','49')
original.set('width',f'{width:.2f}')
original.set('height',str(height))

root=ET.Element(f'{{{SVG}}}svg',{
    'width':'900','height':'110','viewBox':'0 0 900 110',
    'role':'img','aria-label':'Stack: Go, PostgreSQL, Docker, Git, Linux, Kafka',
})
ET.SubElement(root,f'{{{SVG}}}rect',{
    'x':'1','y':'1','width':'898','height':'108','rx':'16','fill':'#15191F','stroke':'#30363D','stroke-width':'2',
})
ET.SubElement(root,f'{{{SVG}}}rect',{
    'x':'431','y':'14','width':'38','height':'3','rx':'1.5','fill':'#8B0000',
})
label=ET.SubElement(root,f'{{{SVG}}}text',{
    'x':'450','y':'36','text-anchor':'middle','fill':'#B34B55',
    'font-family':'JetBrains Mono, SFMono-Regular, Consolas, Liberation Mono, monospace',
    'font-size':'13','font-weight':'700','letter-spacing':'1.0'
})
label.text='STACK'
root.append(original)
path=Path(__file__).resolve().parent/'assets'/'stack.svg'
path.parent.mkdir(parents=True,exist_ok=True)
ET.ElementTree(root).write(path,encoding='utf-8',xml_declaration=True)
print(f'Updated {path} with original Skill Icons.')

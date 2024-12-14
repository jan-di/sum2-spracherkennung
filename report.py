"""
Reporting
"""

from jinja2 import Environment, FileSystemLoader, select_autoescape
from lib import (
    load_audio_json,
)

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)

audio = load_audio_json()

template = env.get_template("report.html.j2")

content = template.render(audio=audio)

with open("report.html", "w", encoding="utf8") as f:
    f.write(content)

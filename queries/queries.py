from jinja2 import Template
from pathlib import Path

base_path = Path(__file__).parent


def openLocal(path):
    return open((base_path / path).resolve()).read()


class Queries:
    """
    Load queries templates and makes them easily accessible
    """
    get_face_encodings = Template(openLocal('./get_face_encodings.sql.jinja'))
    find_closest_match = Template(openLocal('find_closest_match.sql.jinja'))
    unknown_faces = Template(openLocal('./select_unknown_faces.jinja'))
    encoding_columns = ["TERM_{} ".format(i) for i in range(128)]
    save_face = Template("""
    INSERT INTO faces 
    (file_id, locations, {{ encoding_columns | join(',') }})
    VALUES (%s, %s, {% for i in range(127) %} %s, {% endfor %} %s)
    """).render(encoding_columns=encoding_columns)

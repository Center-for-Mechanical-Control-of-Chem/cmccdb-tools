
import io
import base64
import McUtils.Jupyter as interactive
from PIL import Image

from .image_prep import load_image

__reload_hook__ = ['.image_prep']

__all__ = [
    'find_notebook_images',
    'display_image'
]

def find_notebook_images(nb:interactive.NotebookReader=None, header_pattern=None):
    if nb is None:
        nb = interactive.NotebookReader.active_notebook()
    md_cells = nb.cell_list().find_cells_by_type('markdown')
    image_cells = md_cells.find_cells_with_attachments('image/*')
    if header_pattern is not None:
        image_cells = image_cells.find_cells_by_header(header_pattern)
    images = {}
    for cell in image_cells:
        for k,v in cell.attachments.items():
            if k.startswith('image/'):
                image_string = v.attrs['src']
                if image_string.startswith("data:"):
                    header_len = len("data:")
                    image_string = image_string[header_len:]
                header = cell.cell_header
                img = load_image(image_string)
                if header is None or len(header) == 0: header = cell
                images[header] = img
    return images

def prep_image_data_url(image:Image, format='png'):
    buff = io.BytesIO()
    image.save(buff, format=format)
    return f'data:image/{format};base64,' + base64.b64encode(buff.getvalue()).decode("utf-8")
def display_image(image:Image):
    return interactive.JHTML.Image(src=prep_image_data_url(image))


import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML

# allow overriding template directory via env var (useful for tests)
TEMPLATE_DIR = os.getenv("TEMPLATE_DIR", "templates")

# configure Jinja environment once
_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "xml"]),
)


def render_pdf(template_id: str, data: dict) -> bytes:
    """Render the given template with data and return a PDF as bytes.

    The template is looked up under ``{TEMPLATE_DIR}/{template_id}.html``.
    An :class:`jinja2.TemplateNotFound` error will propagate if the file
    doesn't exist.
    """
    # ensure we append extension if not provided
    name = template_id if template_id.endswith(".html") else f"{template_id}.html"
    template = _env.get_template(name)
    html = template.render(**data)
    # WeasyPrint accepts HTML string and returns bytes from write_pdf()
    pdf = HTML(string=html).write_pdf()
    return pdf

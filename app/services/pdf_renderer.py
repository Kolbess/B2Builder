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


def prepare_assets_css(assets: dict) -> str:
    """Return a block of CSS that embeds fonts declared in ``assets``.

    ``assets`` is expected to be a dict with an optional ``fonts`` key mapping
    font-family names to base64-encoded font data (woff2).  The returned CSS
    can be injected into a template's `<style>` block.
    """
    css_lines = []
    fonts = assets.get("fonts") or {}
    for family, b64 in fonts.items():
        # assume woff2 for simplicity
        css_lines.append(
            "@font-face {font-family: '%s'; src: url(data:font/woff2;base64,%s) format('woff2');}"
            % (family, b64)
        )
    return "\n".join(css_lines)



def render_pdf(template_id: str, data: dict) -> bytes:
    """Render the given template with data and return a PDF as bytes.

    The template is looked up under ``{TEMPLATE_DIR}/{template_id}.html``.
    An :class:`jinja2.TemplateNotFound` error will propagate if the file
    doesn't exist.

    The ``data`` dict may include an ``assets`` sub-dictionary containing
    base64 logos and/or fonts; ``assets_css`` will be generated and passed to
    the template automatically.
    """
    # optionally handle assets
    if isinstance(data, dict) and "assets" in data:
        assets = data.get("assets") or {}
        # inject computed css and make assets available in context
        data = dict(data)
        data["assets_css"] = prepare_assets_css(assets)
    # ensure we append extension if not provided
    name = template_id if template_id.endswith(".html") else f"{template_id}.html"
    template = _env.get_template(name)
    html = template.render(**data)
    # WeasyPrint accepts HTML string and returns bytes from write_pdf()
    pdf = HTML(string=html).write_pdf()
    return pdf

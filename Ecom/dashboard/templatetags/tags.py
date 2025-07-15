from django import template

register = template.Library()

@register.filter
def format_description(description):
    """
    Custom template filter to format product descriptions.
    Converts newlines to <br> tags for HTML rendering.
    """
    if description:
        lines = description.split('\n')
        html = '<ul>'
        for line in lines:
            if line.strip():
                html += f"<li>{line}</li>"
        html += '</ul>'
        return html
    return ''
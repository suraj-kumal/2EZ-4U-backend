from django import template
from bs4 import BeautifulSoup
register = template.Library()

@register.filter(is_safe=True)
def get_paragraph(value):
    soup = BeautifulSoup(value,"html.parser")
    content = ""
    try:
        content = soup.find('p')
    except Exception as e:
        return content
    return str(content)
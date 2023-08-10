from xhtml2pdf import pisa
from django.shortcuts import render
from jinja2 import Environment, FileSystemLoader


def render_html(template_name, context):
    env = Environment(loader=FileSystemLoader(''))
    template = env.get_template(template_name)
    rendered_template = template.render(context)
    return rendered_template


def html_to_pdf(html_file_path, pdf_file_path, context):
    try:
        html_content = render_html(html_file_path, context)

        with open(pdf_file_path, 'wb') as pdf_file:
            pisa.CreatePDF(html_content, dest=pdf_file)

        print(f"Conversion successful. PDF saved at: {pdf_file_path}")
    except Exception as e:
        print(f"Conversion failed: {str(e)}")


def generate_sample_pdf(context):
    html_file_path = "utils/input.html"  
    pdf_file_path = "utils/output.pdf"

    html_to_pdf(html_file_path, pdf_file_path, context)

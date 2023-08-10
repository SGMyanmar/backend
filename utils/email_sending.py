from django.core.mail import EmailMessage
from django.conf import settings
from .pdf import generate_sample_pdf

def send_email_with_attachment(subject, body, to_emails, attachment_file_path):
    from_email = settings.EMAIL_HOST_USER
    email = EmailMessage(subject, body, from_email, to_emails)

    with open(attachment_file_path, 'rb') as file:
        email.attach_file(attachment_file_path)

    try:
        email.send()
        return True

    except Exception as e:
        print(str(e))
        return False


def send_sample_email(context):
    subject = 'Test Email with Attachment'
    to_emails = ['kyawkokotun888@gmail.com']
    generate_sample_pdf(context)
    attachment_file_path = 'utils/output.pdf'

    if send_email_with_attachment(subject, '', to_emails, attachment_file_path):
        print('Email sent successfully!')
    else:
        print('Failed to send email.')


if __name__ == '__main__':
    send_sample_email()

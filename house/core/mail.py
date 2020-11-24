from django.core.mail import send_mail


def send_test_mail():
    subject = 'Test send mail'
    message = 'My test'
    send_mail(subject, message, 'test@pp-ua.pp.ua', ['alex2011ua@gmail.com'])

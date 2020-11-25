from django.core.mail import send_mail


def send_test_mail(subject, message):

    send_mail(subject, message, 'test@pp-ua.pp.ua', ['alex2011ua@gmail.com'])

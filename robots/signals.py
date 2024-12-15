from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from orders.models import Order
from robots.models import Robot


@receiver(post_save, sender=Robot)
def notify_customers_when_robot_created(sender, instance, created, **kwargs):
    if created:  # We check that the robot has just been created
        orders = Order.objects.filter(robot_serial=instance.serial)
        for order in orders:
            send_mail(
                'Робот теперь в наличии!',
                f"""Добрый день!
Недавно вы интересовались нашим роботом модели {instance.model}, версии {instance.version}.
Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.""",
                'from@example.com',  # Sender's email address
                [order.customer.email],  # Recipient's email address
                fail_silently=False,
            )

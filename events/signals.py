from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Event


@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
   
    if created and not instance.is_active:
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.encoding import force_bytes
        from django.utils.http import urlsafe_base64_encode
        from django.urls import reverse
        
        
        token = default_token_generator.make_token(instance)
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        
       
        activation_url = reverse('activate_account', kwargs={'uidb64': uid, 'token': token})
        full_activation_url = f"{settings.SITE_URL}{activation_url}" if hasattr(settings, 'SITE_URL') else f"http://127.0.0.1:8000{activation_url}"
        
        
        subject = 'Activate Your Event Management Account'
        html_message = render_to_string('activation_email.html', {
            'user': instance,
            'activation_url': full_activation_url,
        })
        plain_message = strip_tags(html_message)
        
        
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                html_message=html_message,
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending activation email: {e}")


@receiver(m2m_changed, sender=Event.participants.through)
def send_rsvp_confirmation(sender, instance, action, pk_set, **kwargs):
    
    if action == 'post_add' and pk_set:
        users = User.objects.filter(pk__in=pk_set)
        
        for user in users:
            subject = f'RSVP Confirmation: {instance.event_name}'
            html_message = render_to_string('rsvp_confirmation_email.html', {
                'user': user,
                'event': instance,
            })
            plain_message = strip_tags(html_message)
            
            try:
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    html_message=html_message,
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error sending RSVP confirmation email: {e}")

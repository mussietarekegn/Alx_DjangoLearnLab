from django.contrib.contenttypes.models import ContentType
from .models import Notification


def create_notification(recipient, actor, verb, target=None):
    notification = Notification(
        recipient=recipient,
        actor=actor,
        verb=verb
    )

    if target:
        notification.target_content_type = ContentType.objects.get_for_model(target)
        notification.target_object_id = target.id

    notification.save()

from moderation import moderation
from voca.models import Device, Software, Vocabulary


moderation.register(Device)
moderation.register(Software)
moderation.register(Vocabulary)

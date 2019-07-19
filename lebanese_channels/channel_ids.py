from lebanese_channels.channel import Channel
# noinspection PyUnresolvedReferences
from lebanese_channels.services import *

CHANNEL_LIST = []

for cls in Channel.__subclasses__():
    CHANNEL_LIST.append(cls())

CHANNEL_LIST = sorted(CHANNEL_LIST, key=lambda x: x.get_name())

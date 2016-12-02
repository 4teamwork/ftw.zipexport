from ftw.zipexport.interfaces import IContainerZippedEvent
from ftw.zipexport.interfaces import IItemZippedEvent
from zope.interface import implements


class ContainerZippedEvent(object):
    implements(IContainerZippedEvent)

    def __init__(self, obj, comment=None, action=None, actor=None, time=None):
        self.object = obj
        self.action = action
        self.comment = comment
        self.actor = actor
        self.time = time


class ItemZippedEvent(object):
    implements(IItemZippedEvent)

    def __init__(self, obj, comment=None, action=None, actor=None, time=None):
        self.object = obj
        self.action = action
        self.comment = comment
        self.actor = actor
        self.time = time

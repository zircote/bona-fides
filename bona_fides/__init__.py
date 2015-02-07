# coding: utf-8
from __future__ import absolute_import
import json
from .notifications import SubscriptionConfirmation, UnsubscribeConfirmation, Notification

class Validator(object):
    UNSUBSCRIBE = 'unsubscribe'
    SUBSCRIBE = 'subscribe'
    DROP = 'drop'
    ACCEPT = 'accept'

    _default_options = {
        "white_list": [],
        "validate_signature": True

    }

    def __init__(self, options):
        """
        
        :param options dict: 
        :return:
        """
        self.options = dict(self._default_options.items() + options.items())

    def handle(self, json_string):
        try:
            _raw = json.loads(json_string)
        except ValueError as e:
            raise e
        if _raw['Type'] in ['SubscriptionConfirmation']:
            mesg = SubscriptionConfirmation(_raw, validate_signature=self.options['validate_signature'])
        elif _raw['Type'] in ['Notification']:
            mesg = Notification(_raw, validate_signature=self.options['validate_signature'])
        elif _raw['Type'] in ['UnsubscribeConfirmation']:
            mesg = UnsubscribeConfirmation(_raw, validate_signature=self.options['validate_signature'])
        else:
            # Todo Log-it
            raise Exception
        if not mesg.is_valid:
            pass
        if not self.is_acceptable(_raw['TopicArn']):
            pass
        return mesg
    
    def is_acceptable(self, topic_arn):
        if topic_arn not in self.options['white_list']:
            return False
        return True


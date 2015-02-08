# coding: utf-8
# Copyright [2015] [Robert Allen]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
import bona_fides


with open('request.json') as f:
    m = f.read()
OPTIONS = {
    "white_list": [
        "arn:aws:sns:us-west-2:123456789012:MyTopic",
    ],
    "unknown_message_action": bona_fides.Validator.UNSUBSCRIBE,
    "validate_signature": True
}

sns_validation = bona_fides.Validator(OPTIONS)
notification = sns_validation.handle(m)
assert notification.is_valid is True, 'Signature is not valid.'
print notification.message
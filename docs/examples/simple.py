import bona_fides


with open('request.json') as f:
    m = f.read()
OPTIONS = {
    "white_list": [
        "arn:aws:sns:us-east-1:199999999999:blah_blah",  # Accept for a specific topic/arn
    ],
    "unknown_message_action": bona_fides.Validator.UNSUBSCRIBE,
    "validate_signature": True
}

sns_validation = bona_fides.Validator(OPTIONS)
notification = sns_validation.handle(m)
if notification.is_valid:
    print notification.message
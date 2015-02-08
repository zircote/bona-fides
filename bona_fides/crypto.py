# coding: utf-8
# Copyright [2015] [Robert Allen]
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
#
from __future__ import absolute_import
from M2Crypto import X509
from base64 import b64decode
import httplib2
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())


class ValidationException(Exception):
    def __init__(self, *args, **kwargs):
        super(ValidationException, self).__init__(*args, **kwargs)


class Version1(object):
    signing_certs = {}

    def __init__(self, message):
        self.message = message

    @property
    def pub_key(self):
        """
        :return str:
        """
        if 'SigningCertURL' not in self.message.raw_message:
            ex = ValidationException("Invalid event message")
            logging.error(ex)
            raise ex
        if self.message.raw_message['SigningCertURL'] in self.signing_certs:
            logging.debug("SigningCertURL: [%s] exists in memory" % self.message.raw_message['SigningCertURL'])
            return self.signing_certs[self.message.raw_message['SigningCertURL']]
        return self._fetch_signing_key()


    @property
    def encoded_message(self):
        """
        :return str:
        """
        if not self.message.raw_message:
            logging.info("no valid raw_message to encode")
            return ""
        msg = []
        for i in self.message.SIGNATURE_ATTR:
            if i is 'Subject' and (i in self.message.raw_message and len(self.message.raw_message[i]) == 0):
                continue
            msg.append(i)
            msg.append(self.message.raw_message[i])
        as_str = "\n".join(msg)
        logging.debug("encoded message as: [%s]" % as_str)
        return as_str + "\n"

    def validate(self):
        """
        :return bool:
        :raises Exception:
        """
        cert = X509.load_cert_string(self.pub_key)
        pubkey = cert.get_pubkey()
        pubkey.reset_context(md='sha1')
        pubkey.verify_init()
        pubkey.verify_update(self.encoded_message.encode())
        result = pubkey.verify_final(b64decode(self.message.signature))
        if result != 1:
            logging.error('Signature could not be verified for MessageId:[%s]' % self.message.raw_message['MessageId'])
            return False
        return True

    def _fetch_signing_key(self):
        """
        :return str:
        """
        h = httplib2.Http()
        response, content = h.request(self.message.raw_message['SigningCertURL'], 'GET')
        self.signing_certs[self.message.raw_message['SigningCertURL']] = content
        logging.info("adding Signing Key: [%s]" % self.message.raw_message['SigningCertURL'])
        return self.signing_certs[self.message.raw_message['SigningCertURL']]
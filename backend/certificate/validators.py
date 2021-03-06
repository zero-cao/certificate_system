import re
from django.utils.encoding import force_text
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address
from django.utils.translation import gettext_lazy as _


class DomainNameValidator(object):
    """
    Domain name validator adapted from Django's EmailValidator.
    """
    message = 'Enter a valid domain name.'
    code = 'invalid'
    domain_regex = re.compile(
        r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,})$'  # domain
        # literal form, ipv4 address (SMTP 4.1.3)
        r'|^\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]$',
        re.IGNORECASE)
    domain_whitelist = ['localhost']

    def __init__(self, message=None, code=None, whitelist=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if whitelist is not None:
            self.domain_whitelist = whitelist

    def __call__(self, value):
        value = force_text(value)

        if not value:
            raise ValidationError(self.message, code=self.code)

        if (not value in self.domain_whitelist and
                not self.domain_regex.match(value)):
            # Try for possible IDN domain-part
            try:
                value = value.encode('idna').decode('ascii')
                if not self.domain_regex.match(value):
                    raise ValidationError(self.message, code=self.code)
                else:
                    return
            except UnicodeError:
                pass
            raise ValidationError(self.message, code=self.code)


validate_domain_name = DomainNameValidator()


def validate_fqdn(value):
    try:
        validate_domain_name(value)
        return True
    except ValidationError:
        return False


def validate_fqdn_or_ipv46_address(value):
    try:
        validate_ipv46_address(value)
        return True        
    except ValidationError:
        try:
            validate_domain_name(value)
            return True
        except ValidationError:
            return False


def validate_password(value1, value2):
    if len(value1) < 6:
        raise ValidationError(_("Password length is shorter than 6 characters."), code='invalid')

    if value1 != value2:
        raise ValidationError(_("Password mismatch."), code='invalid')

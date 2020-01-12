from cryptography import x509
from cryptography.x509.oid import NameOID, ExtendedKeyUsageOID
from cryptography.x509.extensions import KeyUsage, ExtendedKeyUsage, UnrecognizedExtension
from cryptography.x509.extensions import SubjectAlternativeName, SubjectKeyIdentifier
from cryptography.x509.extensions import BasicConstraints, AuthorityInformationAccess
from cryptography.x509.extensions import CRLDistributionPoints, AuthorityKeyIdentifier
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates
import ipaddress
import datetime
import logging
import os


logger = logging.getLogger('django.certificate')


class CertificateRequest(object):
    def __init__(self, obj):
        self.obj = obj

    def subject(self, is_object=True):
        if is_object: return self.obj.subject

        sub = dict()
        for name in self.obj.subject: sub[name.oid._name] = name.value
        return sub

    def public_key(self, is_object=True):
        if is_object: return self.obj.public_key()

        return self.obj.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()

    def public_key_bytes(self):
        return self.obj.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

    def extensions(self, is_object=True):
        if is_object: return self.obj.extensions

        ext_parent = dict()

        for ext in self.obj.extensions:
            ext_child = None
            if isinstance(ext.value, KeyUsage):
                ext_child = set()
                if ext.value.digital_signature: ext_child.add('digital_signature')
                if ext.value.data_encipherment: ext_child.add('data_encipherment')
                if ext.value.content_commitment: ext_child.add('content_commitment')
                if ext.value.crl_sign: ext_child.add('crl_sign')
                if ext.value.key_encipherment: ext_child.add('key_encipherment')
                if ext.value.key_cert_sign: ext_child.add('key_cert_sign')
                if ext.value.key_agreement:
                    ext_child.add('key_agreement')
                    if ext.value.encipher_only: ext_child.add('encipher_only')
                    if ext.value.decipher_only: ext_child.add('decipher_only')

            elif isinstance(ext.value, ExtendedKeyUsage):
                ext_child = set()
                for subext in ext.value:
                    ext_child.add(subext._name)

            elif isinstance(ext.value, SubjectAlternativeName):
                ext_child = {'DNS Name': [], 'IPv4 Address': [], 'IPv6 Address': []}

                for subext in ext.value._general_names._general_names:
                    if isinstance(subext, x509.general_name.DNSName):
                        ext_child['DNS Name'].append(subext.value)

                    elif isinstance(subext, x509.general_name.IPAddress) and \
                            isinstance(subext.value, ipaddress.IPv4Address):
                        ext_child['IPv4 Address'].append(subext.value.exploded)

                    elif isinstance(subext, x509.general_name.IPAddress) and \
                            isinstance(subext.value, ipaddress.IPv6Address):
                        ext_child['IPv6 Address'].append(subext.value.exploded)

            elif isinstance(ext.value, SubjectKeyIdentifier):
                ext_child = str(ext.value.digest)

            elif isinstance(ext.value, AuthorityKeyIdentifier):
                ext_child =[str(ext.value.key_identifier), ext.value.authority_cert_issuer,
                            ext.value.authority_cert_serial_number]

            elif isinstance(ext.value, BasicConstraints):
                ext_child = dict()
                ext_child['CA'] = str(ext.value.ca)

            # elif isinstance(ext.value, AuthorityInformationAccess):
            #     for subext in ext.value._descriptions:
            #         ext_child[] = str(ext.value._descriptions)

            elif isinstance(ext.value, CRLDistributionPoints):
                ext_child = str(ext.value._distribution_points)

            elif isinstance(ext.value, UnrecognizedExtension):
                ext_child = str(ext.value.value)

            else:
                ext_child = str(ext.value)
                logging.info(ext_child)
            ext_parent[ext.value.oid._name] = ext_child

        return ext_parent


class ReadRequest(CertificateRequest):
    is_valid = True

    def __init__(self, subject):
        if not subject:
            subject = {'req_bytes': b'', 'req_codec': ''}
            
        try:
            self.req = x509.load_pem_x509_csr(subject['req_bytes'], default_backend()) or \
                       x509.load_der_x509_csr(subject['req_bytes'], default_backend())
            
            logger.debug('Certificate signing request format is {}'.format(subject['req_codec']))
            logger.debug('Certificate signing request is:\n{}'.format(subject['req_bytes'].decode()))

            CertificateRequest.__init__(self, self.req)

        except ValueError:
            self.is_valid = False
            logger.error('Certificate signing request maybe be broken')


    def req_signature(self):
        if not self.is_valid: return False

        sign = dict()
        sign['sign_alg'] = self.req.signature_algorithm_oid._name
        sign['sign_data'] = str(self.req.signature)

        return sign

    def request(self, is_object=True):
        if not self.is_valid: return False
        if is_object: return self.req

        result = {'subject': self.subject(is_object=False), 
                  'extensions': self.extensions(is_object=False), 
                  "signature": self.req_signature()} 

        logger.debug(result)
        return result
    
    def request_bytes(self):
        return self.req.public_bytes(serialization.Encoding.PEM)


class ReadCertificate(CertificateRequest):
    is_valid = True

    def __init__(self, subject):
        if not subject:
            subject = {'crt_bytes': b'', 'crt_codec': ''}
            
        try:
            self.crt = x509.load_pem_x509_certificate(subject['crt_bytes'], default_backend()) or \
                       x509.load_der_x509_certificate(subject['crt_bytes'], default_backend())
            
            logger.debug('Certificate format is {}'.format(subject['crt_codec']))
            logger.debug('Certificate is:\n{}'.format(subject['crt_bytes'].decode()))

            CertificateRequest.__init__(self, self.crt)

        except ValueError:
            self.is_valid = False
            logger.error('Certificate maybe be broken')

    def issuer(self, is_object=True):
        if not self.is_valid: return False
        if is_object: return self.crt.issuer

        sub = dict()
        for name in self.crt.issuer: sub[name.oid._name] = name.value
        return sub

    def validity(self):
        if not self.is_valid: return False
        return {
            'From': str(self.crt.not_valid_before),
            'To': str(self.crt.not_valid_after)
        }

    def version(self):
        if not self.is_valid: return False
        return self.crt.version.name

    def serial_number(self):
        if not self.is_valid: return False
        return self.crt.serial_number

    def signature(self):
        if not self.is_valid: return False
        sign = dict()
        sign['sign_alg'] = self.crt.signature_algorithm_oid._name
        sign['sign_data'] = str(self.crt.signature)
        return sign

    def certificate(self, is_object=True):
        if not self.is_valid: return False
        if is_object: return self.crt

        result = {'issuer': self.issuer(is_object=False), 
                  'validity': self.validity(),
                  'subject': self.subject(is_object=False), 
                  'extensions': self.extensions(is_object=False), 
                  'signature': self.signature(),
                  'others': {
                    'version': self.version(), 
                    'serial_number': self.serial_number()}}

        logger.debug(result)
        return result
    
    def certificate_bytes(self):
        logger.debug('\n{}'.format(self.crt.public_bytes(serialization.Encoding.PEM).decode()))
        return self.crt.public_bytes(serialization.Encoding.PEM)
        

def publish_certificate(req, ca, valid_year, hash_alg, is_ca, logger):
    logger.info('Create a certificate builder...')
    crt_builder = x509.CertificateBuilder()
    crt_builder = crt_builder.subject_name(name=req.subject())
    crt_builder = crt_builder.public_key(key=req.public_key())
    for extension in req.extensions():
        crt_builder = crt_builder.add_extension(extension=extension.value, 
                                                critical=extension.critical)

    logger.info('Ready to sign the certificate request...')
    if not isinstance(valid_year, int): valid_year = int(valid_year)
    if is_ca == 'true': is_ca = True
    if is_ca == 'false': is_ca = False
    crt_builder = crt_builder.not_valid_before(time=datetime.datetime.today())
    crt_builder = crt_builder.not_valid_after(
        time=datetime.datetime.today()+datetime.timedelta(days=valid_year*365))
    crt_builder = crt_builder.serial_number(number=x509.random_serial_number())
    crt_builder = crt_builder.add_extension(
        extension=x509.BasicConstraints(ca=is_ca, path_length=None), critical=True)

    logger.info('Select CA to sign the certificate signing request and output certificate')
    if ca == 'SelfSign':
        logger.debug('CA is self-signed')
        crt_builder = crt_builder.issuer_name(name=req.subject())
        ca_key = req.private_key()
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
        ca_dir = os.path.join(base_dir, 'common_static/ca') 
        ca = "{}/{}.pfx".format(ca_dir, ca)
        logger.debug("CA file is located in {}".format(ca))
        with open(file=ca, mode='rb') as f:
            ca_key, ca_crt, ca_others = load_key_and_certificates(
                data=f.read(), password=b'Cisco123!', backend=default_backend())
            crt_builder = crt_builder.issuer_name(name=ca_crt.subject)

    hash_obj_list = {hashes.MD5(), hashes.SHA1(), hashes.SHA224(), hashes.SHA256(), 
            hashes.SHA384(), hashes.SHA512(), hashes.SHA512_224(), 
            hashes.SHA512_256(), hashes.SHA3_224(), hashes.SHA3_256(), 
            hashes.SHA3_384(), hashes.SHA3_512()}
            
    for hash_obj in hash_obj_list:
        if hash_alg == hash_obj.name:
            hash_algor = hash_obj
            break
        else:
            hash_algor = hashes.MD5()

    return crt_builder.sign(private_key=ca_key, algorithm=hash_algor, 
                            backend=default_backend())


class SignCertificate(ReadCertificate, ReadRequest):
    def __init__(self, issuer, subject):
        if not subject:
            subject = {'req': b'', 'req_codec': 'pem', 'req_file': b''}
        if not issuer:
            issuer = {'ca': 'caowen-rootca', 'valid_year': 1, 'hash_alg': 'md5', 'is_ca': 'no'}
        logger.info('Start to read certificate signing request...')
        ReadRequest.__init__(self, subject)
        self.crt = publish_certificate(self, issuer['ca'], issuer['valid_year'], 
            issuer['hash_alg'], issuer['is_ca'], logger)


class MakeKey(object):
    def __init__(self, key=None):
        if not key:
            key = {'key_type': 'rsa', 'key_length': 2048}
        if not isinstance(key['key_length'], int):
            key['key_length'] = int(key['key_length'])

        if key['key_type'].lower() == 'rsa':
            logger.info('Generate RSA key')
            self.key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=key['key_length'],
                backend=default_backend()
            )

        elif key['key_type'].lower() == 'dsa':
            logger.info('Generate DSA key')
            pass

        elif key['key_type'].lower() == 'ec':
            logger.info('Generate EC key')
            pass

    def private_key(self, is_object=True):
        if is_object: return self.key

        return self.key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(b"cisco123!"),
            ).decode()

    def public_key(self, is_object=True):
        if is_object: return self.key.public_key()

        return self.key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()


class MakeRequest(MakeKey, ReadRequest):
    def __init__(self, basic_information, extensions, key):
        if not basic_information:
            basic_information = {'common_name': '', 'country': '', 'province': '', 
                                 'locality': '', 'organization': '', 'unit': ''}

        if not extensions:
            extensions = {'alias_names': [], 'key_usages': [], 'extended_key_usages': []}

        if not key:
            key = {'key_type': 'rsa', 'key_length': 2048}

        logger.info('Start to generate a key...')
        MakeKey.__init__(self, key=key)

        logger.info('Start to generate a basic infomation...')
        info_list = [
            x509.NameAttribute(NameOID.COMMON_NAME, basic_information['common_name']),
            x509.NameAttribute(NameOID.COUNTRY_NAME, basic_information.get('country')),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, basic_information.get('province')),
            x509.NameAttribute(NameOID.LOCALITY_NAME, basic_information.get('locality')),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, basic_information.get('organization')),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, basic_information.get('unit')),
        ]
        self.req_builder = x509.CertificateSigningRequestBuilder().subject_name(
            name=x509.Name(info_list))

        logger.info('Start to add extensions...')
        alias_list = []
        for alias_name in extensions['alias_names']:
            try: address = ipaddress.ip_address(alias_name['value'])
            except ValueError: alias_list.append(x509.DNSName(alias_name['value']))
            else: alias_list.append(x509.IPAddress(address))
        self.req_builder = self.req_builder.add_extension(
            extension=x509.SubjectAlternativeName(alias_list), critical=False)

        digital_signature = True if 'digital_signature' in extensions['key_usages'] else False
        content_commitment = True if 'content_commitment' in extensions['key_usages'] else False
        key_encipherment = True if 'key_enciphermentt' in extensions['key_usages'] else False
        data_encipherment = True if 'data_encipherment' in extensions['key_usages'] else False
        key_agreement = True if 'key_agreement' in extensions['key_usages'] else False
        key_cert_sign = True if 'key_cert_sign' in extensions['key_usages'] else False
        crl_sign = True if 'crl_sign' in extensions['key_usages'] else False
        encipher_only = True if 'encipher_only' in extensions['key_usages'] else False
        decipher_only = True if 'decipher_only' in extensions['key_usages'] else False
        self.req_builder = self.req_builder.add_extension(
            extension=x509.KeyUsage(digital_signature, content_commitment, key_encipherment, 
            data_encipherment, key_agreement, key_cert_sign, crl_sign, encipher_only,
            decipher_only), critical=False)

        extended_key_usages = []
        if 'client_auth' in extensions['extended_key_usages']: 
            extended_key_usages.append(ExtendedKeyUsageOID.CLIENT_AUTH)
        if 'server_auth' in extensions['extended_key_usages']: 
            extended_key_usages.append(ExtendedKeyUsageOID.SERVER_AUTH)
        if 'code_sign' in extensions['extended_key_usages']: 
            extended_key_usages.append(ExtendedKeyUsageOID.CODE_SIGNING)
        if 'oscp_sign' in extensions['extended_key_usages']: 
            extended_key_usages.append(ExtendedKeyUsageOID.OCSP_SIGNING)
        self.req_builder = self.req_builder.add_extension(
            extension=x509.ExtendedKeyUsage(extended_key_usages), critical=False)

        logger.info('Start to export certificate signing request...')
        self.req = self.req_builder.sign(private_key=self.private_key(), 
            algorithm=hashes.SHA256(), backend=default_backend())

        CertificateRequest.__init__(self, self.req)


class MakeCertificate(ReadCertificate, MakeRequest):
    def __init__(self, issuer, basic_information, extensions, key):
        if not issuer:
            issuer = {'ca': '', 'valid_year': 1, 'hash_alg': '', 'is_ca': ''}

        if not basic_information:
            basic_information = {'common_name': '', 'country': '', 'province': '', 
                                 'locality': '', 'organization': '', 'unit': ''}

        if not extensions:
            extensions = {'alias_names': [], 'key_usages': [], 'extended_key_usages': []}

        if not key:
            key = {'key_type': 'rsa', 'key_length': 2048}

        logger.info('Start to generate certificate signing request...')
        MakeRequest.__init__(self, basic_information, extensions, key)
        self.crt = publish_certificate(self, issuer['ca'], issuer['valid_year'], 
                                       issuer['hash_alg'], issuer['is_ca'], logger)

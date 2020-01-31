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


class _PublicKey(object):
    def __init__(self, pub_key: object):
        self.__pub_key = pub_key

    def _public_key(self, data_type='object'):
        if data_type == 'object': 
            return self.__pub_key

        elif data_type == 'json':
            return {'type': 'rsa',
                    'bytes': self.__pub_key.public_bytes(encoding=serialization.Encoding.PEM,
                            format=serialization.PublicFormat.SubjectPublicKeyInfo).decode()}

        elif data_type == 'bytes':
            return self.__pub_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo)


class _CertificateRequest(_PublicKey):
    def __init__(self, crt_req: object):
        self.__crt_req = crt_req
        _PublicKey.__init__(self, self.__crt_req.public_key())

    def _subject(self, data_type='object'):
        if data_type == 'object': return self.__crt_req.subject

        sub = dict()
        for name in self.__crt_req.subject: sub[name.oid._name] = name.value
        return sub

    def _extensions(self, data_type='object'):
        if data_type == 'object': return self.__crt_req.extensions

        ext_parent = dict()

        for ext in self.__crt_req.extensions:
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

            # elif isinstance(ext.value, SubjectKeyIdentifier):
            #     ext_child = str(ext.value.digest)

            # elif isinstance(ext.value, AuthorityKeyIdentifier):
            #     ext_child =[str(ext.value.key_identifier), ext.value.authority_cert_issuer,
            #                 ext.value.authority_cert_serial_number]

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


class _Request(_CertificateRequest):
    def __init__(self, req: object):
        self.__req = req
        _CertificateRequest.__init__(self, self.__req)

    def request(self, data_type='object'):
        if data_type == 'object': 
            return self.__req

        elif data_type == 'json':
            return {'subject': self._subject(data_type='json'), 
                    'extensions': self._extensions(data_type='json'), 
                    'public_key': self._public_key(data_type='json'),
                    "signature": {
                      'sign_alg': self.__req.signature_algorithm_oid._name,
                      'sign_data': str(self.__req.signature)
                    }} 
      
        elif data_type == 'bytes':
            return self.__req.public_bytes(serialization.Encoding.PEM)


class _Certificate(_CertificateRequest):
    def __init__(self, crt: object):
        self.__crt = crt
        _CertificateRequest.__init__(self, self.__crt)

    def _issuer(self, data_type='object'):
        if data_type == 'object': return self.__crt.issuer

        sub = dict()
        for name in self.__crt.issuer: sub[name.oid._name] = name.value
        return sub

    def certificate(self, data_type='object'):
        if data_type == 'object': 
            return self.__crt

        elif data_type == 'json':
            return {'issuer': self._issuer(data_type='json'), 
                    'validity': {
                        'From': str(self.__crt.not_valid_before),
                        'To': str(self.__crt.not_valid_after)
                    },
                    'subject': self._subject(data_type='json'), 
                    'public_key': self._public_key(data_type='json'),
                    'extensions': self._extensions(data_type='json'), 
                    'signature': {
                        'sign_alg': self.__crt.signature_algorithm_oid._name,
                        'sign_data': str(self.__crt.signature)
                    },
                    'others': {
                        'version': self.__crt.version.name, 
                        'serial_number': self.__crt.serial_number}}

        elif data_type == 'bytes':
            logger.debug('\n{}'.format(
                self.__crt.public_bytes(serialization.Encoding.PEM).decode()))
            return self.__crt.public_bytes(serialization.Encoding.PEM)
       

class _Key(_PublicKey):
    def __init__(self, key: object, password: bytes):
        self.__key = key
        self.__password = password
        _PublicKey.__init__(self, self.__key.public_key())

    def private_key(self, data_type='object'):
        if data_type == 'object': 
            return self.__key

        elif data_type == 'json':
            return self.__key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.BestAvailableEncryption(self.__password)).decode()

        elif data_type == 'bytes':
            return self.__key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.BestAvailableEncryption(self.__password))
        

class _MakeKey(_Key):
    def __init__(self, key: dict):
        if not isinstance(key['key_length'], int):
            key['key_length'] = int(key['key_length'])

        if key['key_type'].lower() == 'rsa':
            logger.info('Generate RSA key')
            key_obj = rsa.generate_private_key(
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

        _Key.__init__(self, key_obj, key['password'].encode())


def _publish_certificate(req: object, issuer: dict):
    logger.info('Create a certificate builder...')
    crt_builder = x509.CertificateBuilder()
    crt_builder = crt_builder.subject_name(name=req._subject())
    crt_builder = crt_builder.public_key(key=req._public_key())
    for extension in req._extensions():
        crt_builder = crt_builder.add_extension(extension=extension.value, 
                                                critical=extension.critical)

    logger.info('Ready to sign the certificate request...')
    if not isinstance(issuer['valid_year'], int): issuer['valid_year'] = int(issuer['valid_year'])
    if issuer['is_ca'] == 'true': issuer['is_ca'] = True
    if issuer['is_ca'] == 'false': issuer['is_ca'] = False
    crt_builder = crt_builder.not_valid_before(time=datetime.datetime.today())
    crt_builder = crt_builder.not_valid_after(
        time=datetime.datetime.today()+datetime.timedelta(days=issuer['valid_year']*365))
    crt_builder = crt_builder.serial_number(number=x509.random_serial_number())
    crt_builder = crt_builder.add_extension(
        extension=x509.BasicConstraints(ca=issuer['is_ca'], path_length=None), critical=True)

    logger.info('Select CA to sign the certificate signing request and output certificate')
    if issuer['ca'] == 'SelfSign':
        logger.debug('CA is self-signed')
        crt_builder = crt_builder.issuer_name(name=req._subject())
        ca_key = req.private_key()

    else:
        ca_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'common_static/ca') 
        ca_file = "{}/{}.pfx".format(ca_dir, issuer['ca'])
        logger.debug("CA file is located in {}".format(ca_file))

        with open(file=ca_file, mode='rb') as f:
            ca_bytes = f.read()

        logger.debug('CA file content is \n{}'.format(ca_bytes))
        crt_chain = ReadCertificateChain(ca_bytes, b'Cisco123!')      
        ca_crt = crt_chain.certificate(data_type='object')
        ca_key = crt_chain.private_key(data_type='object')      
        crt_builder = crt_builder.issuer_name(name=ca_crt.subject)

    hash_obj_list = {hashes.MD5(), hashes.SHA1(), hashes.SHA224(), hashes.SHA256(), 
            hashes.SHA384(), hashes.SHA512(), hashes.SHA512_224(), 
            hashes.SHA512_256(), hashes.SHA3_224(), hashes.SHA3_256(), 
            hashes.SHA3_384(), hashes.SHA3_512()}
            
    for hash_obj in hash_obj_list:
        if issuer['hash_alg'] == hash_obj.name:
            hash_algor = hash_obj
            break
        else:
            hash_algor = hashes.MD5()

    return crt_builder.sign(private_key=ca_key, algorithm=hash_algor, backend=default_backend())


class ReadRequest(_Request):
    def __init__(self, subject: dict):          
        try:
            req_obj = x509.load_pem_x509_csr(subject['bytes'], default_backend())
        except:
            try:
                req_obj = x509.load_der_x509_csr(subject['bytes'], default_backend())
            except:
                raise ValueError('request must be wrong')            
        
        logger.debug('Certificate signing request is:\n{}'.format(subject['bytes']))

        _Request.__init__(self, req_obj)


class MakeRequest(_MakeKey, _Request):
    def __init__(self, subject: dict):
        logger.info('Start to generate a key...')
        _MakeKey.__init__(self, subject['key'])

        logger.info('Start to generate a basic infomation...')
        info_list = [
            x509.NameAttribute(NameOID.COMMON_NAME, subject['basic_information']['common_name']),
            x509.NameAttribute(NameOID.COUNTRY_NAME, subject['basic_information'].get('country')),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, subject['basic_information'].get('province')),
            x509.NameAttribute(NameOID.LOCALITY_NAME, subject['basic_information'].get('locality')),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, subject['basic_information'].get('organization')),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, subject['basic_information'].get('unit')),
        ]
        req_builder = x509.CertificateSigningRequestBuilder().subject_name(name=x509.Name(info_list))

        logger.info('Start to add extensions...')
        alias_list = []
        for alias_name in subject['extensions']['alias_names']:
            try: address = ipaddress.ip_address(alias_name['value'])
            except ValueError: alias_list.append(x509.DNSName(alias_name['value']))
            else: alias_list.append(x509.IPAddress(address))
        req_builder = req_builder.add_extension(
            extension=x509.SubjectAlternativeName(alias_list), critical=False)

        digital_signature = True if 'digital_signature' in subject['extensions']['key_usages'] else False
        content_commitment = True if 'content_commitment' in subject['extensions']['key_usages'] else False
        key_encipherment = True if 'key_enciphermentt' in subject['extensions']['key_usages'] else False
        data_encipherment = True if 'data_encipherment' in subject['extensions']['key_usages'] else False
        key_agreement = True if 'key_agreement' in subject['extensions']['key_usages'] else False
        key_cert_sign = True if 'key_cert_sign' in subject['extensions']['key_usages'] else False
        crl_sign = True if 'crl_sign' in subject['extensions']['key_usages'] else False
        encipher_only = True if 'encipher_only' in subject['extensions']['key_usages'] else False
        decipher_only = True if 'decipher_only' in subject['extensions']['key_usages'] else False
        req_builder = req_builder.add_extension(
            extension=x509.KeyUsage(digital_signature, content_commitment, key_encipherment, 
            data_encipherment, key_agreement, key_cert_sign, crl_sign, encipher_only,
            decipher_only), critical=False)

        extended_key_usages = []
        if 'client_auth' in subject['extensions']['extended_key_usages']: 
            extended_key_usages.append(ExtendedKeyUsageOID.CLIENT_AUTH)
        if 'server_auth' in subject['extensions']['extended_key_usages']: 
            extended_key_usages.append(ExtendedKeyUsageOID.SERVER_AUTH)
        if 'code_sign' in subject['extensions']['extended_key_usages']: 
            extended_key_usages.append(ExtendedKeyUsageOID.CODE_SIGNING)
        if 'oscp_sign' in subject['extensions']['extended_key_usages']: 
            extended_key_usages.append(ExtendedKeyUsageOID.OCSP_SIGNING)
        req_builder = req_builder.add_extension(
            extension=x509.ExtendedKeyUsage(extended_key_usages), critical=False)

        logger.info('Start to export certificate signing request...')
        req_obj = req_builder.sign(private_key=self.private_key(), 
            algorithm=hashes.SHA256(), backend=default_backend())

        _Request.__init__(self, req_obj)

    
class ReadCertificate(_Certificate):
    def __init__(self, subject: dict):            
        try:    
            crt_obj = x509.load_pem_x509_certificate(subject['bytes'], default_backend()) 
        except:
            try:
                crt_obj = x509.load_der_x509_certificate(subject['bytes'], default_backend())
            except:
                raise ValueError('certificate must be wrong')
        
        logger.debug('Certificate is:\n{}'.format(subject['bytes']))

        _Certificate.__init__(self, crt_obj)


class ReadCertificateChain(_Certificate, _Key):
    def __init__(self, chain: bytes, password: bytes):
        self._chain = chain
        logger.debug('Certificate chain bytes are:\n{}'.format(chain))
        logger.debug('Certificate chain password is {}'.format(password))        

        try: 
            key, crt, self._ca = load_key_and_certificates(data=chain, password=password, backend=default_backend())
            # logger.debug('Certificate chain ca are:\n{}'.format(self._ca))
            _Certificate.__init__(self, crt)
            _Key.__init__(self, key, password)

        except Exception as err: 
            raise (err)

    def _issuers(self):
        issuers = []
        for issuer in self._ca:
            issuers.append(issuer)
        return issuers
    
    def certficate_chain(self, data_type='bytes'):
        if data_type == 'bytes': 
            return self._chain
        
        elif data_type == 'json':
            return {
                'issuers': self._issuers(),
                'subject': self._subject(),
                'key': self.private_key() or None
            }


class SignCertificate(_Certificate, ReadRequest):
    def __init__(self, issuer: dict, subject: dict):
        logger.info('Start to read certificate signing request...')
        ReadRequest.__init__(self, subject)
        crt_obj = _publish_certificate(self, issuer)
        _Certificate.__init__(self, crt_obj)


class MakeCertificate(_Certificate, MakeRequest):
    def __init__(self, issuer: dict, subject: dict):
        logger.info('Start to generate certificate signing request...')
        MakeRequest.__init__(self, subject)
        crt_obj = _publish_certificate(self, issuer)
        _Certificate.__init__(self, crt_obj)

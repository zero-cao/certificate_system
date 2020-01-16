from rest_framework.response import Response
from rest_framework import status
from django.core import files
from .validators import validate_fqdn_or_ipv46_address
import logging


logger = logging.getLogger('django.certificate')


def key_exist_valid(input, key_name, scope):
    if key_name not in input:
        logger.error('The key "{}" does not exist'.format(key_name))
        return False
    
    if input[key_name] == None or input[key_name] == '' or input[key_name] == b'':
        logger.error('The key "{}" value is empty'.format(key_name))
        return False

    logger.debug('The key "{}" value is: {}'.format(key_name, {
        'current_value': input[key_name],
        'value_type': type(input[key_name]),
        'value_scope': scope
    }))

    if isinstance(scope, list):
        if input[key_name] not in scope:
            logger.error('Please keep key "{}" value be valid'.format(key_name))
            return False
    elif isinstance(scope, range):
        if int(input[key_name]) not in scope:
            logger.error('Please keep key "{}" value be valid'.format(key_name))
            return False
    else:
        if not isinstance(input[key_name], scope):
            logger.error('Please keep key "{}" value be valid'.format(key_name))
            return False

    return True


def verifier_log(post):
    def inner(self, request):
        logger.info('Receive a post request from client {}'.format(request.META['REMOTE_ADDR']))
        logger.debug(request.data)
        logger.info('Handle client posted data')
        return post(self, request)

    return inner


def verifier_crt(post):   
    def inner(self, request):
        logger.info('Verify client posted data')        
        if not key_exist_valid(request.data.dict(), 'codec', ['pem', 'der']) or \
           not key_exist_valid(request.data.dict(), 'type', ['crt', 'req']):

            return Response(data={'error': 'Keys or value are wrong'}, 
                                   status=status.HTTP_400_BAD_REQUEST)

        if not key_exist_valid(request.data.dict(), 'obj', files.uploadedfile.InMemoryUploadedFile):

                return Response(data={'error': 'Keys or value are wrong'}, 
                                    status=status.HTTP_400_BAD_REQUEST)  
        
        return post(self, request)

    return inner


def verifier_crt_sign(post):   
    key_scope = {
        'req_codec': ['pem', 'der'],
        'ca': ['wenca-rootca', 'wenca-subca', 'wenca-grandca', 'SelfSign'],
        'valid_year': range(1, 21),
        'hash_alg': ['md5', 'sha1', 'sha256', 'sha384', 'sha512'],
        'is_ca': ['true', 'false'] 
    }

    def inner(self, request):
        logger.info('Verify client posted data')        
        for key in key_scope:
            if not key_exist_valid(request.data.dict(), key, key_scope[key]):
                return Response(data={'error': 'Keys or value are wrong'}, status=status.HTTP_400_BAD_REQUEST)

        if not key_exist_valid(request.FILES, 'req', files.uploadedfile.InMemoryUploadedFile):
            return Response(data={'error': 'Keys or value are wrong'}, status=status.HTTP_400_BAD_REQUEST)

        return post(self, request)

    return inner


def verifier_crt_make(post):
    issuer_scope = {
        'ca': ['wenca-rootca', 'wenca-subca', 'wenca-grandca', 'SelfSign'],
        'valid_year': range(1, 21),
        'hash_alg': ['md5', 'sha1', 'sha256', 'sha384', 'sha512'],
        'is_ca': [True, False] 
    }

    basic_information_scope = {
        'common_name': str,
        'country': ['CN', 'US'], 
        'province': str, 
        'locality': str, 
        'organization': str, 
        'unit': str, 
    } 

    key_scope = {
        'key_type': ['rsa', 'dsa', 'ecdsa'],
        'key_length': [1024, 2048, 3072, 4096],
        'password': str
    }

    extensions_scope = {
        'key_usages': ['digital_signature', 
            'content_commitment', 
            'key_encipherment', 
            'data_encipherment',
            'key_agreement', 
            'key_cert_sign', 
            'crl_sign', 
            'encipher_only', 
            'decipher_only'
        ],
        'extended_key_usages': [
            'client_auth',
            'server_auth',
            'code_sign',
            'oscp_sign'
        ],
    }

    def inner(self, request):
        logger.info('Verify client posted data')     

        if 'issuer' in request.data:
            for key in issuer_scope:
                if not key_exist_valid(request.data['issuer'], key, issuer_scope[key]):
                    return Response(data={'error': 'Keys or value are wrong'}, 
                                    status=status.HTTP_400_BAD_REQUEST)
        else:    
            return Response(data={'error': 'Keys or value are wrong'}, 
                            status=status.HTTP_400_BAD_REQUEST)

        if 'basic_information' in request.data:
            for key in basic_information_scope:
                if not key_exist_valid(request.data['basic_information'], key, 
                                       basic_information_scope[key]):
                    return Response(data={'error': 'Keys or value are wrong'}, 
                                    status=status.HTTP_400_BAD_REQUEST)
        else:    
            return Response(data={'error': 'Keys or value are wrong'}, 
                                  status=status.HTTP_400_BAD_REQUEST)                               

        if 'key' in request.data:
            for key in key_scope:
                if not key_exist_valid(request.data['key'], key, key_scope[key]):
                    return Response(data={'error': 'Keys or value are wrong'}, 
                                    status=status.HTTP_400_BAD_REQUEST)
        else:    
            return Response(data={'error': 'Keys or value are wrong'}, 
                            status=status.HTTP_400_BAD_REQUEST)          

        if 'extensions' in request.data:
            if 'alias_names' in request.data['extensions']:
                for alias_name in request.data['extensions']['alias_names']:
                    logger.debug('Be verifing alias_name {}'.format(alias_name))
                    if not validate_fqdn_or_ipv46_address(alias_name['value']):
                        return Response(data={'error': 'Keys or value are wrong'}, 
                                        status=status.HTTP_400_BAD_REQUEST)    

            if 'key_usages' in request.data['extensions']:
                for key_usage in request.data['extensions']['key_usages']:
                    logger.debug('Be verifing alias_name {}'.format(key_usage))
                    if key_usage not in extensions_scope['key_usages']:
                        return Response(data={'error': 'Keys or value are wrong'}, 
                                        status=status.HTTP_400_BAD_REQUEST)                                   
      
            if 'extneded_key_usages' in request.data['extensions']:
                for extneded_key_usage in request.data['extensions']['extneded_key_usages']:
                    logger.debug('Be verifing alias_name {}'.format(key_usage))
                    if extneded_key_usage not in extensions_scope['extneded_key_usages']:
                        return Response(data={'error': 'Keys or value are wrong'}, 
                                        status=status.HTTP_400_BAD_REQUEST)   

        return post(self, request)

    return inner

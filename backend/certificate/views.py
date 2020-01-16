from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.renderers import JSONRenderer, BaseRenderer
from certificate.x509 import ReadRequest, ReadCertificate
from certificate.x509 import SignCertificate, MakeCertificate
from django.core import files
from .verifier import verifier_log
import logging


logger = logging.getLogger('django.certificate')


class CertificateParsing(APIView):
    parser_classes = [MultiPartParser]
    renderer_classes = [JSONRenderer]

    @verifier_log
    def post(self, request):
        obj_bytes = b''

        try:
            for chunk in request.data.dict().get('obj').chunks():
                obj_bytes += chunk

        except AttributeError as e:
            logger.error(e)
            return Response(data={'error': 'Request or certificate is empty'}, 
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            if request.data.dict().get('type') == 'crt':
                obj = ReadCertificate({
                    'crt_bytes': obj_bytes, 
                    'crt_codec': request.data.dict().get('codec')
                })
                res = obj.certificate(data_type='string')

            elif request.data.dict().get('type') == 'req':
                obj = ReadRequest({
                    'req_bytes': obj_bytes, 
                    'req_codec': request.data.dict().get('codec')
                })  
                res =  obj.request(data_type='string')

        except ValueError as e:
            logger.error(e)
            return Response(data={'error': 'Request or certificate is invalid'}, status=status.HTTP_400_BAD_REQUEST)
                            
        else:
            return Response(data=res, status=status.HTTP_200_OK)


class PEMRenderer(BaseRenderer):
    media_type = 'text/plain'
    format = 'pem'
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        return data


class CertificateSigning(APIView):
    parser_classes = [MultiPartParser]
    renderer_classes = [PEMRenderer]

    @verifier_log
    def post(self, request):
        req_bytes = b''

        try:
            for chunk in request.data.dict().get('req').chunks():
                req_bytes += chunk    
                    
        except AttributeError as e:
            logger.error(e)
            return Response(data='Request  is empty', 
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            crt = SignCertificate({
                    'ca': request.data.dict().get('ca'),
                    'valid_year': request.data.dict().get('valid_year'),
                    'hash_alg': request.data.dict().get('hash_alg'),
                    'is_ca': request.data.dict().get('is_ca')
                },
                {
                    'req_bytes': req_bytes, 
                    'req_codec': request.data.dict().get('req_codec'),
                },)

        except ValueError as e:
            logger.error(e)
            return Response(data='Request is invalid', 
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=crt.certificate(data_type='bytes'), 
                            status=status.HTTP_200_OK)


class CertificateMaking(APIView):
    parser_classes = [JSONParser]
    renderer_classes = [PEMRenderer]  

    @verifier_log
    def post(self, request):
        try:
            crt = MakeCertificate(request.data['issuer'], request.data['basic_information'], 
                                  request.data['extensions'], request.data['key'])
        
        except ValueError as e:
            logger.error(e)
            return Response(data=e, status=status.HTTP_400_BAD_REQUEST)     

        else:       
            res = crt.certificate(data_type='bytes') + crt.private_key(data_type='bytes')
            return Response(data=res, status=status.HTTP_200_OK)

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.renderers import JSONRenderer, BaseRenderer
from certificate.x509 import ReadRequest, ReadCertificate
from certificate.x509 import SignCertificate, MakeCertificate
from django.core import files
from .verifier import verifier_crt, verifier_crt_sign, verifier_crt_make, verifier_log
import logging


logger = logging.getLogger('django.certificate')


class CertificateParsing(APIView):
    parser_classes = [MultiPartParser]
    renderer_classes = [JSONRenderer]

    @verifier_log
    @verifier_crt
    def post(self, request):
        obj_bytes = b''

        for chunk in request.data.dict().get('obj').chunks():
            obj_bytes += chunk

        try:
            if request.data.dict().get('type') == 'crt':
                obj = ReadCertificate({
                    'crt_bytes': obj_bytes, 
                    'crt_codec': request.data.dict().get('codec')
                })
                res = obj.certificate(is_object=False)

            elif request.data.dict().get('type') == 'req':
                obj = ReadRequest({
                    'req_bytes': obj_bytes, 
                    'req_codec': request.data.dict().get('codec')
                })  
                res =  obj.request(is_object=False)

        except ValueError as e:
            logger.error(e)
            return Response(data={'error': 'certificate or request content should be broken'}, 
                            status=status.HTTP_400_BAD_REQUEST)
                            
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
    @verifier_crt_sign
    def post(self, request):
        req_bytes = b''

        for chunk in request.data.dict().get('req').chunks():
            req_bytes += chunk            

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
        except:
            return Response(data={'request content should be broken'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=crt.certificate_bytes(), status=status.HTTP_200_OK)


class CertificateMaking(APIView):
    parser_classes = [JSONParser]
    renderer_classes = [PEMRenderer]  

    @verifier_log
    @verifier_crt_make
    def post(self, request):
        crt = MakeCertificate(request.data['issuer'], request.data['basic_information'], 
                              request.data['extensions'], request.data['key'])

        res = crt.certificate_bytes() + \
              b'\n-----Key Password: b"Cisco123!"-----\n\n' + \
              crt.private_key(is_object=False).encode()

        return Response(data=res, status=status.HTTP_200_OK)

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.renderers import JSONRenderer, BaseRenderer
from certificate.x509 import ReadRequest, ReadCertificate, ReadCertificateChain
from certificate.x509 import SignCertificate, MakeCertificate
from django.core import files
from django.http import FileResponse
from .verifier import verifier_log
import logging, os, time, mimetypes


logger = logging.getLogger('django.certificate')


def seconds_to_str(seconds):
    tm = time.localtime(seconds)
    return time.strftime("%Y-%m-%d %X", tm)


crt_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
    'common_static/crt/') 


class CertificateFiles(APIView):
    parser_classes = [MultiPartParser]
    renderer_classes = [JSONRenderer]  

    def get(self, request):
        crt_dict = dict()

        for parent, dirnames, filenames in os.walk(crt_dir, followlinks=True):
            del dirnames
            for filename in filenames:
                file_path = os.path.join(parent, filename)
                file_info = os.stat(file_path)
                crt_dict[filename] = {
                  'file_type': mimetypes.guess_type(file_path)[0],
                  'file_size': file_info.st_size,
                  'created_time': seconds_to_str(file_info.st_ctime),
                  'modified_time': seconds_to_str(file_info.st_mtime), 
                }
                
        return Response(data=crt_dict, status=status.HTTP_200_OK)

    def post(self, request):
        existed_crt_list = list()
        uploaded_crt_list = list()

        try:
            for file_name in request.data.dict():
                file_path = os.path.join(crt_dir, file_name)

                if os.path.exists(file_path):
                    existed_crt_list.append(file_name)

                else:
                    uploaded_crt_list.append(file_name)
                    with open(file=file_path, mode='wb') as f:
                        for chunk in request.data.dict().get(file_name).chunks():
                            f.write(chunk) 

        except (AttributeError, TypeError) as e:
            logger.error(e)
            return Response(data='File is empty', status=status.HTTP_400_BAD_REQUEST)

        else:
            if existed_crt_list:
                response = '{} have existed  {} are uploaded'.format(existed_crt_list, uploaded_crt_list)
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {'code': 200, 'status': 'success'}
                return Response(data=response, status=status.HTTP_200_OK)


class CertificateFile(APIView):
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, filename, operation, password):
        req_params = request.query_params

        if req_params['operation'] == 'sign':
            req_bytes = b''
            
            try:
                for chunk in request.data.dict().get('req').chunks():
                    req_bytes += chunk    

                crt = SignCertificate({
                        'ca': request.data.dict().get('ca'),
                        'valid_year': request.data.dict().get('valid_year'),
                        'hash_alg': request.data.dict().get('hash_alg'),
                        'is_ca': request.data.dict().get('is_ca')
                    }, {'bytes': req_bytes})

            except Exception as err:
                logger.error(err)
                return Response(data=str(err), status=status.HTTP_400_BAD_REQUEST)
          
            else:
                response = {'crt': crt.certificate(data_type='bytes')}
                return Response(data=response, status=status.HTTP_200_OK) 

        elif req_params['operation'] == 'make':
            try:
                crt = MakeCertificate(request.data['issuer'], request.data['subject'])
            
            except Exception as err:
                logger.error(err)
                return Response(data=str(err), status=status.HTTP_400_BAD_REQUEST)     

            else:   
                response = {'crt': crt.certificate(data_type='bytes'),
                            'key': crt.private_key(data_type='bytes')}    
   
                return Response(data=response, status=status.HTTP_200_OK) 
      
        else:
            return Response(data={'error': 'publish is not supported'}, status=status.HTTP_400_BAD_REQUEST)                
     

    def get(self, request, filename, operation, password):
        req_params = request.query_params
        crt_file = os.path.join(crt_dir, req_params['filename'])
        crt_type = mimetypes.guess_type(crt_file)[0]

        with open(file=crt_file, mode='rb') as f:
            crt_bytes = f.read()   

        if req_params['operation'] == 'download':
            return FileResponse(open(file=crt_file, mode='rb'), as_attachment=True)

        elif req_params['operation'] == 'parse':
            if crt_type == 'application/x-x509-ca-cert':
              crt_object = ReadCertificate({'bytes': crt_bytes})
              return Response(data=crt_object.certificate(data_type='json'), 
                              status=status.HTTP_200_OK)   

            elif crt_type == 'application/x-pkcs12':
                try:
                    crt_object =  ReadCertificateChain(
                                    {'bytes': crt_bytes, 'password': req_params['password'].encode('utf8')})
                except:
                    return Response(data={'error': 'password is invalid'}, 
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(data=crt_object.certficate_chain(data_type='json'), 
                                    status=status.HTTP_200_OK)
        
        else:
            return Response(data={'error': 'sytle is not supported'}, 
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, filename, operation, password):
        req_params = request.query_params
        crt_file = os.path.join(crt_dir, req_params['filename'])  

        try:
            if os.path.exists(crt_file):
                os.remove(crt_file)
                response = {'code': 200, 'status': 'success'}

        except TypeError as e:
            logger.error(e)
            return Response(data={'error': e}, status=status.HTTP_400_BAD_REQUEST)   

        else:
            return Response(data=response, status=status.HTTP_200_OK)

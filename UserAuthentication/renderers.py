import json

from rest_framework.renderers import JSONRenderer


class UserJsonRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):

        # # received token will be in byte token. Byte token doesn't well serialize so, we have to decode it
        # token = data.get('token', None)

        # if(token is not None and isinstance(token, bytes)):
        #     data['token'] = token.decode('utf-8')

        
        # return json.dumps({
        #     'user': data
        # })


        response = ''
        if('ErrorDetail' in str(data)):
            response = json.dumps({'errors': data})
        else:
            response = json.dumps(data)

        return response
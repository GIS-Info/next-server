from rest_framework.renderers import JSONRenderer


class APIRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        code = 0
        message = 'success'
        response = renderer_context['response']
        if response.exception:
            code = 1
            message = data['error']
            data = None
        response = {
            'code': code,
            'message': message,
            'data': data
        }

        return super(APIRenderer, self).render(response, accepted_media_type, renderer_context)

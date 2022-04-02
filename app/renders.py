from rest_framework.renderers import JSONRenderer


class SuccessAPIRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = {
            'code': 0,
            'message': 'success',
            'data': data
        }

        return super(SuccessAPIRenderer, self).render(response, accepted_media_type, renderer_context)

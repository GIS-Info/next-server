from rest_framework.renderers import JSONRenderer
class APIRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        error_msg = data.get('detail', None)
        if error_msg:
            response = {
                'code': 1,
                'message': error_msg.code,
                'data': ""
            }
        else:
            response = {
                'code': 0,
                'message': 'success',
                'data': data
            }

        return super(APIRenderer, self).render(response, accepted_media_type, renderer_context)

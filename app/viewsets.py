from rest_framework.viewsets import ModelViewSet

from app.response import SuccessResponse


class ModelViewSetWithCustomResponse(ModelViewSet):
    def create(self, request, *args, **kwargs):
        response = super(ModelViewSetWithCustomResponse, self).create(request, *args, **kwargs)
        return SuccessResponse.wrap_response(response)

    def retrieve(self, request, *args, **kwargs):
        response = super(ModelViewSetWithCustomResponse, self).retrieve(request, *args, **kwargs)
        return SuccessResponse.wrap_response(response)

    def update(self, request, *args, **kwargs):
        response = super(ModelViewSetWithCustomResponse, self).update(request, *args, **kwargs)
        return SuccessResponse.wrap_response(response)

    def destroy(self, request, *args, **kwargs):
        response = super(ModelViewSetWithCustomResponse, self).destroy(request, *args, **kwargs)
        return SuccessResponse.wrap_response(response)

    def list(self, request, *args, **kwargs):
        response = super(ModelViewSetWithCustomResponse, self).list(request, *args, **kwargs)
        return SuccessResponse.wrap_response(response)
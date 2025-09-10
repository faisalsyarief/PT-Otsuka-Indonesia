from rest_framework.renderers import JSONRenderer


class StandardizedJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response') if renderer_context else None
        status_code = response.status_code if response else 200

        if isinstance(data, dict) and "rc" in data and "message" in data:
            return super().render(data, accepted_media_type, renderer_context)

        message = "Success" if 200 <= status_code < 300 else "Error"
        wrapped = {
            "rc": status_code,
            "message": message,
            "data": data
        }

        return super().render(wrapped, accepted_media_type, renderer_context)
from rest_framework.serializers import ValidationError


class UrlValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        obj = dict(value).get(self.field)
        if 'youtube.com' not in obj:
            raise ValidationError('Only urls from YouTube allowed')

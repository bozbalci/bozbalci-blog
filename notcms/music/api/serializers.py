from rest_framework import serializers


class LastfmTrackSerializer(serializers.Serializer):
    artist = serializers.CharField()
    title = serializers.CharField()
    lastfm_url = serializers.URLField()
    image_url = serializers.URLField(allow_null=True)
    scrobbled_at = serializers.DateTimeField(allow_null=True)
    now_playing = serializers.BooleanField()

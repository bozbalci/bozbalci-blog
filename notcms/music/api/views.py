from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from notcms.music.api.serializers import LastfmTrackSerializer
from notcms.music.lastfm import lastfm_api


class GetLastPlayedTrackView(APIView):
    def get(self, request):
        track = lastfm_api.get_last_played()
        if not track:
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = LastfmTrackSerializer(track)
        return Response(serializer.data)

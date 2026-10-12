from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .models import VideoAnalysis
from .serializers import VideoAnalysisSerializer


class VideoUploadAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = VideoAnalysisSerializer(
            data=request.data
        )

        if serializer.is_valid():
            analysis = serializer.save()

            return Response(
                {
                    "message": "Video uploaded successfully.",
                    "analysis": VideoAnalysisSerializer(
                        analysis
                    ).data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class VideoResultAPIView(APIView):

    def get(self, request, pk):
        try:
            analysis = VideoAnalysis.objects.get(pk=pk)
        except VideoAnalysis.DoesNotExist:
            return Response(
                {"error": "Analysis not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = VideoAnalysisSerializer(analysis)

        return Response(serializer.data)
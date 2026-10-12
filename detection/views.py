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


from rest_framework.views import APIView
from rest_framework.response import Response

from .models import VideoAnalysis
from .serializers import VideoAnalysisSerializer


class VideoHistoryAPIView(APIView):

    def get(self, request):
        analyses = VideoAnalysis.objects.all().order_by("-created_at")

        serializer = VideoAnalysisSerializer(
            analyses,
            many=True
        )

        return Response({
            "count": analyses.count(),
            "results": serializer.data
        })


from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import VideoAnalysis
from .serializers import VideoAnalysisSerializer


class StartAnalysisAPIView(APIView):

    def post(self, request, pk):
        try:
            analysis = VideoAnalysis.objects.get(pk=pk)
        except VideoAnalysis.DoesNotExist:
            return Response(
                {"error": "Video analysis not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if analysis.status in ["processing", "completed"]:
            return Response(
                {
                    "message": (
                        f"Analysis is already {analysis.status}."
                    )
                },
                status=status.HTTP_409_CONFLICT,
            )

        analysis.status = "processing"
        analysis.error_message = ""
        analysis.save(
            update_fields=["status", "error_message"]
        )

        return Response(
            {
                "message": "Analysis started.",
                "analysis": VideoAnalysisSerializer(
                    analysis
                ).data,
            },
            status=status.HTTP_200_OK,
        )


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import VideoAnalysis


@api_view(["POST"])
def save_detection_result(request, pk):
    try:
        analysis = VideoAnalysis.objects.get(pk=pk)
    except VideoAnalysis.DoesNotExist:
        return Response(
            {"error": "Analysis not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    result = request.data.get("result")
    confidence = request.data.get("confidence")

    if result not in ["real", "deepfake", "inconclusive"]:
        return Response(
            {"error": "Invalid detection result."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if confidence is None:
        return Response(
            {"error": "Confidence is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        confidence = float(confidence)
    except (TypeError, ValueError):
        return Response(
            {"error": "Confidence must be a number."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not 0 <= confidence <= 1:
        return Response(
            {"error": "Confidence must be between 0 and 1."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    analysis.result = result
    analysis.confidence = confidence
    analysis.status = "completed"
    analysis.error_message = ""

    analysis.save()

    return Response({
        "message": "Detection result saved successfully.",
        "id": analysis.id,
        "status": analysis.status,
        "result": analysis.result,
        "confidence": analysis.confidence,
    })
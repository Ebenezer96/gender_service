from datetime import datetime, timezone

import requests
from requests.exceptions import RequestException
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ClassifyNameView(APIView):
    def get(self, request):
        name_values = request.GET.getlist("name")

        if not name_values:
            return Response(
                {"status": "error", "message": "Missing name parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(name_values) != 1:
            return Response(
                {"status": "error", "message": "name must be a string"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        name = name_values[0]

        if name is None or not isinstance(name, str):
            return Response(
                {"status": "error", "message": "name must be a string"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        name = name.strip()

        if not name:
            return Response(
                {"status": "error", "message": "Missing or empty name parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            upstream_response = requests.get(
                "https://api.genderize.io",
                params={"name": name},
                timeout=5,
            )
            upstream_response.raise_for_status()
            payload = upstream_response.json()
        except RequestException:
            return Response(
                {"status": "error", "message": "Failed to fetch data from upstream service"},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        except ValueError:
            return Response(
                {"status": "error", "message": "Invalid response from upstream service"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        gender = payload.get("gender")
        probability = payload.get("probability")
        count = payload.get("count")

        if gender is None or count == 0:
            return Response(
                {"status": "error", "message": "No prediction available for the provided name"},
                status=status.HTTP_200_OK,
            )

        try:
            probability = float(probability)
            sample_size = int(count)
        except (TypeError, ValueError):
            return Response(
                {"status": "error", "message": "Invalid response from upstream service"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        processed_at = (
            datetime.now(timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z")
        )

        is_confident = probability >= 0.7 and sample_size >= 100

        return Response(
            {
                "status": "success",
                "data": {
                    "name": name.lower(),
                    "gender": gender,
                    "probability": probability,
                    "sample_size": sample_size,
                    "is_confident": is_confident,
                    "processed_at": processed_at,
                },
            },
            status=status.HTTP_200_OK,
        )
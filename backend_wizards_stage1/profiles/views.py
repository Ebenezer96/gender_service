from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Profile
from .services import (
    fetch_gender,
    fetch_age,
    fetch_nationality,
    UpstreamAPIError,
)
from .utils import get_age_group, get_top_country


class ProfileListCreateView(APIView):
    def get(self, request):
        queryset = Profile.objects.all()

        gender = request.query_params.get("gender")
        country_id = request.query_params.get("country_id")
        age_group = request.query_params.get("age_group")

        if gender:
            queryset = queryset.filter(gender__iexact=gender)

        if country_id:
            queryset = queryset.filter(country_id__iexact=country_id)

        if age_group:
            queryset = queryset.filter(age_group__iexact=age_group)

        data = [
            {
                "id": str(profile.id),
                "name": profile.name,
                "gender": profile.gender,
                "age": profile.age,
                "age_group": profile.age_group,
                "country_id": profile.country_id,
            }
            for profile in queryset
        ]

        return Response(
            {
                "status": "success",
                "count": len(data),
                "data": data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        name = request.data.get("name")

        if name is None:
            return Response(
                {"status": "error", "message": "Missing or empty name"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not isinstance(name, str):
            return Response(
                {"status": "error", "message": "Invalid type"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        normalized_name = name.strip().lower()

        if not normalized_name:
            return Response(
                {"status": "error", "message": "Missing or empty name"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        existing_profile = Profile.objects.filter(name=normalized_name).first()

        if existing_profile:
            return Response(
                {
                    "status": "success",
                    "message": "Profile already exists",
                    "data": {
                        "id": str(existing_profile.id),
                        "name": existing_profile.name,
                        "gender": existing_profile.gender,
                        "gender_probability": existing_profile.gender_probability,
                        "sample_size": existing_profile.sample_size,
                        "age": existing_profile.age,
                        "age_group": existing_profile.age_group,
                        "country_id": existing_profile.country_id,
                        "country_probability": existing_profile.country_probability,
                        "created_at": existing_profile.created_at.isoformat().replace("+00:00", "Z"),
                    },
                },
                status=status.HTTP_200_OK,
            )

        try:
            gender_data = fetch_gender(normalized_name)
            age_data = fetch_age(normalized_name)
            nationality_data = fetch_nationality(normalized_name)

            top_country = get_top_country(nationality_data["country"])

            profile = Profile.objects.create(
                name=normalized_name,
                gender=gender_data["gender"],
                gender_probability=gender_data["probability"],
                sample_size=gender_data["count"],
                age=age_data["age"],
                age_group=get_age_group(age_data["age"]),
                country_id=top_country["country_id"],
                country_probability=top_country["probability"],
            )

            return Response(
                {
                    "status": "success",
                    "data": {
                        "id": str(profile.id),
                        "name": profile.name,
                        "gender": profile.gender,
                        "gender_probability": profile.gender_probability,
                        "sample_size": profile.sample_size,
                        "age": profile.age,
                        "age_group": profile.age_group,
                        "country_id": profile.country_id,
                        "country_probability": profile.country_probability,
                        "created_at": profile.created_at.isoformat().replace("+00:00", "Z"),
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        except UpstreamAPIError as e:
            return Response(
                {"status": "error", "message": str(e)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        except Exception:
            return Response(
                {"status": "error", "message": "Server failure"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProfileDetailView(APIView):
    def get(self, request, profile_id):
        try:
            profile = Profile.objects.get(id=profile_id)
        except Profile.DoesNotExist:
            return Response(
                {"status": "error", "message": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {
                "status": "success",
                "data": {
                    "id": str(profile.id),
                    "name": profile.name,
                    "gender": profile.gender,
                    "gender_probability": profile.gender_probability,
                    "sample_size": profile.sample_size,
                    "age": profile.age,
                    "age_group": profile.age_group,
                    "country_id": profile.country_id,
                    "country_probability": profile.country_probability,
                    "created_at": profile.created_at.isoformat().replace("+00:00", "Z"),
                },
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, profile_id):
        try:
            profile = Profile.objects.get(id=profile_id)
        except Profile.DoesNotExist:
            return Response(
                {"status": "error", "message": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
from rest_framework.views import APIView
from rest_framework.views import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Pet
from .serializers import PetSerializer
from groups.models import Group
from traits.models import Trait


class PetView(APIView, PageNumberPagination):

    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group_data = serializer.validated_data.pop("group")
        trait_data = serializer.validated_data.pop("traits")

        group_obj = Group.objects.filter(
            scientific_name__iexact=group_data["scientific_name"]
        ).first()

        if not group_obj:
            new_group = Group.objects.create(**group_data)
            new_pet = Pet.objects.create(**serializer.validated_data, group=new_group)
        else:
            new_pet = Pet.objects.create(**serializer.validated_data, group=group_obj)

        for trait_element in trait_data:
            trait_obj = Trait.objects.filter(name__iexact=trait_element["name"]).first()

            if not trait_obj:
                trait_obj = Trait.objects.create(**trait_element)
            new_pet.traits.add(trait_obj)

        serializer = PetSerializer(new_pet)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        traits_data = request.query_params.get("trait", None)

        if traits_data:
            pets = Pet.objects.filter(traits__name=traits_data)

            result_page = self.paginate_queryset(pets, request, view=self)

            serializer = PetSerializer(result_page, many=True)

            return self.get_paginated_response(serializer.data)

        pets = Pet.objects.all()

        result_page = self.paginate_queryset(pets, request, view=self)

        serializer = PetSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

class PetDetailView(APIView, PageNumberPagination):
    def get(self, request: Request, pet_id) -> Response:
        get_pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(get_pet)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request: Request, pet_id) -> Response:
        get_pet = get_object_or_404(Pet, id=pet_id)
        get_pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pet_id):
        get_pet = get_object_or_404(Pet, id=pet_id)

        serializer = PetSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        group_data = serializer.validated_data.pop("group", None)
        traits_data = serializer.validated_data.pop("traits", None)

        if group_data:
            try:
                new_group = Group.objects.get(
                scientific_name=group_data["scientific_name"]
            )
                get_pet.group = new_group

            except Group.DoesNotExist:

                add_group = Group.objects.create(**group_data)
                get_pet.group = add_group 

        if traits_data:
            get_pet.traits.clear()
        
            for traits in traits_data:
                traits_obj = Trait.objects.filter(name__iexact=traits["name"]).first()

            if not traits_obj:
                traits_obj = Trait.objects.create(**traits)

            get_pet.traits.add(traits_obj)

        [setattr(get_pet, key, value) for key, value in serializer.validated_data.items()]
        
        get_pet.save()
        serializer = PetSerializer(get_pet)
        return Response(serializer.data, status.HTTP_200_OK)
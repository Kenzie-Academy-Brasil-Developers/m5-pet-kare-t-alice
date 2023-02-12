from django.shortcuts import render
from rest_framework import serializers
from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer
from pets.models import Pet, SexChoice
from groups.models import Group
from traits.models import Trait


# Create your views here.
class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=SexChoice.choices, default=SexChoice.DEFAULT)

    group = GroupSerializer()
    traits = TraitSerializer(many=True)

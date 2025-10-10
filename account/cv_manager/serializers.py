from rest_framework import serializers
from .models import (
    CVProfile, UserJobExperience, UserEducation, UserSoftSkill, 
    UserHardSkill, UserLanguage, UserHobby
)

class UserJobExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserJobExperience
        fields = ['id', 'role', 'position', 'company', 'start_date', 'end_date', 'description']

class UserEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEducation
        fields = ['id', 'title', 'institution', 'start_date', 'end_date', 'description']

class UserSoftSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name')
    class Meta:
        model = UserSoftSkill
        fields = ['id', 'skill_name']

class UserHardSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name')
    class Meta:
        model = UserHardSkill
        fields = ['id', 'skill_name']

class UserLanguageSerializer(serializers.ModelSerializer):
    language_name = serializers.CharField(source='language.name')
    class Meta:
        model = UserLanguage
        fields = ['id', 'language_name', 'level']

class UserHobbySerializer(serializers.ModelSerializer):
    hobby_name = serializers.CharField(source='hobby.name')
    class Meta:
        model = UserHobby
        fields = ['id', 'hobby_name', 'description']

class CVProfileSerializer(serializers.ModelSerializer):
    experiencias = UserJobExperienceSerializer(source='selected_experiences', many=True)
    educaciones = UserEducationSerializer(source='selected_educations', many=True)
    softskills = UserSoftSkillSerializer(source='selected_softskills', many=True)
    hardskills = UserHardSkillSerializer(source='selected_hardskills', many=True)
    idiomas = UserLanguageSerializer(source='selected_languages', many=True)
    hobbies = UserHobbySerializer(source='selected_hobbies', many=True)

    class Meta:
        model = CVProfile
        fields = [
            'id', 'title', 'slug', 'skin', 'primary_color', 'font_family',
            'header_image', 'is_public', 'experiencias', 'educaciones',
            'softskills', 'hardskills', 'idiomas', 'hobbies',
            'created_at', 'updated_at'
        ]

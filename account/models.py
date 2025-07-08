from django.db import models
<<<<<<< HEAD

# Create your models here.
=======
from django.contrib.auth.models import User

# 🔹 1. UserProfile (1-1 con User)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username


# 🔹 2. UserJobExperience (1-N con User)
class UserJobExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.position} at {self.company}"


# 🔹 3. SoftSkill + UserSoftSkill (N-M)
class SoftSkill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class UserSoftSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(SoftSkill, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.skill.name}"


# 🔹 4. Language + UserLanguage (N-M)
class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class UserLanguage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    level = models.CharField(max_length=50)  # A1, A2, B1, etc.

    def __str__(self):
        return f"{self.user.username} - {self.language.name} ({self.level})"


# 🔹 5. Hobby + UserHobby (N-M)
class Hobby(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class UserHobby(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.hobby.name}"


# 🔹 6. UserEducation (1-N con User)
class UserEducation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} at {self.institution}"


# 🔹 7. CVProfile (1-N con User)
class CVProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    include_profile = models.BooleanField(default=True)
    include_jobs = models.BooleanField(default=True)
    include_education = models.BooleanField(default=True)
    include_languages = models.BooleanField(default=True)
    include_softskills = models.BooleanField(default=True)
    include_hobbies = models.BooleanField(default=False)

    def __str__(self):
        return self.title
>>>>>>> 7a09ebf (Sesion 1-2-3)

import factory
from django.contrib.auth import get_user_model
from .models import CVProfile

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User 

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@test.com")
    password = factory.PostGenerationMethodCall('set_password', '1234')


class CVFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CVProfile  # Solo el modelo

    user = factory.SubFactory(UserFactory)
    title = factory.Faker('job')

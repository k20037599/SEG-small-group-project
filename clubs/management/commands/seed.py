from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from clubs.models import User

class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

        self.user_types = [
            'APPLICANT',
            'MEMBER',
            'OFFICER',
            'OWNER'
        ]

        self.experience_levels = [
            'BEGINNER',
            'INTERMEDIATE',
            'ADVANCED'
        ]

    def handle(self, *args, **options):
        for i in range(200): # creates 200 Members
            User.objects.create_user(
                username = self.faker.unique.user_name(),
                first_name = self.faker.first_name(),
                last_name = self.faker.last_name(),
                email = self.faker.unique.safe_email(),
                bio = self.faker.word(),
                personal_statement = self.faker.word(),
                experience_level = self.faker.word(ext_word_list=self.experience_levels),
                user_type = 'MEMBER',
                password = 'Password123'
            )
        for i in range(40): # creates 40 applicants
            User.objects.create_user(
                username = self.faker.unique.user_name(),
                first_name = self.faker.first_name(),
                last_name = self.faker.last_name(),
                email = self.faker.unique.safe_email(),
                bio = self.faker.word(),
                personal_statement = self.faker.word(),
                experience_level = self.faker.word(ext_word_list=self.experience_levels),
                user_type = 'APPLICANT',
                password = 'Password123'
            )
        for i in range(20): # creates 20 officers
            User.objects.create_user(
                username = self.faker.unique.user_name(),
                first_name = self.faker.first_name(),
                last_name = self.faker.last_name(),
                email = self.faker.unique.safe_email(),
                bio = self.faker.word(),
                personal_statement = self.faker.word(),
                experience_level = self.faker.word(ext_word_list=self.experience_levels),
                user_type = 'OFFICER',
                password = 'Password123'
            )

        # creates 1 owner

        # creates the users specified in the requirements
        User.objects.create_user(
            username = 'jebKerman',
            first_name = 'Jebediah',
            last_name = 'Kerman',
            email = 'jeb@example.org',
            bio = self.faker.word(),
            personal_statement = self.faker.word(),
            experience_level = 'ADVANCED',
            user_type = 'MEMBER',
            password = 'Password123'
        )

        User.objects.create_user(
            username = 'valKerman',
            first_name = 'Valentina',
            last_name = 'Kerman',
            email = 'val@example.org',
            bio = self.faker.word(),
            personal_statement = self.faker.word(),
            experience_level = 'ADVANCED',
            user_type = 'OFFICER',
            password = 'Password123'
        )

        User.objects.create_user(
            username = 'bilKerman',
            first_name = 'Billie',
            last_name = 'Kerman',
            email = 'billie@example.org',
            bio = self.faker.word(),
            personal_statement = self.faker.word(),
            experience_level = 'ADVANCED',
            user_type = 'OWNER',
            password = 'Password123'
        )

from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from clubs.models import User

class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

        self.experience_levels = [
            'BEGINNER',
            'INTERMEDIATE',
            'ADVANCED'
        ]

        # List of existing user types:
        #   -APPLICANT
        #   -MEMBER
        #   -OFFICER
        #   -OWNER

    def handle(self, *args, **options):
        # creates 200 Members
        for i in range(200):
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
        # creates 40 applicants
        for i in range(40):
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
                application_status = 'PENDING'
            )
        # creates 20 officers
        for i in range(20):
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

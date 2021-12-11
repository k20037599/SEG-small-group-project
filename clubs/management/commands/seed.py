from django.core.management.base import BaseCommand, CommandError

from faker import Faker

from clubs.models import User

class Command(BaseCommand):
    APPLICANT_COUNT = 20
    MEMBER_COUNT = 80
    OFFICER_COUNT = 20
    DEFAULT_PASSWORD = 'Password123'

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

        # List of existing user types: APPLICANT, MEMBER, OFFICER, OWNER

        # List of potential experience levels
        self.experience_levels = [
            'BEGINNER',
            'INTERMEDIATE',
            'ADVANCED'
        ]

    def handle(self, *args, **options):
        self.create_specific_users()
        self.create_applicants()
        self.create_members()
        self.create_officers()

    # creates multiple applicants based on APPLICANT_COUNT
    def create_applicants(self):
        applicant_count = 0

        while applicant_count < self.APPLICANT_COUNT:
            print(f'Seeding applicant {applicant_count+1}/{self.APPLICANT_COUNT}.', end = '\r')
            self.create_applicant()
            applicant_count += 1

        print('Applicants successfully seeded.')

    # creates a single applicant
    def create_applicant(self):
        User.objects.create_user(
            username = self.faker.unique.user_name(),
            first_name = self.faker.first_name(),
            last_name = self.faker.last_name(),
            email = self.faker.unique.safe_email(),
            bio = self.faker.word(),
            personal_statement = self.faker.word(),
            experience_level = self.faker.word(ext_word_list=self.experience_levels),
            user_type = 'APPLICANT',
            password = Command.DEFAULT_PASSWORD,
            application_status = 'PENDING'
        )

    # creates multiple members based on MEMBER_COUNT
    def create_members(self):
        member_count = 0

        while member_count < self.MEMBER_COUNT:
            print(f'Seeding member {member_count+1}/{self.MEMBER_COUNT}.', end = '\r')
            self.create_member()
            member_count += 1

        print('Members successfully seeded.')

    # creates a single member
    def create_member(self):
        User.objects.create_user(
            username = self.faker.unique.user_name(),
            first_name = self.faker.first_name(),
            last_name = self.faker.last_name(),
            email = self.faker.unique.safe_email(),
            bio = self.faker.word(),
            personal_statement = self.faker.word(),
            experience_level = self.faker.word(ext_word_list=self.experience_levels),
            user_type = 'MEMBER',
            password = Command.DEFAULT_PASSWORD
        )

    # creates multiple officers based on OFFICER_COUNT
    def create_officers(self):
        officer_count = 0

        while officer_count < self.OFFICER_COUNT:
            print(f'Seeding officer {officer_count+1}/{self.OFFICER_COUNT}.', end = '\r')
            self.create_officer()
            officer_count += 1

        print('Officers successfully seeded.')

    # creates a single officer
    def create_officer(self):
        User.objects.create_user(
            username = self.faker.unique.user_name(),
            first_name = self.faker.first_name(),
            last_name = self.faker.last_name(),
            email = self.faker.unique.safe_email(),
            bio = self.faker.word(),
            personal_statement = self.faker.word(),
            experience_level = self.faker.word(ext_word_list=self.experience_levels),
            user_type = 'OFFICER',
            password = Command.DEFAULT_PASSWORD
        )

    # creates the users specified in the requirements
    def create_specific_users(self):
        print('Jebediah Kerman successfully seeded.')
        User.objects.create_user(
            username = 'jebKerman',
            first_name = 'Jebediah',
            last_name = 'Kerman',
            email = 'jeb@example.org',
            bio = self.faker.word(),
            personal_statement = self.faker.word(),
            experience_level = 'ADVANCED',
            user_type = 'MEMBER',
            password = self.DEFAULT_PASSWORD
        )

        print('Valentina Kerman successfully seeded.')
        User.objects.create_user(
            username = 'valKerman',
            first_name = 'Valentina',
            last_name = 'Kerman',
            email = 'val@example.org',
            bio = self.faker.word(),
            personal_statement = self.faker.word(),
            experience_level = 'ADVANCED',
            user_type = 'OFFICER',
            password = self.DEFAULT_PASSWORD
        )

        print('Billie Kerman successfully seeded.')
        User.objects.create_user(
            username = 'bilKerman',
            first_name = 'Billie',
            last_name = 'Kerman',
            email = 'billie@example.org',
            bio = self.faker.word(),
            personal_statement = self.faker.word(),
            experience_level = 'ADVANCED',
            user_type = 'OWNER',
            password = self.DEFAULT_PASSWORD
        )

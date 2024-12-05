from faker import Faker


# fake = Faker("en_US")


class CustomFaker(Faker):
    """Wrap Faker class to add custom methods."""

    def lorem(self, word_count: int = 2):
        """Create a string with fake words."""
        return " ".join(fake.words(word_count, unique=True))


fake = CustomFaker("en_US")

__all__ = ["fake"]

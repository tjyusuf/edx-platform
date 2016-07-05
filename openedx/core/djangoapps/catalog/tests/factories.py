"""Factories for generating fake catalog data."""
import factory
from factory.fuzzy import FuzzyText


class CourseRun(factory.Factory):
    """
    Factory for stubbing CourseRun resources from the catalog API.
    """
    class Meta(object):
        model = dict

    marketing_url = FuzzyText(prefix='https://www.example.com/marketing/')

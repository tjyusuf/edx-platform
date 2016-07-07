import logging

from django.core.management.base import BaseCommand
from py2neo import Graph, Node, Relationship, authenticate, watch
from py2neo.compat import integer, string, unicode
from request_cache.middleware import RequestCache
from xmodule.modulestore.django import modulestore
from xmodule.partitions.partitions import UserPartition

log = logging.getLogger(__name__)

class ModuleStoreSerializer(object):
    """
    Class with functionality to serialize a modulestore to CSVs:
    Each csv will have information about one kind of xblock.
    There will also be a "relationships" csv with information about
    which xblocks are children of each other.
    """
    def __init__(self):
        self.all_courses = modulestore().get_course_summaries()



    def serialize_item(self, item, course_key):
        """
        Args:
            item: an XBlock
            course_key: the course key of the course the item is in

        Returns:
            fields: a dictionary of an XBlock's field names and values
            block_type: the name of the XBlock's type (i.e. 'course'
            or 'problem')
        """
        # convert all fields to a dict and filter out parent and children field
        fields = dict(
            (field, field_value.read_from(item))
            for (field, field_value) in item.fields.iteritems()
            if field not in ['parent', 'children']
        )

        fields['edited_on'] = unicode(getattr(item, 'edited_on', u''))
        fields['display_name'] = item.display_name_with_default

        fields['location:ID'] = unicode(item.location)
        if "location" in fields:
            del fields['location']

        block_type = item.scope_ids.block_type

        fields['type'] = block_type

        label = fields['type']
        del fields['type']

        if 'checklists' in fields:
            del fields['checklists']

        fields['org'] = course_key.org
        fields['course'] = course_key.course
        fields['run'] = course_key.run
        fields['course_key'] = unicode(course_key)

        return fields, label


class Command(BaseCommand):


    def handle(self, *args, **options):

        mss = ModuleStoreSerializer()

        ACCEPTABLE_TYPES = (integer, string, unicode, float, bool, tuple, list, set, frozenset)

        graph = Graph(password="edx", bolt=True)
        authenticate("localhost:7474", 'neo4j', 'edx')
        graph.delete_all()

        for course in mss.all_courses:
            print course
            location_to_node = {}
            for item in modulestore().get_items(course.id):
                fields, label = mss.serialize_item(item, course.id)

                for k, v in fields.iteritems():
                    try:
                        fields[k] = coerce_types(v, ACCEPTABLE_TYPES)
                    except TypeError:
                        import ipdb; ipdb.set_trace()
                        coerce_types(v, ACCEPTABLE_TYPES)
                        raise

                if not isinstance(label, ACCEPTABLE_TYPES):
                    label = unicode(label)
                try:
                    node = Node(label, **fields)
                except TypeError:
                    print label
                    print fields
                    raise
                location_to_node.update({item.location: node})

            tx = graph.begin()
            for item in modulestore().get_items(course.id):
                if item.has_children:
                    for child_loc in item.get_children():
                        parent_node = location_to_node.get(item.location)
                        child_node = location_to_node.get(child_loc.location)
                        if parent_node is not None and child_node is not None:
                            relationship = Relationship(parent_node, "PARENT_OF", child_node)
                            tx.create(relationship)
            tx.commit()



def coerce_types(value, acceptable_types):
    if isinstance(value, (tuple, list, set, frozenset)) and not isinstance(value, UserPartition):
        for index, element in enumerate(value):
            value[index] = unicode(element)

    elif not isinstance(value, acceptable_types) or isinstance(value, UserPartition):
        value = unicode(value)

    return value
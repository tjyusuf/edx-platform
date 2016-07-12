"""
Milestones Transformer
"""

from django.conf import settings

from edx_proctoring.api import get_attempt_status_summary
from edx_proctoring.models import ProctoredExamStudentAttemptStatus
from openedx.core.lib.block_structure.transformer import BlockStructureTransformer, FilteringTransformerMixin
from util import milestones_helpers


class MilestonesTransformer(FilteringTransformerMixin, BlockStructureTransformer):
    """
    Exclude proctored exams unless the user is not a verified student or has
    declined taking the exam.
    """
    VERSION = 1
    BLOCK_HAS_PROCTORED_EXAM = 'has_proctored_exam'

    @classmethod
    def name(cls):
        return "milestones"

    @classmethod
    def collect(cls, block_structure):
        """
        Computes any information for each XBlock that's necessary to execute
        this transformer's transform method.

        Arguments:
            block_structure (BlockStructureCollectedData)
        """
        block_structure.request_xblock_fields('is_proctored_enabled')
        block_structure.request_xblock_fields('is_practice_exam')

    def transform_block_filters(self, usage_info, block_structure):
        if not settings.FEATURES.get('ENABLE_PROCTORED_EXAMS', False):
            return [block_structure.create_universal_filter()]
        # this needs to change ^^^

        def has_milestones_for_user(block_key):
            """
            Test whether the block is a proctored exam for the user in
            question, or requires any other unfulfilled milestones.
            """
            if (
                    block_key.block_type == 'sequential' and (
                        block_structure.get_xblock_field(block_key, 'is_proctored_enabled') or
                        block_structure.get_xblock_field(block_key, 'is_practice_exam')
                    )
            ):
                # This section is an exam.  It should be excluded unless the
                # user is not a verified student or has declined taking the exam.
                user_exam_summary = get_attempt_status_summary(
                    usage_info.user.id,
                    unicode(block_key.course_key),
                    unicode(block_key),
                )
                exam_is_proctored = user_exam_summary and \
                                    user_exam_summary['status'] != ProctoredExamStudentAttemptStatus.declined

                # after checking for proctored, we check for all other milestones
                # if we need additional fields bump up version number
                milestones_exist_for_exam = bool(milestones_helpers.get_course_content_milestones(
                                                    unicode(block_key.course_key),
                                                    unicode(block_key),
                                                    'requires',
                                                    usage_info.user.id
                                                ))
                return exam_is_proctored or milestones_exist_for_exam

        return [block_structure.create_removal_filter(has_milestones_for_user)]


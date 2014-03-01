from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import re


def validate_regex(value):
    try:
        re.compile(value)
    except re.error as err:
        raise ValidationError('"{}" is not a valid regex: {}'.format(value,
                                                                     err))


def validate_question_answers(question, answer):
    if not question or not answer:
        return
    cnt = 0
    for answer in question.offeredanswer_set.all():
        if answer.answer_type == 'I':
            cnt += 1
    if answer.id is None and answer.answer_type == 'I':
        cnt += 1
    if question.question_type in ('CI', 'RI') and cnt > 1:
        raise ValidationError(_('Choice with input and multiple choice with'
                              ' input type of question cannot have more than'
                              ' one input type of answer'))

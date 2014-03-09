from __future__ import unicode_literals
from django.db import models
from tinymce.models import HTMLField
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from anonsurvey.validators import validate_regex, validate_question_answers
from collections import OrderedDict
from django.core.exceptions import ValidationError


class Survey(models.Model):
    name = models.SlugField(max_length=128, verbose_name=_('Name'))
    title = models.CharField(max_length=128, verbose_name=_('Title'))
    active = models.BooleanField(default=False, verbose_name=_('Active'))
    intro = HTMLField(blank=False, null=False, verbose_name=_('Intro text'))
    mod_datetime = models.DateTimeField(auto_now=True,
                                        verbose_name=_('Modification'
                                                       ' DateTime'))

    def question_or_group(self):
        foo = OrderedDict()
        for q in self.question_set.all():
            if not q.question_group:
                foo[(q.id, None)] = [q]
            else:
                key = (q.question_group.id, q.question_group)
                if not key in foo:
                    foo[key] = [q]
                else:
                    foo[key].append(q)
        spam = []
        for key in foo.iterkeys():
            keyval = key[1]
            spam.append((keyval, foo[key]))
        return spam

    def __unicode__(self):
        return '{}: {}'.format(self.name, self.title)

    class Meta:
        ordering = ['mod_datetime']
        verbose_name = _('Survey')
        verbose_name_plural = _('Surveys')


class QuestionGroup(models.Model):
    survey = models.ForeignKey(Survey, verbose_name=_('Survey'))
    text = models.CharField(max_length=256, verbose_name=_('Text'))

    def __unicode__(self):
        return '{}: {}'.format(self.survey, self.text)

    class Meta:
        verbose_name = _('Question Group')
        verbose_name_plural = _('Question Groups')


class Question(models.Model):
    QTYPE_INPUT = 'I'
    QTYPE_RADIO = 'R'
    QTYOE_CHECKBOX = 'C'
    QTYPE_RADIO_INPUT = 'RI'
    QTYPE_CHECKBOX_INPUT = 'CI'
    QUESTION_TYPES = (
        (QTYPE_INPUT, _('input')),
        (QTYPE_RADIO, _('choice')),
        (QTYOE_CHECKBOX, _('multiple choice')),
        (QTYPE_RADIO_INPUT, _('choice with input')),
        (QTYPE_CHECKBOX_INPUT, _('multiple choice with input')),
    )

    survey = models.ForeignKey(Survey, verbose_name=_('Survey'))
    question_group = models.ForeignKey(QuestionGroup, null=True, blank=True,
                                       verbose_name=_('Question Group'))
    question_type = models.CharField(max_length=2, choices=QUESTION_TYPES,
                                     default='I', verbose_name=_('Type'))
    text = models.CharField(max_length=256, verbose_name=_('Text'))
    requires_answer = models.BooleanField(default=True,
                                          verbose_name=_('Requires Answer'))
    sort_index = models.PositiveIntegerField(default=1,
                                             verbose_name=_('Sort By Asc'))

    def __unicode__(self):
        return '{}: {}'.format(self.survey, self.text)

    def clean(self):
        if (self.question_group and
                self.survey.id != self.question_group.survey.id):
            raise ValidationError(_('Question group should belong to'
                                    ' the same survey as this question'))

    class Meta:
        ordering = ['sort_index']
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')


class OfferedAnswer(models.Model):
    ATYPE_INPUT = 'I'
    ATYPE_CHOICE = 'C'
    ANSWER_TYPES = (
        (ATYPE_INPUT, 'input'),
        (ATYPE_CHOICE, 'choice'),
    )

    question = models.ForeignKey(Question, verbose_name=_('Question'))
    answer_type = models.CharField(max_length=1, choices=ANSWER_TYPES,
                                   default='C', verbose_name=_('Type'))
    prefix = models.CharField(max_length=128, null=True, blank=True,
                              verbose_name=_('Text Prefix'))
    text = models.CharField(max_length=128, null=True, blank=True,
                            verbose_name=_('Text'))
    sufix = models.CharField(max_length=128, null=True, blank=True,
                             verbose_name=_('Text Sufix'))
    # for choice if has value then answer is selected by default
    default = models.CharField(max_length=128, null=True, blank=True,
                               verbose_name=_('Default Value'))
    validation_format = models.CharField(max_length=256, null=True, blank=True,
                                         verbose_name=_('Validation Regex'),
                                         validators=[validate_regex])
    sort_index = models.PositiveIntegerField(default=1,
                                             verbose_name=_('Sort By Asc'))

    def __unicode__(self):
        return '{}: {}: {}: {}'.format(self.answer_type,
                                       self.prefix,
                                       self.text,
                                       self.sufix)

    def clean(self):
        validate_question_answers(self.question, self)

    class Meta:
        ordering = ['sort_index']
        verbose_name = _('Offered Answer')
        verbose_name_plural = _('Offered Answers')


class Answer(models.Model):
    client_id = models.CharField(max_length=256, verbose_name=_('Client ID'))
    datetime = models.DateTimeField(auto_now=True,
                                    verbose_name=_('DateTime'))
    answer = models.ForeignKey(OfferedAnswer, verbose_name=_('Offered Answer'))
    # entered text for inputs
    text = models.CharField(max_length=256, verbose_name=_('Entered Text'))

    def __unicode__(self):
        return '{}: {}: {}'.format(self.client_id,
                                   self.answer,
                                   self.text)

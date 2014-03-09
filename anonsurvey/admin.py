from django.contrib import admin
from anonsurvey.models import Survey, QuestionGroup, Question,\
    OfferedAnswer
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from mce_filebrowser.admin import MCEFilebrowserAdmin


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class SurveyAdmin(MCEFilebrowserAdmin):
    prepopulated_fields = {'name': ('title',)}
    fields = ('title', 'name', 'intro', 'active')
    list_display = ('name', 'title', 'active')
    search_fields = ('title', 'intro')
    list_filter = ('active',)
    inlines = [QuestionInline]


class OfferedAnswerInlineFormSet(forms.models.BaseInlineFormSet):
    def clean(self):
        super(OfferedAnswerInlineFormSet, self).clean()

        cnt = 0
        question = None
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue
            data = form.cleaned_data
            if 'answer_type' in data and data['answer_type'] == 'I':
                cnt += 1
            if not question:
                question = data['question']
        if question and question.question_type in ('CI', 'RI') and cnt > 1:
            raise ValidationError(_('Choice with input and multiple choice'
                                  ' with input type of question cannot have'
                                  ' more than one input type of answer'))


class OfferedAnswerInline(admin.StackedInline):
    model = OfferedAnswer
    formset = OfferedAnswerInlineFormSet
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    inlines = [OfferedAnswerInline]
    list_display = ('survey', 'question_group', 'text', )
    search_fields = ('text', 'offeredanswer__prefix',
                     'offeredanswer__answer_type',
                     'offeredanswer__text',
                     'offeredanswer__sufix',)
    list_filter = ('question_type', 'requires_answer', )


class QuestionGroupAdmin(admin.ModelAdmin):
    list_display = ('survey', 'text', )
    search_fields = ('text', )
    inlines = [QuestionInline]


class OfferedAnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'prefix', 'text', 'sufix', 'sort_index')
    search_fields = ('question__text', 'prefix', 'text', 'sufix')
    list_filter = ('answer_type', 'question', 'question__survey')


admin.site.register(Survey, SurveyAdmin)
admin.site.register(QuestionGroup, QuestionGroupAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(OfferedAnswer, OfferedAnswerAdmin)

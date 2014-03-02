==========
Anonsurvey
==========

Anonsurvey is a Django app to create Web-based anonymous surveys.

Quick start
-----------

1. Add "anonsurvey" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'polls',
      )

   Anonsurvey admin also depends on:
    'tinymce',
    'sorl.thumbnail',
    'mce_filebrowser',

2. Include the anonsurvey URLconf in your project urls.py like this::

      url(r'^survey/', include('anonsurvey.urls')),

3. Run `python manage.py syncdb` to create the anonsurvey models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a survey (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/survey/ to list surveys.


Creating survey
---------------
First you enter survey main data:

    * title
    * name (which is a slug initialy created from title)
    * introduction text
    * active state (False by default).

Then you can enter question. For each question you can enter the
question group the question belongs to. Question group is optinal.
Question data are:

    * survey the question belongs to
    * optional question group
    * type of the question:
        - input - input type text
        - choice - input type radio group
        - multiple choice - input type checkboxes
        - choice with input - input type radio group with one radio 
          input with type text
        - multiple choice with input - input type checkboxes with one
          checkbox with input type text
    * text of the question
    * requires answer
    * sort index - questions are sorted by this number ascending.

Question group contains of the survey it belongs to and question group
text.

For each question you define answer or multiple offered answers.
Answer data are:

    * type - input or choice - it is relevant only for choice with 
      input and multiple choice with input question types
    * text prefix - displayed before input field of input type answer
    * text - displayed for choice type of answer
    * text sufix - displayed after input field of input type answer
    * default value - for input type of answer
    * validation regex - for input type of answer; regex is a valid
      python regex
    * sort index - answers are sorted by this number ascending.

Depending on survey definition survey questions and offered answers are
rendered differently.

First, survey title and intro text are displayed.
Then questions are rendered in ordering depending on sort index value.
If question belongs to question group then group's title is displayed.
Then each quesiton for group is rendered inside that group.
If question belongs to none group then its alone is rendered.
For each question its text is displayed.
Under the question answers are rendered in ordering defined by sort
index value.
If question type is input then input field is rendered.
Before input field text prefix is displayed. After input field text
sufix is displayed. If default value is defined that value is rendered
inside input field.
If question type is choice then offered answers are displayed as
radio group. Each radio is one offered answer and its text is displayed.
If question type is multiple choice then offered answers are displayed
as checkbox. Each checkbox is one offered answer and its text is
displayed.
If quesiton type is choice with input or multiple choice with input
then each answer is displayed as above for choice or multiple choice
type of question. Here answer's answer type is relevant. If type is
input then its radio or checkbox contains of input field which is
rendered the same as for input type of question.

When submiting completed survey validations are performed:

    * if question requires answer then answer must be suplied
    * if answer type is input and validation regex is supplied
      then answer value must match defined regex (note that
      regex is prefixed and sufixe with ^ and $ so that whole string
      match is checked).

Submitted answers data are:

    * client_id - in the format <current_timestamp>@<remote_ip>
      (by this value you can group answers to one client that
      completed the survey)
    * datetime - current timestamp answer is saved
    * answer - foreign key to offered answer that is input/selected
    * text - input value for input type of offered answer.

Within package there are simplest templates you can use to make your
own.
For survey display 
{% include "anonsurvey/survey_form.thml" with survey=survey %} is used.
This template provides a way for rendering the survey form depending
on survey definition. You can use it as is or you can use it as a
template for constructing yours.

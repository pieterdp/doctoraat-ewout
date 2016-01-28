from flask.ext.wtf import Form
from wtforms import SubmitField, SelectMultipleField, widgets


class MultiCheckBoxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class InitForm(Form):
    submit = SubmitField('Confirm init')


class MatchForm(Form):
    matches = MultiCheckBoxField('Match', coerce=int)
    submit = SubmitField('Submit')

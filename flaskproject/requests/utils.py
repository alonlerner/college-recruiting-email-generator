from wtforms import widgets, SelectMultipleField

default_subject='[my first name] [my last name] - Prospective Student-Athlete'

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()
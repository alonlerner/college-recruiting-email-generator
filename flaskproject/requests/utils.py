from wtforms import widgets, SelectMultipleField

default_subject='XXX XXX - Prospective Student-Athlete'

default_content='''Hello Coach [coach-last-name],

My name is XXX XXX and I am a swimmer from XXX. My SAT score is XXX. Please recruit me!'''

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()
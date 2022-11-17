from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, DateTimeField, TextAreaField
from datetime import datetime
from wtforms.validators import DataRequired


class EditButtonForm(FlaskForm):
    hidden_id = HiddenField("You haven't filled this yet!")
    edit_button = SubmitField("Edit note")
    delete_button = SubmitField("Delete note")


class SubmitForm(FlaskForm):
    hidden_id = HiddenField()
    text_field = TextAreaField(render_kw={"placeholder": "Enter your text of note here"},
                               validators=[DataRequired()])
    tags_field = StringField(render_kw={"placeholder": "Divide tags with ;"})
    date_field = DateTimeField(render_kw={"placeholder": "YYYY-MM-DD HH:MM:SS"},
                               validators=[DataRequired()])
    submit_form_button = SubmitField("Redact note")


class CreateButtonForm(FlaskForm):
    create_form_button = SubmitField("Create new note")


class FilterButtonForm(FlaskForm):
    filter_notes_button = SubmitField("Filter your notes")


class ResetFilterForm(FlaskForm):
    reset_filtering_button = SubmitField("Delete all filters")


class FilterForm(FlaskForm):
    tags_field = StringField(render_kw={"placeholder": "Divide tags with ;"})
    start_date = DateTimeField(render_kw={"placeholder": "start date: YYYY-MM-DD HH:MM:SS",
                                          "style": "width: 250px"})
    end_date = DateTimeField(render_kw={"placeholder": "end date: YYYY-MM-DD HH:MM:SS",
                                        "style": "width: 250px"})
    filter_button = SubmitField("Filter your notes")


def get_forms(entries):
    sorted_by_date_entries =\
        {k: v for k, v in sorted(entries.items(), key=lambda item: item[1]["date"], reverse=True)}
    ids = list(sorted_by_date_entries.keys())
    entries_by_id = [sorted_by_date_entries[i] for i in ids]
    forms_by_id = [EditButtonForm(prefix=i) for i in ids]
    create_button_form = CreateButtonForm()
    filter_notes_button_form = FilterButtonForm()
    reset_filtering_button_form = ResetFilterForm()
    for i, form in enumerate(forms_by_id):
        form.hidden_id.data = ids[i]
    return entries_by_id, forms_by_id,\
        create_button_form, filter_notes_button_form, reset_filtering_button_form


def get_submit_form(id_of_entry=None, entry=None):
    form = SubmitForm()
    if entry is None:
        form.date_field.data = datetime.now()
        form.tags_field.description = "Divide tags with ;. For example tag1; tag2"
        form.hidden_id.data = -1
    else:
        form.hidden_id.data = id_of_entry
        form.text_field.data = entry["text"]
        form.tags_field.data = "; ".join(entry["tags"])
        form.date_field.data = entry["date"]
    return form

#def generate_edit_form(entry):
#
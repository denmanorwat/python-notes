from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from forms import forms
from forms import entry_manager
from Instruction_hierarchy import SingleNoteInstruction
from server_communication import RemoteDB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'


@app.route("/", methods=["GET", "POST"])
def start():
    remote_DB = RemoteDB("172.17.0.1", 65432) #"172.17.0.1"
    entries = remote_DB.get_all_items()
    entries_by_id, forms_by_id,\
        create_button, filter_button, reset_button = forms.get_forms(entries)
    filtration_tags, interval = entry_manager.get_tags_and_dates()

    if request.method == "POST":
        if create_button.create_form_button.data:
            return redirect((url_for('form')))
        if filter_button.filter_notes_button.data:
            return redirect((url_for('filter')))
        if reset_button.reset_filtering_button.data:
            entry_manager.pop_tags_and_dates()
        for form in forms_by_id:
            pushed_edit = form.edit_button.data
            pushed_delete = form.delete_button.data
            id_of_entry = form.hidden_id.data
            if pushed_edit:
                entry_manager.save_entry(id=id_of_entry, entry=entries[id_of_entry])
                return redirect((url_for('form')))
            if pushed_delete:
                delete_instruction = SingleNoteInstruction("DELETE", id=id_of_entry)
                remote_DB.send_instruction(delete_instruction)
                print("DELETE", id_of_entry)

        # post/redirect/get pattern. More info at:
        # https://en.wikipedia.org/wiki/Post/Redirect/Get
        return redirect(url_for('start'))

    return render_template('list_elements.html', title='Записки',
                           len_entries=len(entries),
                           forms=forms_by_id, entries=entries_by_id,
                           create_button=create_button, filter_button=filter_button,
                           reset_button=reset_button,
                           filtration_tags=filtration_tags, interval=interval)


@app.route("/form", methods=["GET", "POST"])
def form():
    remote_DB = RemoteDB("172.17.0.1", 65432) #"172.17.0.1"
    id, entry = entry_manager.get_entry_if_exists()
    print("Id: {}".format(id))
    print("Entry: {}".format(entry))
    if request.method == "GET":
        submit_form = forms.get_submit_form(id, entry)
    else:
        submit_form = forms.SubmitForm()
    if submit_form.validate_on_submit() and submit_form.submit_form_button.data:
        entry_manager.pop_entry_if_exists()
        id_of_note = submit_form.hidden_id.data
        text = submit_form.text_field.data
        tags = submit_form.tags_field.data.replace(" ", "").split(";")
        tags = tags[:-1] if tags[-1] == '' else tags
        datetime = submit_form.date_field.data
        print(type(datetime))
        query_word = "CREATE" if id_of_note == "-1" else "EDIT"
        edit_or_create_instruction = SingleNoteInstruction(query_word, id=id_of_note,
                                           text=text, tags=tags, datetime=datetime)
        remote_DB.send_instruction(edit_or_create_instruction)
        return redirect(url_for('start'))
    elif len(submit_form.errors) > 0:
        flash(list(submit_form.errors.values())[0])
    return render_template('submit_form.html', form=submit_form)


@app.route("/filter", methods=["GET", "POST"])
def filter():
    filter_form = forms.FilterForm()
    filter_form.validate_on_submit()
    if filter_form.filter_button.data:
        print("Filter executed")
        tags = filter_form.tags_field.data.replace(" ", "").split(";")
        tags = tags[:-1] if tags[-1] == '' else tags
        start_date = filter_form.start_date.data
        end_date = filter_form.end_date.data
        if "start_date" in filter_form.errors and "end_date" in filter_form.errors:
            date_interval = None
        elif "end_date" in filter_form.errors:
            date_interval = (start_date, datetime(9999, 12, 31, 23, 59, 59))
        elif "start_date" in filter_form.errors:
            date_interval = (datetime(0, 1, 1, 0, 0, 1), end_date)
        else:
            date_interval = (start_date, end_date)
        print(tags)
        print(date_interval)
        if date_interval is not None:
            print(type(date_interval[0]))
            print(type(date_interval[1]))
        entry_manager.save_tags_and_dates(tags, date_interval)
        return redirect(url_for('start'))
    return render_template('filter_form.html', form=filter_form)

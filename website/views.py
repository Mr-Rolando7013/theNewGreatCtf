from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, send_from_directory
from flask_login import login_required, current_user
from .models import Note,File
from . import db,csrf,app
from werkzeug.utils import secure_filename
import json
import os

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')
    users_notes = Note.query.all()
    return render_template("home.html", notes=users_notes, user=current_user)


@views.route('/delete-note', methods=['POST'])
@login_required
@csrf.exempt
def delete_note(): 
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id or current_user.isAdmin:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py'}


@views.route('/documents', methods=['GET','POST'])
@login_required
def upload_file():
    if not current_user.isAdmin:
        return "You're not authorized to view this page."
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        uploaded_file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if uploaded_file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if uploaded_file and allowed_file(uploaded_file.filename):
            filename = uploaded_file.filename
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('views.uploaded_file', filename=filename))
    return render_template('documents.html', user=current_user)

@views.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('views.uploaded_files', filename=filename))

@views.route('/uploaded_files/<filename>')
def uploaded_files(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
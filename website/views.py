from flask import Blueprint , render_template , request , flash , redirect , url_for

from .models import Label , Text , LabelingInfo 

from . import db

from flask_login import login_required, current_user

import csv

import os

from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("base.html")

@views.route('/home')
def my_home():
    return render_template("base.html")


@views.route('/contact')
def contact():
    return render_template("contact.html")

@views.route('/about')
def about():
    return render_template("about.html")

@views.route('/user', methods = ['Get', 'POST'])
@login_required
def user():
    if request.method == 'POST':
        if 'submit_label' in request.form:
            label = request.form.get("label")
            new_label = Label.query.filter_by(label=label).first()
            if new_label:
                print("already exitst!")
                flash("label already exists!", category='error')
            else:
                new_label = Label(label=label)
                db.session.add(new_label)
                db.session.commit()
                print("successfully added!!")
                flash("successfully added!", category='success')
        elif 'submit_text' in request.form:
            text = request.form.get("text")
            new_text = Text.query.filter_by(context=text).first()
            if new_text:
                print("already exitst!")
                flash("label already exists!", category='error')
            else:
                new_text = Text(context=text)
                db.session.add(new_text)
                db.session.commit()
                print("successfully added!")
                flash("successfully added!", category='success')
    return render_template("user.html", user = current_user)

@views.route('/labeling/<int:item_index>', methods = ['Get', 'POST'])
@login_required
def labeling(item_index):
    if request.method == 'POST' and 'attach' in request.form:
        text_id = request.form.get("text")###
        text_instance = Text.query.get(text_id)
        label = request.form.get("label")
        new_labeling_info = LabelingInfo(label = label, user_id = current_user.id, text = text_instance.context)###3
        print(new_labeling_info)
        db.session.add(new_labeling_info)
        db.session.commit()
        next_item_index = item_index + 1
        total_text_items = len(Text.query.all())
        if next_item_index > total_text_items:
            next_item_index = 1
        return redirect(url_for('views.labeling', item_index=next_item_index))
       # current_user.labels.append(new_labeling_info)####check if it is needed
        print("successfully attached!")
        flash("successfully attached!", category="success")

    labels = Label.query.all()
    texts = Text.query.all()
    print(labels)
    print(len(texts))
    if item_index < 1 or item_index > len(texts):
        return "Item not found", 404
    text = texts[item_index - 1]
    return render_template("labeling.html", user = current_user, labels = labels, text=text, item_index=item_index, total_items=len(texts))

@views.route('/history', methods = ['Get', 'POST'])
@login_required
def history():
    if request.method == 'POST':
        label_info_id = request.form.get("label_info")
        labels = Label.query.all()
        return redirect(url_for('views.edit', iid=int(label_info_id)))
        
    labelings = current_user.labels
    labeling_info = LabelingInfo.query.all()
    texts = Text.query.all()
    return render_template("history.html", user = current_user, labeling_info = labeling_info , labelings = labelings, texts = texts)

@views.route('/edit/<int:iid>', methods=['GET', 'POST'])
@login_required
def edit(iid):
    if request.method == 'POST':
        new_label = request.form.get("label")
        labeling_info_id = request.form.get("label_info_id")
        item_to_edit = LabelingInfo.query.get(labeling_info_id)
        item_to_edit.label = new_label
        db.session.commit()
        
    labels = Label.query.all()
    return render_template("edit.html", iid = iid, labels = labels)


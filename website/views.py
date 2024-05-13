from flask import Blueprint , render_template , request , flash , redirect , url_for

from .models import Label , Text , LabelingInfo 

from . import db

from flask_login import login_required, current_user

import csv

import os

import random

from werkzeug.utils import secure_filename

from sqlalchemy import asc ###

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
    return render_template("user.html", user = current_user, button_pressed = False)################

@views.route('/labeling/<int:item_index>/<string:mode>', methods = ['Get', 'POST'])
@login_required
def labeling(item_index,mode):###
    if request.method == 'POST' and 'attach' in request.form:
        index = request.form.get("text")###
        texts = Text.query.all()
        #text_instance = Text.query.get(text_id)
        index = int(index)
        text_instance = texts[index]

        label = request.form.get("label")
        new_labeling_info = LabelingInfo(label = label, user_id = current_user.id, text = text_instance.context)###3
        print(new_labeling_info)
        db.session.add(new_labeling_info)
        db.session.commit()
            
        #texts = Text.query.all()
        #index = [text_instance.id for text in texts].index(text_id)
            
        db.session.delete(text_instance)
        db.session.commit()
            
        #least_count_text = Text.query.order_by(asc(Text.count)).first() ###
        #next_item_index = least_count_text.id ###
        return redirect(url_for('views.labeling', item_index=index+1, mode = mode)) ####+1
       # current_user.labels.append(new_labeling_info)####check if it is needed
        print("successfully attached!")
        flash("successfully attached!", category="success")

    labels = Label.query.all()
    texts = Text.query.all()
    print(labels)
    print(len(texts))
    if item_index == 0:
        item_index = random.randint(0, len(texts) - 1)
        print(item_index, "this is randommmmm")
            
    #text_list = Text.query.order_by(asc(Text.count))
    end_flag = False
    if item_index > len(texts) - 1:
        item_index = 0
    if len(texts) == 0:
        end_flag = True
    
    if end_flag == False:
        print(item_index)
        text = texts[item_index]
    print("PPPPPPPPPPPPPPPPPPPPPPPP")
    print(item_index)
    if end_flag:
        text = Text(context="all dataset is being labeled please wait for the rest of data to be uploaded.", count = 0)####
        db.session.add(text)
        db.session.commit()
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


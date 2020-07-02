from flask import Flask 
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, validators, ValidationError
from wtforms.validators import DataRequired, Length , Email


class ContactForm(FlaskForm):
    """Contact form."""
    name = StringField('Name:',[
        DataRequired()])
    email = StringField('Email:', [
        DataRequired()])

    submit = SubmitField('Sign up')
class sign(FlaskForm):
    """Contact form."""
    name = StringField('Name', [
        DataRequired()])
    email = StringField('Email', [
        DataRequired()])

    submit = SubmitField('Sign in')
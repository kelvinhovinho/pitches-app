from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField,SelectField
from wtforms.validators import Required,Email,EqualTo
from wtforms import ValidationError
from ..models import User

class updateProfile(FlaskForm):
    bio = TextAreaField('Tell us about yourself',validators = [Required()])
    submit = SubmitField('Submit')

class PitchForm(FlaskForm):
    pitch_title = StringField('Pitch title',validators=[Required()])
    pitch_category = SelectField('Pitch Category', choices = [('Select category','Select category'),('interview', 'Interview'), ('product', 'Product'),('promotion','Promotion'),('pickup','Pickup Lines')], validators=[Required()])
    pitch_comment = TextAreaField('Your Pitch')
    submit = SubmitField('Submit Pitch')

class CommentForm(FlaskForm):
    text = TextAreaField('Write a comment:',validators=[Required()])
    submit = SubmitField('Submit')        

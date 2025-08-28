from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, NumberRange, Length, Optional

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=200)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=1000)])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0.01, max=9999.99)], places=2)
    image_url = StringField('Image URL', validators=[Optional(), Length(max=500)])
    stock_quantity = IntegerField('Stock Quantity', validators=[DataRequired(), NumberRange(min=0)])
    category_id = SelectField('Category', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Save Product')

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Save Category')

class CheckoutForm(FlaskForm):
    customer_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    customer_email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    customer_phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    shipping_address = TextAreaField('Shipping Address', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Place Order')

class AddToCartForm(FlaskForm):
    product_id = HiddenField('Product ID', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1, max=100)], default=1)
    submit = SubmitField('Add to Cart')

class UpdateCartForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0, max=100)])
    submit = SubmitField('Update')

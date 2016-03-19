from flask import Blueprint, session, request
from database import registerCustomer, loginCustomer, FetchOrders, OrderPlacement, NewCourierOrder
import json
import gc
def add_routes(app=None):
  Customer = Blueprint('Customer', __name__, static_url_path='/Customer/static', static_folder='./static', template_folder='./templates')
  
  @Customer.route('/api/Customer/')
  def home():
    return 'Customer page'
  
  @Customer.route('/api/Customer/logout/')
  def logout():
    try:
      session.clear()
      gc.collect()
      return 'Logged out'
    except Exception as e:
      return str(e)
  
  @Customer.route('/api/Customer/login/', methods=['GET','POST'])
  def login():
    if request.method == 'POST':
      reply, user = loginCustomer(request.args.get('user'))
      if reply == 'Login Success':
	session['id'] = user['_id']
	session['Email'] = user['Email']
	session['user'] = 'Customer'
	user['response']='Login Successfull'
	return reply
      else:
	return reply
    return 'Invalid Request'
  
  @Customer.route('/api/Customer/signup/', methods=['GET','POST'])
  def signup():
    if request.method == 'POST':
      reply = registerCustomer(request.args.get('user'))
      return reply
    return 'Invalid Request'
  
  @Customer.route('/api/Customer/OrderPlacement/', methods=['GET','POST'])
  def Orderplacement():
    try:
      if request.method == 'POST':
	if session['user'] == 'Customer':
	  reply = OrderPlacement(request.args.get('cartItems'), session['id'])
	  return reply
	return 'User Not Logged IN'
      return 'Invalid Request'
    except Exception as e:
      return str(e)
  
  @Customer.route('/api/Customer/NewCourierOrder/', methods=['GET','POST'])
  def newCourierOrder():
    try:
      if request.method == 'POST':
	if session['user'] == 'Customer':
	  reply = NewCourierOrder(session['id'], request.args.get('order'))
	  return reply
	return 'User Not Logged IN'
      return 'Invalid Request'
    except Exception as e:
      return str(e)
      return 'Unable to Place order right now'
  
  @Customer.route('/api/Customer/FetchOrders/', methods=['GET','POST'])
  def Fetchorders():
    if request.method == 'POST':
      if session['user'] == 'Customer':
	reply = FetchOrders(session['id'])
	return reply
      return 'User Not Logged IN'
    return 'Invalid Request'
  
  app.register_blueprint(Customer)
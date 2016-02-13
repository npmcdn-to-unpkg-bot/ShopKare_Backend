from flask import Blueprint, session, request, send_from_directory
from database import loginAdmin, registerAdmin, registerProduct, removeProduct, ProductImagePath, RemoveBatch, AddBatch, addlevel1Category, removelevel1Category, addMainCategory, removeMainCategory, addSubCategory, removeSubCategory, reteriveCategories, reteriveProducts, reteriveBatches
import json, os
from werkzeug import secure_filename

def allowed_file(filename):
  return filename.rsplit('.', 1)[-1].lower() in ['png', 'jpg', 'jpeg', 'gif', 'bmp']

def add_routes(app=None):
  Admin = Blueprint('Admin', __name__, static_url_path='/Admin/static', static_folder='./static', template_folder='./templates')
  
  @Admin.route('/api/Admin')
  def home():
    try:
      return send_from_directory(os.getcwd()+'/Admin/static/', 'signup.html')
    except Exception as e:
      print str(e)
      return 'Unable to load'
  
  @Admin.route('/api/Admin/dashboard/')
  def dashboard():
    try:
      return send_from_directory(os.getcwd()+'/Admin/static/', 'products.html')
    except Exception as e:
      print str(e)
      return 'Unable to load'
  
  @Admin.route('/api/Admin/login/', methods=['GET','POST'])
  def login():
    if request.method == 'POST':
      reply, user = loginAdmin(request.args.get('user'))
      if reply == 'Login Sucess':
	session['id'] = user['_id']
	session['Email'] = user['Email']
	session['user'] = 'Admin'
	user['response']='Login Successfull'
	return json.dumps(user)
      else:
	return reply
    return 'Invalid Request'
  
  @Admin.route('/api/Admin/signup/', methods=['GET','POST'])
  def signup():
    if request.method == 'POST':
      if request.args.get('secretkey') == 'cmclogo':
	reply = registerAdmin(request.args.get('user'))
	return reply
      return 'Authentication Failed'
    return 'Invalid Request'
  
  @Admin.route('/api/Admin/addProduct/', methods=['GET','POST'])
  def addproduct():
    try:
      if request.method == 'POST':
	if session['user'] == 'Admin':
	  product = json.loads(request.args.get('product'))
	  reply = registerProduct(product['Main Category'], product['Sub Category'], request.args.get('product'))
	  return reply
	return 'Authentication Failed'
      return 'Invalid Request'
    except Exception as e:
      print str(e)
      return 'Unable to Add'
  
  @Admin.route('/api/Admin/removeProduct/', methods=['GET','POST'])
  def removeproduct():
    if request.method == 'POST':
      if session['user'] == 'Admin':
	product = json.loads(request.args.get('product'))
	del product['$$hashKey']
	reply = removeProduct(product['Main Category'], product['Sub Category'], product['_id'])
	if reply =='Registered':
	  path = ProductImagePath(product['Main Category'], product['Sub Category'], product['_id'])
	return reply
      return 'Authentication Failed'
    return 'Invalid Request'
  
  @Admin.route('/api/Admin/imageUpload/', methods=['GET','POST'])
  def imageUpload():
    if request.method == 'POST':
      if session['user'] == 'Admin':
	file = request.files['file']
	if allowed_file(file.filename):
	  product = json.loads(request.args.get('product'))
	  path = ProductImagePath(product['Main Category'], product['Sub Category'], product['_id']) 
	  if not path == 'Unable to fetch':
	    file.save(os.path.join(path, secure_filename(file.filename)))
	    return 'Image Uploaded'
	  return 'Unable to Upload'
	return 'Invalid Image format'
      return 'Authentication Failed'
    return 'Invalid Request'
  
  @Admin.route('/api/Admin/removeBatch/', methods=['GET','POST'])
  def removeBatch():
    if request.method == 'POST':
      if session['user'] == 'Admin':
	pid = request.args.get('pid')
	BatchID = request.args.get('bid')
	reply = RemoveBatch(pid, BatchID)
	return reply
      return 'Authentication Failed'
    return 'Invalid Request'
  
  @Admin.route('/api/Admin/addatch/', methods=['GET','POST'])
  def addBatch():
    if request.method == 'POST':
      if session['user'] == 'Admin':
	reply = AddBatch(request.args.get('pid'), request.args.get('Batch'))
	return reply
      return 'Authentication Failed'
    return 'Invalid Request'
  
  @Admin.route('/api/Admin/addlevel1category/', methods=['GET','POST'])
  def addlevel1category():
    try:
      if request.method == 'POST':
	if session['user'] == 'Admin':
	  reply = addlevel1Category(request.args.get('level1category'))
	  return reply
	return 'Authentication Failed'
      return 'Invalid Request'
    except Exception as e:
      print str(e)
      return 'Unable to add right now'
    
  @Admin.route('/api/Admin/removelevel1Category/', methods=['GET','POST'])
  def removelevel1category():
    if request.method == 'POST':
      if session['user'] == 'Admin':
	reply = removelevel1Category(request.args.get('level1category'))
	return reply
      return 'Authentication Failed'
    return 'Invalid Request'
  
  @Admin.route('/api/Admin/addMainCategory/', methods=['GET','POST'])
  def addmainCategory():
    if request.method == 'POST':
      if session['user'] == 'Admin':
	reply = addMainCategory(request.args.get('level1category'), request.args.get('MainCategory'))
	return reply
      return 'Authentication Failed'
    return 'Invalid Request'
  
  @Admin.route('/api/Admin/removeMainCategory/', methods=['GET','POST'])
  def removemainCategory():
    if request.method == 'POST':
      if session['user'] == 'Admin':
	reply = removeMainCategory(request.args.get('level1category'), request.args.get('MainCategory'))
	return reply
      return 'Authentication Failed'
    return 'Invalid Request'
  
  @Admin.route('/api/Admin/addSubCategory/', methods=['GET','POST'])
  def addSubcategory():
    if request.method == 'POST':
      if session['user'] == 'Admin':
	reply = addSubCategory(request.args.get('level1category'), request.args.get('MainCategory'), request.args.get('subCategory'))
	return reply
      return 'Authentication Failed'
    return 'Invalid Request'
  
  @Admin.route('/api/Admin/removeSubCategory/', methods=['GET','POST'])
  def removeSubcategory():
    if request.method == 'POST':
      if session['user'] == 'Admin':
	reply = removeSubCategory(request.args.get('level1category'), request.args.get('MainCategory'), request.args.get('subCategory'))
	return reply
      return 'Authentication Failed'
    return 'Invalid Request'
  
  @Admin.route('/api/Admin/reteriveCategories/', methods=['GET','POST'])
  def reterivecategories():
    if request.method == 'POST':
      if session['user'] == 'Admin':
	reply = reteriveCategories()
	return reply
      return 'Authentication Failed'
    return 'Invalid Request'
  
  @Admin.route('/api/admin/getProducts/', methods=['GET','POST'])
  def ReteriveProducts():
    try:
      if request.method == 'POST':
	if session['user'] == 'Admin':
	  reply = reteriveProducts(request.args.get('maincategory'), request.args.get('subcategory'))
	  return reply
	return 'Authentication Failed'
      return 'Invalid Request'
    except Exception as e:
      print str(e)
      return 'Unable to Fetch'
    
  @Admin.route('/api/Admin/reteriveBatches/', methods=['GET','POST'])
  def reterivebatches():
    try:
      if request.method == 'POST':
	if session['user'] == 'Admin':
	  reply = reteriveBatches(request.args.get('pid'))
	  return reply
	return 'Authentication Failed'
      return 'Invalid Request'
    except Exception as e:
      print str(e)
      return 'Unable to Fetch'
  
  app.register_blueprint(Admin)
import pymongo
import json
from passlib.hash import sha256_crypt
import os
import gc

base='http://www.shopkare.com/'

def MongoDBconnection(database, collection):
  connection = pymongo.MongoClient("mongodb://localhost")
  db = connection[database]
  cursor = db[collection]
  return connection, db, cursor

def registerAdmin(user):
  try:
    connection, db, collection = MongoDBconnection('Admin', 'Admin')
    user = json.loads(user)
    if collection.find({'$or':[{"Mobile":user['Mobile']},{"Email":user['Email']}]}).count():
      return 'User Already Exists'
    iter = collection.find()
    if not iter.count():
      user['_id']='A_1'
    else:
      user['_id'] = 'A_'+ str(int(iter[iter.count()-1]['_id'].split("_")[-1])+1)
    user['Password']= sha256_crypt.encrypt(str(user['Password']))
    collection.insert(user)
    connection.close()
    gc.collect()
    return 'Registration Successfull'
  except Exception as e:
    print str(e)
    return 'Unable to Register'

def loginAdmin(user):
  try:
    connection, db, collection = MongoDBconnection('Admin', 'Admin')
    user = json.loads(user)
    iter = collection.find({'$or':[{"Email":user['Email']},{"Mobile":user['Mobile']}]})
    if not iter.count():
      return "User Does't Exists", '[]'
    print iter[0]['Password']
    if sha256_crypt.verify(user['Password'],iter[0]['Password']):
      reply = iter[0]
      connection.close()
      gc.collect()
      del reply['Password']
      connection.close()
      gc.collect()
      return 'Login Sucess', reply
    else:
      connection.close()
      gc.collect()
      return 'Authentication Failed', '[]'
  except Exception as e:
    print str(e)
    return 'Unable to Login', '[]'

def registerProduct(MainCategory, SubCategory, product):
  try:
    MainCategory = MainCategory.replace(" ","_")
    SubCategory = SubCategory.replace(" ","_")
    product = json.loads(product)
    for index,val in enumerate(product['Quantity']):
      for i,val in enumerate(product['Quantity'][index]["Quantities"]):
	del product['Quantity'][index]["Quantities"][i]["$$hashKey"]
    connection, db, collection = MongoDBconnection(MainCategory, SubCategory)
    iter = collection.find()
    if not iter.count():
      product['_id']='P_'+product['_id']+'_1'
    else:
      product['_id'] = 'P_'+product['_id']+'_'+ str(int(iter[iter.count()-1]['_id'].split("_")[-1])+1)
    collection.insert(product)
    connection.close()
    gc.collect()
    return 'Registered', product['_id']
  except Exception as e:
    return str(e)
    return 'Unable to Register', '[]'

def removeProduct(MainCategory, SubCategory, pid):
  try:
    MainCategory = MainCategory.replace(" ","_")
    SubCategory = SubCategory.replace(" ","_")
    connection, db, collection = MongoDBconnection(MainCategory, SubCategory)
    iter = collection.find({"_id":pid}).count()
    if iter:
      collection.remove({"_id":pid})
      connection, db, collection = MongoDBconnection('Batches', pid)
      db.drop_collection(pid)
    else:
      return 'Unable to Remove'
    connection.close()
    gc.collect()
    return 'Removed'
  except Exception as e:
    return 'Unable to Remove'

def ProductImagePath(level1Category, MainCategory, SubCategory, pid):
  try:
    MainCategory = MainCategory.replace(" ","_")
    SubCategory = SubCategory.replace(" ","_")
    level1Category = level1Category.replace(" ","_")
    path = os.getcwd()+"/Product/static/Products/"+ level1Category + '/'+ MainCategory + "/"+ SubCategory + "/"+pid+"/"
    if not os.path.exists(path):
      os.makedirs(os.getcwd()+"/Product/static/Products/"+ level1Category + '/'+ MainCategory + "/"+ SubCategory + "/"+pid+"/")
    return os.getcwd()+"/Product/static/Products/"+ level1Category + '/'+ MainCategory + "/"+ SubCategory + "/"+pid+"/"
  except Exception as e:
    return 'Unable to fetch'

def AddBatch(pid, Batch):
  try:
    Batch = json.loads(Batch)
    connection, db, collection = MongoDBconnection('Batches', pid)
    iter = collection.find()
    if not iter.count():
      Batch['_id']='B_1'
    else:
      Batch['_id'] = 'B_'+str(int(iter[iter.count()-1]['_id'].split("_")[-1])+1)
    collection.insert(Batch)
    return "Added"
  except Exception as e:
    print str(e)
    return 'Unable to Add'

def UpdateBatch(pid, Batch):
  try:
    Batch = json.loads(Batch)
    connection, db, collection = MongoDBconnection('Batches', pid)
    collection.update({"_id":pid},Batch)
    return "Updated"
  except Exception as e:
    print str(e)
    return 'Unable to Update'

def RemoveBatch(pid, BatchID):
  try:
    connection, db, collection = MongoDBconnection('Batches', pid)
    iter = collection.find({"_id":BatchID}).count()
    if not iter:
      connection.close()
      gc.collect()
      return "Unable to Remove"
    collection.remove({"_id":BatchID})
    connection.close()
    gc.collect()
    return "Removed"
  except Exception as e:
    print str(e)
    return 'Unable to Remove'

def addlevel1Category(level1category):
  try:
    connection, db, collection = MongoDBconnection('Admin', 'Categories')
    iter = collection.find({"_id":level1category})
    if iter.count():
      return 'Category Already Exists'
    collection.insert({"_id":level1category, "Categories":[]})
    return 'Added'
  except Exception as e:
    print str(e)
    return 'Unable to Add'

def removelevel1Category(level1category):
  try:
    connection, db, collection = MongoDBconnection('Admin', 'Categories')
    collection.remove({"_id":level1category})
    connection.close()
    gc.collect()
    return 'Removed'
  except Exception as e:
    print str(e)
    return 'Unable to Remove'

def addMainCategory(level1category, MainCategory):
  try:
    connection, db, collection = MongoDBconnection('Admin', 'Categories')
    MainCategory = MainCategory[1:-1]
    collection.update({"_id":level1category},{"$addToSet":{"Categories":{MainCategory:[]}}})
    connection.close()
    gc.collect()
    return 'Added'
  except Exception as e:
    print str(e)
    return 'Unable to Add'

def removeMainCategory(level1category, MainCategory):
  try:
    connection, db, collection = MongoDBconnection('Admin', 'Categories')
    iter = collection.find({"_id":level1category})
    iter = tuple(iter)
    for item in iter:
      categories = dict(item)
    for index, category in enumerate(categories['Categories']):
      if MainCategory in category.keys():
	del categories['Categories'][index]
	collection.update({"_id":level1category},{"Categories":categories['Categories']})
	connection.close()
	gc.collect()
	return 'Removed'
    connection.close()
    gc.collect()
    return 'Removed'
  except Exception as e:
    print str(e)
    return 'Unable to Remove'

def addSubCategory(level1category, MainCategory, subCategory):
  try:
    connection, db, collection = MongoDBconnection('Admin', 'Categories')
    subCategory = subCategory[1:-1]
    iter = collection.find({"_id":level1category})
    iter = tuple(iter)
    for item in iter:
      categories = dict(item)
    for index, category in enumerate(categories['Categories']):
      if MainCategory in category.keys():
	category[MainCategory].append(subCategory)
	category = json.loads(json.dumps(category))
	categories['Categories'][index] = category
	collection.update({"_id":level1category},{"Categories":categories['Categories']})
	return 'Added'
    connection.close()
    gc.collect()
    #print iter[0]
    return 'Added'
  except Exception as e:
    print str(e)
    return 'Unable to Add'

def removeSubCategory(level1category, MainCategory, subCategory):
  try:
    connection, db, collection = MongoDBconnection('Admin', 'Categories')
    iter = collection.find({"_id":level1category})
    iter = tuple(iter)
    for item in iter:
      categories = dict(item)
    for index, category in enumerate(categories['Categories']):
      if MainCategory in category.keys() and subCategory in category[MainCategory]:
	category[MainCategory].remove(subCategory)
	collection.update({"_id":level1category},{"Categories":categories['Categories']})
	connection.close()
	gc.collect()
	return 'Removed'
    connection.close()
    gc.collect()
    return 'Removed'
  except Exception as e:
    print str(e)
    return 'Unable to Remove'

def reteriveCategories():
  try:
    connection, db, collection = MongoDBconnection('Admin', 'Categories')
    iter = collection.find()
    if not iter.count():
      return '[]'
    connection.close()
    gc.collect()
    return str(json.dumps(tuple(iter)))
  except Exception as e:
    print str(e)
    return 'Unable to Remove'

def reteriveProducts(MainCategory, SubCategory):
  try:
    MainCategory = MainCategory.replace(" ","_")
    SubCategory = SubCategory.replace(" ","_")
    connection, db, collection = MongoDBconnection(MainCategory, SubCategory)
    iter = collection.find()
    if not iter.count():
      return '[]'
    connection.close()
    gc.collect()
    return str(json.dumps(tuple(iter)))
  except Exception as e:
    print str(e)
    return 'Unable to Remove'
  
def reteriveCategories():
  try:
    connection, db, collection = MongoDBconnection('Admin', 'Categories')
    iter = collection.find()
    if not iter.count():
      return '[]'
    connection.close()
    gc.collect()
    return str(json.dumps(tuple(iter)))
  except Exception as e:
    print str(e)
    return 'Unable to Remove'
  
def reteriveBatches(pid):
  try:
    connection, db, collection = MongoDBconnection('Batches', pid)
    iter = collection.find()
    if not iter.count():
      return '[]'
    connection.close()
    gc.collect()
    return str(json.dumps(tuple(iter)))
  except Exception as e:
    print str(e)
    return 'Unable to Remove'

def updateProduct(product, MainCategory, SubCategory):
  try:
    product = json.loads(product)
    MainCategory = MainCategory.replace(" ","_")
    SubCategory = SubCategory.replace(" ","_")
    connection, db, collection = MongoDBconnection(MainCategory, SubCategory)
    collection.update({"_id":product['_id']},product)
    return 'Updated'
  except Exception as e:
    return str(e)
    return 'Update Failed'

def updateBatch (pid, batch):
  try:
    batch = json.loads(batch)
    connection, db, collection = MongoDBconnection('Batches', pid)
    iter = collection.update({"_id":batch['_id']},batch)
    return 'Updated'
  except Exception as e:
    print str(e)
    return 'Unable to update'
  

def registerDeliveryBoy(user):
  try:
    connection, db, collection = MongoDBconnection('Admin', 'DeliveryBoy')
    user = json.loads(user)
    if collection.find({'$or':[{"Mobile":user['Mobile']},{"Email":user['Email']}]}).count():
      return 'User Already Exists'
    iter = collection.find()
    if not iter.count():
      user['_id']='D_1'
    else:
      user['_id'] = 'D_'+ str(int(iter[iter.count()-1]['_id'].split("_")[-1])+1)
    collection.insert(user)
    connection.close()
    gc.collect()
    return 'Registration Successfull'
  except Exception as e:
    print str(e)
    return 'Unable to Register'

def loginDeliveryBoy(user):
  try:
    connection, db, collection = MongoDBconnection('Admin', 'DeliveryBoy')
    user = json.loads(user)
    iter = collection.find({'$or':[{"Email":user['Email']},{"Mobile":user['Mobile']}]})
    if not iter.count():
      return "User Does't Exists", '[]'
    if user['Password'] == iter[0]['Password']:
      reply = iter[0]
      connection.close()
      gc.collect()
      del reply['Password']
      connection.close()
      gc.collect()
      return 'Login Sucess', reply
    else:
      connection.close()
      gc.collect()
      return 'Authentication Failed', '[]'
  except Exception as e:
    print str(e)
    return 'Unable to Login', '[]'  

def updateOrderStatus(Did, orderID, status):
  try:
    connection, db, collection = MongoDBconnection('DeliveryBoy', Did)
    collection.update({"_id":orderID},{"$set":{"status":status}})
    connection.close()
    connection, db, collection = MongoDBconnection('Admin', 'Orders')
    collection.update({"_id":orderID},{"$set":{"status":status}})
    iter = tuple(collection.find({"_id":orderID}))
    connection.close()
    gc.collect()
    connection, db, collection = MongoDBconnection('Customers', iter[0]['cid'])
    collection.update({"_id":orderID},{"$set":{"status":status}})
    connection.close()
    gc.collect()
    return 'Updated'
  except Exception as e:
    print str(e)
    return 'Unable to Update'

def VerifyOrder(Did, orderID, otp):
  try:
    connection, db, collection = MongoDBconnection('Admin', 'Orders')
    iter = collection.find({"_id":orderID},{"OTP":True})
    if iter.count() and iter[0]['OTP']== otp:
      reply = updateOrderStatus(Did, orderID, 'Delivered')
      if reply == 'Updated':
	connection.close()
	gc.collect()
	return 'Order Delivered'
    connection.close()
    gc.collect()
    return 'Invalid OTP'
  except Exception as e:
    print str(e)
    return 'Unable to Update'

def FetchOrders(userMode, Did):
  try:
    return '[{"_id":"O_101","Products":[{"ProductID":"P_101","PName":"Pepsi","Quantiy":"1 Liter","Price":"RS80"},{"ProductID":"P_102","PName":"Coca","Quantiy":"300 ML","Price":"Rs60"},{"ProductID":"P_103","PName":"Limca","Quantiy":"1 Liter","Price":"Rs90"}],"Customer Name":"Sahil Sehgal","Mobile":"9988776655","City":"Roorkee","state":"Utrakhand", "Address":"IIT Roorkee","Total amount":"1000"},{"_id":"O_102","Products":[{"ProductID":"P_110","PName":"Goodday","Quantiy":"1 Packet","Price":"Rs10"},{"ProductID":"P_112","PName":"50-50 Biscuits","Quantiy":"300gm","Price":"Rs20"},{"ProductID":"P_103","PName":"Limca","Quantiy":"1 Liter","Price":"Rs90"}],"Customer Name":"Sandeep","Mobile":"9188776655","City":"Hyderabad","state":"Andhra Pardesh", "Address":"RamKoti","Total amount":"2000"}]'
    connection, db, collection = MongoDBconnection(userMode, Did)
    if userMode == 'DeliveryBoy':
      iter = collection.find({"status":"Pending"})
    else:
      iter = collection.find()
    if not iter.count():
      return '[]'
    return str(json.dumps(tuple(iter)))
  except Exception as e:
    print str(e)
    return 'Unable to Fetch'

def testing():
  x = {u'description': u'Maah ki dal', u'Level1 Category': u'Grocery', u'Main Category': u'Pulses and Grains', u'Sub Category': u'Dals', u'_id': u'0_0_0', u'product_name': u'Maah ki Dal', u'Quantity': [{u'City': u'Hyderabad', u'Quantities': [{u'$$hashKey': u'object:3', u'Quantity': [u'1 Kg', 1000]}, {u'$$hashKey': u'object:16', u'Quantity': [u'500 gm', 50]}]}]}
  for index,val in enumerate(x['Quantity']):
    for i,val in enumerate(x['Quantity'][index]["Quantities"]):
      del x['Quantity'][index]["Quantities"][i]["$$hashKey"]
  return json.dumps(x) 

if __name__ == '__main__':
  #print testing()
  #print VerifyOrder('D_1',"O_102",'9182')
  print updateProduct('{"_id":"123", "Name":"Sahil","Category":["Val1", "val2"]}', 'Bakery', 'Cakes')
  #print reteriveProducts('Bakery','Cakes')
  #print reteriveCategories()
  #print addSubCategory('Grocery', 'Bakery', 'Cakes')
  #print removeSubCategory('Grocery', 'Pulses and Grains', 'Dals')
  #print removeMainCategory('Grocery', 'Medicines')
  #print addMainCategory('Grocery', 'Medicines')
  #print removelevel1Category('Electricals')
  #print addlevel1Category('Electricals')
  #print RemoveBatch('P_1_1_1',"B_3")
  #print AddBatch('P_1_1_1','{"Product Name": "Cocacola", "Quantity":10, "Quantity Unit":"Number", "SP":15, "CP":18}')
  #print registerAdmin('{"Name":"Sahil","Password":"123456","Mobile":"9780008628","Email":"sahilsehgal1995@gmail.com"}')
  #print loginAdmin('{"Email":"sahilsehgal1995@gmail.com","Password":"123456","Mobile":"9780008628"}')
  #print registerProduct('Snacks Beverages','Cold Drinks','{"_id":"1_1","Name":"Coke", "Brand":"CocaCola"}')
  #print removeProduct('Snacks Beverages','Cold Drinks','P_1_1_1')

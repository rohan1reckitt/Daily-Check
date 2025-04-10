import pymysql.cursors
import time
from flask import Flask, jsonify
from flask_cors import CORS
from flask import request, jsonify
from pymongo import MongoClient
import urllib.parse
from dotenv import load_dotenv
import os

load_dotenv()

Mongo_URI1 = os.getenv("MONGO_URI1")
Mongo_URI2 = os.getenv("MONGO_URI2")
Mongo_Pass = os.getenv("MONGO_PASSWORD")

def fetch_mongo_data(uri, db_name, collection_name,query):

    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]
    cursor = collection.find(query)
    return cursor

encoded_password = urllib.parse.quote_plus(Mongo_Pass)
Mongo_URI =Mongo_URI1+encoded_password+Mongo_URI2

Database ="DailyCheckDB"
Collection ="credentials"

print(Mongo_URI)

app = Flask(__name__)
CORS(app)  

def get_pk_connection():
	Collection_data = fetch_mongo_data(Mongo_URI, Database, Collection, {"country": "pk"})
	for doc in Collection_data:
		docs=doc
	connection = pymysql.connect(host=docs['host'] ,
	user=docs['user'],
	password=docs['password'],
	#port=2499,
	db=docs['db'],
	charset='utf8mb4',
	cursorclass=pymysql.cursors.DictCursor)
	return connection

def get_sa_connection():
	Collection_data = fetch_mongo_data(Mongo_URI, Database, Collection, {"country": "sa"})
	for doc in Collection_data:
		docs=doc
	connection = pymysql.connect(host=docs['host'],
	user=docs['user'],
	password=docs['password'],
	#port=2499,
	db=docs['db'],
	charset='utf8mb4',
	cursorclass=pymysql.cursors.DictCursor)
	return connection

def get_middle_east_connection():
	Collection_data = fetch_mongo_data(Mongo_URI, Database, Collection, {"country": "me"})
	for doc in Collection_data:
		docs=doc
	connection = pymysql.connect(host=docs['host'],
	user=docs['user'],
	password=docs['password'],
	#port=2499,
	db=docs['db'],
	charset='utf8mb4',
	cursorclass=pymysql.cursors.DictCursor)
	return connection

def get_eg_connection():
	Collection_data = fetch_mongo_data(Mongo_URI, Database, Collection, {"country": "eg"})
	for doc in Collection_data:
		docs=doc
	connection = pymysql.connect(host=docs['host'],
	user=docs['user'],
	password=docs['password'],
	#port=2499,
	db=docs['db'],
	charset='utf8mb4',
	cursorclass=pymysql.cursors.DictCursor)
	return connection

def get_gcc_connection():
	Collection_data = fetch_mongo_data(Mongo_URI, Database, Collection, {"country": "gcc"})
	for doc in Collection_data:
		docs=doc
	connection = pymysql.connect(host=docs['host'],
	user=docs['user'],
	password=docs['password'],
	#port=2499,
	db=docs['db'],
	charset='utf8mb4',
	cursorclass=pymysql.cursors.DictCursor)
	return connection


def main_result(dataList,output,actualCnt):
	cnt =0
	result=False
	lst=[]
	for i in output:
		cnt+=1
		if(dataList[i['platform_name']]==i['count(*)']):
			print("True")
			result=True
			lst.append({i['platform_name']:result,"count":i['count(*)']})
		else: 
			print(i['platform_name'],"  ",i['count(*)'])
			result=False
			lst.append({i['platform_name']:result,"count":i['count(*)']})
	print("Todays Platform Number: ",cnt)
	return {"result":lst,"Todays Platform Number":cnt,"Actual Platforms":actualCnt}

def main_result2(dataList,output,actualCnt):
	cnt =0
	result=False
	lst=[]
	for i in output:
		cnt+=1
		if(dataList[i['platform_name']]==i['count(keyword)']):
			print("True")
			result=True
			lst.append({i['platform_name']:result,"count":i['count(keyword)']})
		else: 
			print(i['platform_name'],"  ",i['count(keyword)'])
			result=False
			print(result)
			lst.append({i['platform_name']:result,"count":i['count(keyword)']})
	print("Todays Platform Number: ",cnt)
	return {"result":lst,"Todays Platform Number":cnt,"Actual Platforms":actualCnt}



def main(connections,ind,date_str):
	connection, country =list(connections.items())[ind]
	curr = connection.cursor()
	print(curr) 
	sql_command = """
	select distinct pf_id, count(*), platform_name, created_on, status
	from rb_pdp
	where date(created_on) = %s and status = 1
	group by pf_id
	"""
	# sql_command ="select distinct pf_id, count(*),platform_name,created_on,status from rb_pdp where date(created_on)='2025-03-25'  and status=1 GROUP by pf_id"
	curr.execute(sql_command, (date_str,))
	output = curr.fetchall() 

	dataList_pk={"Daraz":1115,"Pandamart":2672}
	dataList_uae={"Careem-App":1660,"Ninja":6000,"Nana":1776,"Noon Minutes":12900,"Talabat":4517,"Amazon UAE 3P":36,"Carrefouruae":5642,"Amazon KSA":920,"Amazon":519}
	dataList_sa={"Takealot":389,"Picknpay ASAP":5681,"Amazon":314,"Picknpay":3588,"Sixty60":15300,}
	dataList_eg ={"Amazon":142,"Talabat":4572,"BreadFast":806}
	dataList_gcc ={"Talabat BH":760,"Drops":358,"Tawseel":317,"Talabat KW":2057,"Talabat OM":558,"Talabat QA":1304}

	if(country=='dataList_uae'):
		datalist =dataList_uae
		print("Country :", "Middle East (UAE)" )
		# main_result(datalist,output)

	elif(country=='dataList_sa'):
		datalist =dataList_sa
		print("Country :", "South Africa (SA)" )
		# main_result(datalist,output)
	elif(country=='dataList_pk'):
		print("Country :", "Pakistan (PK)" )
		datalist =dataList_pk
		# main_result(datalist,output)
	elif(country=='dataList_eg'):
		print("Country :", "Egypt (Eg)" )
		datalist =dataList_eg
		# main_result(datalist,output)
	elif(country=='dataList_gcc'):
		print("Country :", "(GCC)" )		
		datalist =dataList_gcc
		# main_result(datalist,output)


	print("Actual Platforms: ",len(datalist))
	# for j in output:
	return main_result(datalist,output,len(datalist))
	#     print(j,end='\n')

def main2(connections,ind,date_str):
	connection, country =list(connections.items())[ind]
	curr = connection.cursor()
	print(curr) 
	sql_command = """
	select distinct pf_id, count(keyword),platform_name ,created_on,status from rb_kw
	where date(created_on)=%s and status=1  GROUP by pf_id;
	"""
	# sql_command ="select distinct pf_id, count(*),platform_name,created_on,status from rb_pdp where date(created_on)='2025-03-25'  and status=1 GROUP by pf_id"
	curr.execute(sql_command, (date_str,))
	output = curr.fetchall() 

	dataList_pk={"Daraz":1129,"Pandamart":1880}
	dataList_uae={"Amazon KSA":4426,"Amazon":4414}
	dataList_sa={"PICKNPAY ASAP":13957,"Amazon":4195,"Takealot":7112,"Picknpay":25010,"sixty60":37820}
	dataList_eg ={"Amazon" :1281}
	dataList_gcc ={}

	if(country=='dataList_uae'):
		datalist =dataList_uae
		print("Country :", "Middle East (UAE)" )
		# main_result(datalist,output)

	elif(country=='dataList_sa'):
		datalist =dataList_sa
		print("Country :", "South Africa (SA)" )
		# main_result(datalist,output)
	elif(country=='dataList_pk'):
		print("Country :", "Pakistan (PK)" )
		datalist =dataList_pk
		# main_result(datalist,output)
	elif(country=='dataList_eg'):
		print("Country :", "Egypt (Eg)" )
		datalist =dataList_eg
		# main_result(datalist,output)
	elif(country=='dataList_gcc'):
		print("Country :", "(GCC)" )		
		datalist =dataList_gcc
		# main_result(datalist,output)


	print("Actual Platforms: ",len(datalist))
	# for j in output:
	return main_result2(datalist,output,len(datalist))
	#     print(j,end='\n')


@app.route('/')
def home():
	return(jsonify({"message":"Hello From server!!"}))

@app.route('/get_data', methods=['POST'])
def get_data():
	data = request.get_json()
	country_code = data.get('country_code')
	date_str = data.get('date')  
	

	connections = {
		get_middle_east_connection(): "dataList_uae",
		get_sa_connection(): "dataList_sa",
		get_pk_connection(): "dataList_pk",
		get_eg_connection(): "dataList_eg",
		get_gcc_connection(): "dataList_gcc"
	}

	country_lst = {
		"me": 0,
		"sa": 1,
		"pk": 2,
		"eg": 3,
		"gcc": 4
	}

	country_num = country_lst.get(country_code)
	result = main(connections, country_num, date_str)
	return jsonify(result)

@app.route('/get_kw', methods=['POST'])
def get_kw():
	data = request.get_json()
	country_code = data.get('country_code')
	date_str = data.get('date')  

	connections = {
		get_middle_east_connection(): "dataList_uae",
		get_sa_connection(): "dataList_sa",
		get_pk_connection(): "dataList_pk",
		get_eg_connection(): "dataList_eg",
		get_gcc_connection(): "dataList_gcc"
	}

	country_lst = {
		"me": 0,
		"sa": 1,
		"pk": 2,
		"eg": 3,
		"gcc": 4
	}

	country_num = country_lst.get(country_code)
	result = main2(connections, country_num, date_str)
	return jsonify(result)

def findCountry_code(country):
	county_lst={"me" :0,
	"sa":1,
	"pk":2,
	"eg" :3,
	"gcc" :4}
	country_cod =county_lst.get(country)
	print(country_cod)
	return country_cod

if __name__ =="__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)


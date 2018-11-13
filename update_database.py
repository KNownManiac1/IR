import pymysql
import random
import pickle


def update_database(db, cursor, userId, docId, id):
	sql = "SELECT * FROM user_clicks WHERE USER_ID = " + str(userId) + " AND DOC_ID = " + str(docId)
        try:
             	cursor.execute(sql)
             	number = cursor.rowcount
		if number == 0:
			try:
				sql = "INSERT INTO user_clicks VALUES(" + str(userId) + "," + str(docId) + ", 1, " + str(id) + ")" 
				cursor.execute(sql)
				db.commit()
				print 'Successfully inserted new user-document pair'
			except Exception as e:
				print e
				print 'Error in inserting a new user-document pair'
				db.rollback()  	
		else:
			try:
				sql = "SELECT CLICKS FROM user_clicks WHERE USER_ID = " + str(userId) + " AND DOC_ID = " + str(docId)
				cursor.execute(sql)
				row = cursor.fetchone()
				clicks = row[0]
				if clicks < 50:
					sql = "UPDATE user_clicks SET CLICKS = CLICKS + 1 WHERE USER_ID = " + str(userId) + " AND DOC_ID = " + str(docId)
					cursor.execute(sql)
					db.commit()
					print 'Successfully updated clicks ' + str(clicks +1) 
			except Exception as e:
				print e
				print 'Error in updating clicks of existing user'
				db.rollback()
        except Exception as e:
            	print str(e) + str(userId) + str(docId)
             	print 'Error in checking if user is present'
             	db.rollback()


def create_random_data(db, cursor, users, documents):
	for i in range(1000):
		user_data = random.randint(min(users), max(users))
		document_data = random.randint(min(documents), max(documents))
		update_database(db, cursor, user_data, document_data, i+1)
	

def main():
	users = [i for i in range(1,101)]
	fp = open('document-index.txt', 'rb')
	doc_index = pickle.load(fp)
	fp.close()
	documents = [int(i) for i in doc_index.values()]
	db = pymysql.connect("localhost", "qasys", "321@demo", "QA_system")
	cursor = db.cursor()
	create_random_data(db, cursor, users, documents)
	db.close()


if __name__ == '__main__':
	main()

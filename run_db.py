import sqlite3
from collections import namedtuple
import md5
import time
CONFIG = { "users" : 
			[	{ "id": 0, "username": "jjangoo", "password": "mypassword", "email": "jjangoo81@gmail.com"},
		 		{ "id": 1, "username": "booboo", "password": "mypassword1", "email": "booboo90@gmail.com"}, 
		 		{ "id": 2, "username": "ameoba", "password": "mypassword2", "email": "ameoba@gmail.com"}
		 	],
		 	"conversations":
		 	[   { "id": 0, "user1": 0, "user2": 1, "ip": "127.0.0.1", "time": time.time() }, 
		 	    { "id": 1, "user1": 1, "user2": 0, "ip": "127.0.0.1", "time": time.time() },
		 	    { "id": 2, "user1": 2, "user2": 0, "ip": "127.0.0.1", "time": time.time() }
		 	],
		 	"messages":
		 	[   {"id": 1, "message": "hey what is up", "user_id": 0, "ip": "127.0.0.1", "time": time.time(), "conversation_id": 1 },
		 	   {"id": 2, "message": "what is your name?", "user_id": 2, "ip": "127.0.0.1", "time": time.time(), "conversation_id": 2 },
		 	   {"id": 3, "message": "steve", "user_id": 1, "ip": "127.0.0.1", "time": time.time(), "conversation_id": 0 },
		 	]
		 }
conn = sqlite3.connect("MESSAGE.db")
User = namedtuple("User", ["id", "username", "password", "email"])
Conversation = namedtuple("Conversation", ["id", "user1", "user2", "ip", "time" ])
Message = namedtuple("Message", ["id", "message", "user_id", "ip", "time", "conversation_id" ])
users = []
for each_user in CONFIG["users"]: 
	user = User(each_user["id"], each_user["username"], md5.new(each_user['password']).hexdigest(), each_user["email"])
	users.append(user)
conversations = []
for each_convo in CONFIG["conversations"]:
	conversation = Conversation(each_convo["id"], each_convo["user1"], each_convo['user2'], each_convo['ip'], each_convo['time'])
	conversations.append(conversation)	
messages = []	
for each_msg in CONFIG["messages"]:
	message = Message(each_msg["id"], each_msg["message"], each_msg["user_id"], each_msg["ip"], each_msg["time"], each_msg["conversation_id"])
	messages.append(message)

c = conn.cursor()
CREATE_TABLE_FOR_USER_QUERY = """create table if not exists users
							(id integer primary key, username varchar(25) not null,
							password varchar(50) not null, email varchar(100) not null)"""	
c.execute(CREATE_TABLE_FOR_USER_QUERY)
CREATE_TABLE_FOR_CONVERSATION_QUERY = """create table if not exists conversation 
      						( id integer primary key, user1 integer not null, user2 integer not null, 
      					     ip varchar(30), time integer not null, 
      					     foreign key(user1) references users(id), 
      					     foreign key(user2) references users(id))"""
c.execute(CREATE_TABLE_FOR_CONVERSATION_QUERY)
CREATE_TABLE_FOR_MESSAGE_QUERY = """ create table if not exists message 
							( id integer primary key not null, message varchar(250) not null, 
							 user_id integer not null, ip varchar(30) not null, time integer not null, 
							 conversation_id integer not null, 
							 foreign key(user_id) references users(id),
							 foreign key(conversation_id) references conversation(id))"""
c.execute(CREATE_TABLE_FOR_MESSAGE_QUERY)
for each_user in users:
	c.execute("insert into users values (?,?,?,?)", each_user)
for each_convo in conversations:
	c.execute("insert into conversation values (?,?,?,?,?)", each_convo)	
for each_msg in messages:
	c.execute("insert into message values (?,?,?,?,?,?)", each_msg)

c.execute("select * from users")
resp = c.fetchall()
print resp
c.execute("select * from conversation")
resp = c.fetchall()
print resp
c.execute("select * from message")
resp = c.fetchall()
print resp
conn.close()
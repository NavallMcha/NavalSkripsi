import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('cats-firebase-sdk.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://is-the-cats-fur-wet-default-rtdb.firebaseio.com/'
})

ref = db.reference('/')
ref.set({
    'suhu': '65.41',
    'kelembapan': '95.12',
    'kucing': '0'
})

temperature_ref = ref.child('suhu')
print(temperature_ref.get())

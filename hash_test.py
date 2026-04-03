import bcrypt

salt = bcrypt.gensalt()
hashed = bcrypt.hashpw('admin123'.encode('utf-8'), salt)
print(hashed.decode('utf-8'))

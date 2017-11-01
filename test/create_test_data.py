import random
from app import db

# create some users
words = [line.strip() for line in open("words.txt", "r")]
n_users = 1000
for i in range(n_users):
    first = random.choice(words)
    last = random.choice(words)
    
# create some courses
# create some posts
# create some comments
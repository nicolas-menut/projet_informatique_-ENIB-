import sqlite3 
from datetime import date
from datetime import datetime



conn = sqlite3.connect('Base_off')
c = conn.cursor()

##maintenant nous allons getter la date actuelle 
today = date.today()
today = str(today)
#print(type(today))
today = datetime.strptime(today , '%Y-%m-%d')
#print(type(today))
print("aujourdhui nous sommes le :", today)
c.execute("SELECT dateevent,id FROM event")
for w in c.fetchall():
    j = str(w[0])
    #ici le type est un tuple faut que je le convertisse en datetime
    j = j.strip("('")
    j = j.strip("')")
    j = j.strip(",")
    j = j.strip("'")
    txt = j.split("-")
    if txt[0] == "2019" :
        j = datetime.strptime(j,'%Y-%m-%d')

    if type(j)==type(today):
        if j < today :
            print(today," est superieur a :",j)
            sql = """DELETE FROM event WHERE id=?"""
            val = str(j)
            c.execute(sql,(w[1], ))
            conn.commit()
            print("perime")
        else :
            print(today," est inferieur a :",j)
            print("c ok")
    else:
        print("not the same type")

        

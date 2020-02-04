#coding by Dhamydau#
from dibimadpro import db 



#REMISE A JOUR DU SITE
#linteret est juste dans un premier temps de se connecter puis dacceder que aux events
#sa ne sert a rien de passer dune table autant lier lid du pro et daller chercher les events qui corresponde 
#a cette enseigne 
#donc pour faire plus court : deux classes une pour se co 
#une pour consulter et rajouter des events


class Logueur(db.Model):
    __tablename__="logueur"

    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String , nullable = False)
    mdp = db.Column(db.String , nullable = False)


#donc jinistialise cest obligatoire je nutilise enfin jextraie ce qui minteresse 
    def __init__(self,name,mdp):
        self.name = name
        self.mdp = mdp

#de souvenir cest le fait d'ordonner l'affichage
    def  __repr__(self):
        return '<{}-{}>'.format(self.name,self.mdp)

    def getter(self,a):
        db.create_all()
        truc = Logueur.query.filter_by(name = a).first()
        return truc.id
    
    def getterName(self,name):
        db.create_all()
        vlum = Logueur.query.filter_by(id = name).first()
        return vlum.name




class Event(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nom_event = db.Column(db.String)
    dateevent = db.Column(db.Integer)
    id_enseigne = db.Column(db.Integer , db.ForeignKey('point.id'))
    point = db.relationship('Point')
    infoevent = db.Column(db.String)


    def __init__(self,nom_event,dateevent,id_enseigne,infoevent):
        self.nom_event = nom_event
        self.dateevent = dateevent 
        self.id_enseigne = id_enseigne
        self.infoevent = infoevent
    
    def __repr__(self):
        return "<Point %s: Lat %s >" % (self.nom_event,self.dateevent)


    def getter(self , a):
        #ici le but sera de recuperer toutes les events dune enseigne a partir de lid_enseigne
        db.create_all()
        truc = Event.query.filter_by(id_enseigne=a).all()
        return truc

    def sauveur(self,a,b,c):
        db.create_all()
        d = "Null"
        db.session.add(Event(a,b,c,d))
        db.session.commit()

    def sauveurBis(self,a,b,c,d):
        db.create_all()
        db.session.add(Event(a,b,c,d))
        db.session.commit()
    
    def eliminator(self, value):
        db.create_all()
        Event.query.filter_by(nom_event = value).delete()
        db.session.commit()


class Point(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    latitude_off = db.Column(db.Float)
    longitude_off = db.Column(db.Float)
    filtre_id = db.Column(db.Integer , db.ForeignKey('filtre.id'))
    name = db.Column(db.String)
    #district nest pas definis car cela va etre notre seconde classe donc on va la definir pour quelle existe dans cette classe
    filtre = db.relationship('Filtre')
    #jai tout simplement dit que cest en relation avec notre table sql District 

    def __init__(self,id,filtre,latitude_off,longitude_off,name):
        self.id = id 
        self.filtre = filtre
        self.latitude_off = latitude_off
        self.longitude_off = longitude_off
        self.name = name
    
    def __repr__(self):
        return "<Point %d: Lat %s Lng %s %s>" % (self.id, self.latitude_off, self.longitude_off,self.name)

    def getName(self,i):
        db.create_all()
        a = Point.query.filter_by(id = i).first()
        return a 


class Filtre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    
    def __repr__(self):
        return "<Point %d: Lat %s>" % (self.id, self.name)




class Logueura(db.Model):
    __tablename__="Table_user"

    _id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String , nullable = False)
    mdp = db.Column(db.String , nullable = False)
    id_en = db.Column(db.Integer , nullable = False)

#donc jinistialise cest obligatoire je nutilise enfin jextraie ce qui minteresse 
    def __init__(self,name,mdp,id_en):
        self.name = name
        self.mdp = mdp
        self.id_en = id_en

#de souvenir cest le fait d'ordonner l'affichage
    def  __repr__(self):
        return '<{}-{}-{}>'.format(self.name,self.mdp,self.id_en)

    def getter(self,a,b):
        db.create_all()
        truc = Logueura.query.filter_by(name = a).first()
        return truc.id_en


class Enseigne(db.Model):
    __tablename__="Table_enseigne"

    _id = db.Column(db.Integer , primary_key = True)
    nom = db.Column(db.String , nullable = False)
    adresse = db.Column(db.String , nullable = False)
    id_events = db.Column(db.String , nullable = False)

#donc jinistialise cest obligatoire je nutilise enfin jextraie ce qui minteresse 
    def __init__(self,nom,adresse,id_events):
        self.nom = nom
        self.adresse = adresse
        self.id_events = id_events

#de souvenir cest le fait d'ordonner l'affichage
    def  __repr__(self):
        return '<{}-{}-{}>'.format(self.nom,self.adresse,self.id_events)
    
    def getter(self , a):
        db.create_all()
        truc = Enseigne.query.filter_by(_id = a).first()
        return truc.id_events

    


    
class Tara(db.Model):
    __tablename__="Tara"

    _id = db.Column(db.Integer , primary_key = True)
    nameevent = db.Column(db.String , nullable = False)
    place = db.Column(db.String , nullable = False)
    timeadd = db.Column(db.Integer , nullable = False)
    timeevent = db.Column(db.Integer , nullable = False)

#donc jinistialise cest obligatoire je nutilise enfin jextraie ce qui minteresse 
    def __init__(self,nameevent,place,timeadd,timeevent):
        self.nameevent = nameevent
        self.place = place
        self.timeadd = timeadd
        self.timeevent = timeevent

#de souvenir cest le fait d'ordonner l'affichage
    def  __repr__(self):
        return '<{}-{}-{}-{}>'.format(self.nameevent,self.place,self.timeadd,self.timeevent) 
    
    def sauveur(self,a,b,c,d):
        db.create_all()
        db.session.add(Tara(a,b,c,d))
        db.session.commit()
    
    def eliminator(self, value):
        db.create_all()
        Tara.query.filter_by(nameevent = value).delete()
        db.session.commit()

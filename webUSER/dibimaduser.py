#coding by Dhamydau#
from flask import Flask ,render_template ,g 
from mocks import Post
from datetime import datetime
import sqlite3
from flask import request
from flask import redirect
from flask import url_for,flash
from flask_wtf import FlaskForm
from wtforms import SelectField 
from flask_sqlalchemy import SQLAlchemy
from os import listdir
from os.path import isfile, join


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../BDD/Base_off'  
app.secret_key = 'my precious'
db = SQLAlchemy(app)

#Le but du jeu est dafficher une page avec un menu deroulant permettant a lutilisateur de choisir 
#quel filtre utiliser
#a partir de la en fonction du filtre la map va afficher les differents points sur la map
#qui est de base naturellement centre sur brest


####################LES CLASSES#############################
#dans notre cas nous allons utiliser que deux classes
#la premiere permettra de getter les coordonnees des ppoints chaques points a une identite unique et une identite le reliant a un filtre en particulier 
#la deuxieme classe sera tout simplement le nom du filtre que lutilisateur choisira, en fonction de sa 
#le programme ne choisira daffficher que les points correspondant a un filtre en particulier

#nous allons commencer par definir dans notre programme la classe des points 

##CLasse test vu que sa veut pas marcher 

class Event(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nom_event = db.Column(db.String)
    dateevent = db.Column(db.Integer)
    id_enseigne = db.Column(db.Integer , db.ForeignKey('point.id'))
    point = db.relationship('Point')
    infoevent = db.Column(db.String)


    def __init__(self,id,nom_event,dateevent,point,infoevent):
        self.id = id 
        self.point = point 
        self.nom_event = nom_event
        self.dateevent = dateevent 
        self.infoevent = infoevent
    
    def __repr__(self):
        return "<Point %s %s: Lat %s %s %s >" % (self.id, self.nom_event,self.dateevent,self.infoevent , self.point)



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

class Filtre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    
    def __repr__(self):
        return "<Point %d: Lat %s>" % (self.id, self.name)


class Form(FlaskForm):
    dist = SelectField('Filtre' , choices = [])

################## FIN CLASSES #####################


#@app.route('/')
##on rajoute des metadonnees ce sont des infos supplementaires en gros dans notre cas sur notre url si on fait un / et bien cela appellera notre fonction ci dessous
#def home():
#    #ok donc la on va incorporer tous les filtres dans une liste deroulante dans notre html pour cela 
#    #on va recueuillir tous le data de la column de la table district
#    districts = District.query.all()
#    #ok la jai toutes les informations de la table de tout0es les columns
#    #jai plus qua incorporer sa dans mon html 
#    form = Form()
#    return render_template('pages/home.html',form = form)

@app.route('/', methods=['GET','POST'])
def home():
    form = Form()
    #cest pour initialiser comme on commence par quelquechose faut bien la definir.
    tap  = Filtre.query.all()
    data = district(1)
    form.dist.choices = [(dist.id , dist.name) for dist in Filtre.query.all()]
    if request.method == 'POST':
        val = form.dist.data 
        data = district(val)
        return render_template('pages/home.html',form = form , data = data)

    return render_template('pages/home.html',form = form,  data = data) 







@app.route("/district/<int:district_id>")
def district(district_id):
    #cette route est dans le cas ou lutilisateur change lid du filtre 
    #premier temps on prends tout le data de la table points qui comprennent seulement comme district_id ce qua tape luser 
    #manque plus qua getter les coordonnees du point car cest que ce quon veut
    hello = int(district_id)
    if hello == 1 :
        flop = Point.query.all()
    else :
        flop = Point.query.filter_by(filtre_id = district_id).all()
    tablat = []
    tablong = []
    tabid = []
    tabname = []
    for i in flop :
        print("je suis une value : ",i.id,type(i.id))
        tablat.append(i.latitude_off)
        tablong.append(i.longitude_off)
        tabid.append(i.id)
        text = i.name 
        text = str(text)
        print(text)
        tabname.append(text)
    data = {"lat":tablat , "long":tablong , "id":tabid, "name":tabname}
    for j in tabname :
        print("voila ",j)
    return data
    
#le but du jeu est que quand on genere un point ce dernier doit rajouter un url for qui va appeler une fonction cette fonction doit verifier les informations du point donne et doit generer les evenements propose
#... Premier jet : mettre en avant que son id qui est un id fixe des que son id est donne il va chercher le nom et les evenements qui lui correspond 
#point faible pour linstant : trouver un moyen de mettre un argument dans un urlfor 


@app.route('/<name>')
#on rajoute des metadonnees ce sont des infos supplementaires en gros dans notre cas sur notre url si on fait un / et bien cela appellera notre fonction ci dessous
def hello(name):
    a = Point.query.filter_by(id = name).first()
    print(a.name)
    val = "none"
    try:
        faile = open("./Infos/"+a.name,'r')
        contenue = faile.read()
        faile.close()
    except:
        contenue="None"

    fichiers = [f for f in listdir('./static/logo/') if isfile(join('./static/logo',f))]
    for i in fichiers :
        print('HELLLLLLOOO',i)
        v  = i.split('.')
        if v[0]==a.name :
            val = str(i) 

    print(contenue)
    contenue = str(contenue)
    fap = Event.query.filter_by(id_enseigne = name).all()

    return render_template('pages/about.html',name = fap,texte = contenue , title = a.name,val=val)

@app.route('/info/<int:idevent>')
def moremore(idevent):
    info = Event.query.filter_by(id = idevent).first()
    return render_template('pages/info.html',data = info)

@app.route('/info/<int:idevent>',methods = ['GET','POST'])
def moremoremore(idevent):
    nid = Event.query.filter_by(id = idevent).first()
    if request.method == 'POST':
        if "return" in request.form:
            return redirect(url_for('hello' ,name = nid.id_enseigne))

@app.route('/about')
#on rajoute des metadonnees ce sont des infos supplementaires en gros dans notre cas sur notre url si on fait un / et bien cela appellera notre fonction ci dessous
def about():
    return render_template('pages/about.html')

@app.route('/contact')
#on rajoute des metadonnees ce sont des infos supplementaires en gros dans notre cas sur notre url si on fait un / et bien cela appellera notre fonction ci dessous
def contact():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@app.route('/blog')
#on rajoute des metadonnees ce sont des infos supplementaires en gros dans notre cas sur notre url si on fait un / et bien cela appellera notre fonction ci dessous
def posts_index():
    posts= Post.all()
    return render_template('posts/index.html', posts=posts)

@app.route('/blog/posts/<int:id>')
def posts_show(id):
    posts= Post.all()
    post = Post.find(id)
    return render_template('posts/show.html',post=post)

@app.context_processor
def inject_now():
    return {'now':datetime.now()}



@app.context_processor
def utility_processor():
    def pluralize(count , singular , plural = None):
        if not isinstance(count , int ):
            raise ValueError('{} must be an integer'.format(count))
        
        
        if plural is None :
            plural = singular + 's'
            
            
        if count == 1 :
            result = singular
            
            
        else :
            result = plural
            
            
        return "{} {}".format(count,result)
            
    return dict(pluralize = pluralize)

# if __name__ ==  '__main__' :
    # ici on dit que si on execute notre code directement il faudra lancer la commande suivante
    # ici je suis en mode developpement a chaque modifications cela va reloader  
    # app.run(debug = True , port = 3000)

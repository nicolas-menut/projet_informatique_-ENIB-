#coding by Dhamydau#
from __future__ import print_function

import os
import time
from datetime import datetime
from functools import wraps
import mimetypes
from flask import Response, render_template
from flask import Flask
from flask import send_file
from flask import request
from flask import session
from flask import redirect
from flask import url_for,flash
from werkzeug import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask import abort

###################################################################################################################
##########################################DESCRIPTION DE MON SITE##################################################
###################################################################################################################
#Mon site a pour but de pouvoir a un utilisateur de se connecter par l'intermediaire dune bdd il va pouvoir modifier des informations se trouvant dans sa table table qui stockera des informations sur des evenements ou autre 
# a savoir , des que levenement a depasse la date actuelle ce dernier est supprime automatiquement histoire de ne pas faire des pubs sur des choses anterieurs 


DATABASE = './BDD/Base_DD'
app = Flask(__name__)
app.secret_key = "my precious"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///../BDD/Base_off'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)
from models import * 




def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap


@app.route('/')
#ici on part dans le debut du site cad explication authentification etc 
def home():
    session.pop('logged_in' , False)
    return render_template('index.html')

@app.route('/log')
def log():
    return render_template('log__.html')


@app.route('/log', methods=['POST'])
def login():
    posts = db.session.query(Logueur).all()
    print(posts)
    if request.method == 'POST' :
        for post in posts :


            if request.form['username'] == post.name and request.form['password'] == post.mdp :
                a = request.form['username']
                b = request.form['password']
                session['logged_in'] = True
                #il va chercher dans la table_user dabord les infos
                n = Logueur(db,db)
                #ici il va chercher le id_en pour se ratttacher a la table des enseignes
                value = n.getter(a)
                #on appel la talbe des enseignes et on va getter les l'information quon veut cest a dire le nom de lenseigne 
                #a partir de la on va appeler la table de lenseigne specifique 
                print("JE SUIS DEDANS")
                print("FDPPPPPP ? ",value)
                #on envoie linformation a la fonction chercheur 
                return redirect(url_for('chercheur',name= value))
                #ici on va se rediriger sur la fonction chercheur et son argument  name sera nameur 

            else:
                error = "veuillez entrer un id ou mdp correct"
    return render_template('log__.html',error = error)


@app.route('/home/<name>')
@login_required
def chercheur(name):
    #ici je nai pas reussi a "automatiser" la chose jaurai aime integrer name dans db.session.query
    if name != None:
        w = Event(db,db,db,db)
        val = w.getter(name)
        return render_template('demande.html',name = name , posts = val)
    else :
        error = "la table n'a pas ete trouve"
        return render_template('log__.html',error = error )


@app.route('/home/<name>',methods = ['POST','GET'])
def modif_table(name):
    v = Logueur(db,db)
    nomens = v.getterName(name)
    if request.method == 'POST':
            
        if 'envoie' in request.form:
                a = request.form['addevent']
                b = request.form['addplace']
                c = request.form['infoevent']
                #d = request.form['addtimeevent']
                w = Event(db,db,db,db)
                if a != "" :
                    if b != "":
                        if c!= "":
                            w.sauveurBis(a,b,name,c)
                        else :
                            w.sauveur(a,b,name)
                        #if c != "":
                            #if d != "":

                if a == "":
                    flash("Veuillez mettre un evenement svp \n")
                if b == "":
                    flash("\n Veuillez mettre un endroit svp \n")
                #if c == "":
                    #flash("Veuillez mettre une date svp")
                #if d == "":
                #flash("Veuillez mettre un date d'event svp")
        if 'upload' in request.form :
            return redirect(url_for('upload',name = name))
                    
        if 'rmv' in request.form:
            a = request.form['destructor']
            w = Event(db,db,db,db)
            w.eliminator(a)

    posts = w.getter(name)
    #bon la sa chier mais je crois que cest une question de securite car il sait pas ce quil doit rajouter au niveau des colonnes donc je crois quil faudra 
    #predefinir ce quil faudra appliquer tout simplement donc creer une fonction dans la classe qui va recuperer lid actuel pour linserer dans lid enseigne 
    return render_template('demande.html',posts = posts , vul = nomens)


  

@app.route('/home/<name>/upload')
def upload(name):
    return render_template('upload.html')

@app.route('/home/<name>/upload' , methods = ['POST','GET'])
def uploader(name):
    if request.method == 'POST' :
        if 'maintenant' in request.form :
            print("oui je suis rentrreeeeee !!! ")
            f = request.files['file']
            w = Point(db,db,db,db,db)
            nom = w.getName(name)
            texte = f.filename.split('.')
            if texte[1]=='png':
                f.filename = nom.name +'.png'
            if texte[1]=='jpg':
                f.filename = nom.name + '.jpg'
            f.save(os.path.join('static/logo',secure_filename(f.filename)))
            txt = "votre fichier a bien ete enregistre"
            return render_template('upload.html',parle = txt)
        
        if 'retour' in request.form :
            return redirect(url_for('chercheur',name = name))


# if __name__ == '__main__':

    # Standalone
    # app.run( port=8080, debug=True)

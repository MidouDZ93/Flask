from flask import Flask, render_template ,request, redirect, url_for,flash,send_file
import json

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def index():
    return render_template('index.html')

#afficher les taches dont le statut est en cours
@app.route("/tacheencours")
def tacheencour():
   with open('taches.json', 'r') as file:
     taches = json.load(file)
     taches_en_cours = [tache for tache in taches if tache.get('statut') == 'en cours'or tache.get('statut') == 'non assignee']
     return render_template('tacheencours.html', taches=taches_en_cours)


def get_all_employees():
    with open('employes.json', 'r') as employes_file:
        employes = json.load(employes_file)
    return employes


  
from flask import redirect, url_for

@app.route("/edit/<titre>", methods=['GET', 'POST'])
def edit_task(titre):
    if request.method == 'POST':
        with open('taches.json', 'r') as file:
            taches = json.load(file)
        
        for tache in taches:
            if tache['titre'] == titre:
                tache['titre'] = request.form.get('titre')
                tache['description'] = request.form.get('description')
                tache['statut'] = request.form.get('statut')
                nouveau_nom_employe = request.form.get('employe_assigne')
                
                # Rechercher l'employé dans la liste des employés
                employe_details = None
                with open('employes.json', 'r') as employes_file:
                    employes = json.load(employes_file)
                    for employe in employes:
                        if employe['nom'] == nouveau_nom_employe:
                            employe_details = employe
                            break
                
                # Mettre à jour l'employé assigné dans la tâche
                tache['employe_assigne'] = employe_details
                
                break
        
        with open('taches.json', 'w') as file:
            json.dump(taches, file, indent=4)
        
        # Rediriger vers la page affichant toutes les tâches
        return redirect(url_for('touteslestaches'))
    else:
        # Si la méthode de requête est GET, renvoyer le template edit_task.html avec les détails de la tâche
        with open('taches.json', 'r') as file:
            taches = json.load(file)
        
        for tache in taches:
            if tache['titre'] == titre:
                employes = get_all_employees()  # Utilisation de la fonction pour obtenir la liste des employés
                return render_template('edit_task.html', tache=tache, employes=employes)
        
        # Si la tâche avec le titre spécifié n'est pas trouvée, rediriger vers la page affichant toutes les tâches
        flash('La tâche spécifiée n\'a pas été trouvée.', 'error')
        return redirect(url_for('touteslestaches'))






@app.route("/delete/<titre>", methods=['POST'])
def delete_task(titre):
    # Supprimer la tâche avec le titre donné
    with open('taches.json', 'r+') as file:
        taches = json.load(file)
        taches = [tache for tache in taches if tache['titre'] != titre]
        file.seek(0)
        json.dump(taches, file, indent=4)
        file.truncate()
    
    # Rediriger vers la page des tâches en cours
    return redirect(url_for('tacheencour'))




@app.route("/touteslestaches")
def touteslestaches():
    # Load tasks from taches.json
    with open('taches.json', 'r') as file:
        taches = json.load(file)
    
    # Render the template with the tasks data
    return render_template('touteslestaches.html', taches=taches)


@app.route("/export-json")
def export_json():
    # Logic to export the JSON file
    # For example, you can send the file directly using Flask's send_file function
    return send_file('taches.json', as_attachment=True)





# Charger les données des employés depuis employes.json
with open('employes.json', 'r') as file:
    employes = json.load(file)

# Route pour afficher le formulaire de création
@app.route("/ajouttache", methods=['GET'])
def create_task_form():
    return render_template('ajouttache.html', employes=employes)

@app.route("/ajouttache", methods=['POST'])
def create_task():
    # Récupérer les détails de la tâche depuis le formulaire
    titre = request.form['titre']
    description = request.form['description']
    statut = request.form['statut']
    employe_nom = request.form['employe_assigne']

    # Rechercher l'employé dans la liste des employés
    employe_details = None
    for employe in employes:
        if employe['nom'] == employe_nom:
            employe_details = employe
            break

    # Créer un dictionnaire pour la nouvelle tâche
    new_task = {
        'titre': titre,
        'description': description,
        'statut': statut,
        'employe_assigne': {
            'nom': employe_details['nom'],
            'prenom': employe_details['prenom'],
            'email': employe_details['email'],
            'icone': employe_details['icone']
        }
    }

    # Ajouter la nouvelle tâche à la liste des tâches
    with open('taches.json', 'r+') as file:
        tasks = json.load(file)
        tasks.append(new_task)
        file.seek(0)
        json.dump(tasks, file, indent=4)

    # Afficher un message de confirmation
    flash('Tâche créée avec succès!', 'success')

    # Rediriger vers la page de toutes les tâches
    return redirect(url_for('touteslestaches'))



def get_all_employees():
    with open('employes.json', 'r') as employes_file:
        employes = json.load(employes_file)
    return employes



app.run()

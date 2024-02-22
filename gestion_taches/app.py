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
                tache['employe_assigne'] = request.form.get('employe_assigne')
                break
        
        with open('taches.json', 'w') as file:
            json.dump(taches, file, indent=4)
        
        # Redirect to the page showing tasks in progress
        return redirect(url_for('tacheencour'))
    else:
        # If the request method is GET, render the edit_task.html template with the task details
        with open('taches.json', 'r') as file:
            taches = json.load(file)
        
        for tache in taches:
            if tache['titre'] == titre:
                return render_template('edit_task.html', tache=tache)
        
        # If the task with the provided title is not found, redirect to the page showing tasks in progress
        flash('La tâche spécifiée n\'a pas été trouvée.', 'error')
        return redirect(url_for('tacheencours'))


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


if __name__ == "__main__":
    app.run(debug=True)

app.run()

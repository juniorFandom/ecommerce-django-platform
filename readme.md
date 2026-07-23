# Market Platform

**Market Platform** est une plateforme modulaire de gestion commerciale conçue pour gérer les utilisateurs, les produits, les catégories, les stocks, les mouvements de stock, les commandes et les paiements.

Le projet est développé avec **Django** et **Django REST Framework**, en suivant une architecture modulaire permettant d'ajouter progressivement de nouvelles fonctionnalités métier.

---

## 🚀 Fonctionnalités

### 👤 Gestion des utilisateurs

* Création de comptes utilisateurs
* Authentification et connexion
* Gestion du profil utilisateur
* Modification du mot de passe
* Activation et désactivation des comptes
* Gestion des rôles et permissions

### 📦 Gestion des produits

* Création et gestion des produits
* Gestion des catégories
* Modification des informations des produits
* Suivi de la disponibilité des produits

### 🏷️ Gestion des catégories

* Création de catégories
* Modification des catégories
* Suppression des catégories
* Liste des catégories

### 📊 Gestion de l'inventaire

* Suivi des stocks
* Gestion des quantités disponibles
* Définition d'un seuil minimal de stock
* Suivi de la disponibilité des produits
* Gestion des quantités réservées

### 🔄 Gestion des mouvements de stock

* Gestion des entrées de stock
* Gestion des sorties de stock
* Gestion des ajustements de stock
* Historique des mouvements
* Enregistrement du motif des mouvements
* Mise à jour automatique de l'inventaire

### 🛒 Gestion des commandes

* Création de commandes
* Gestion des lignes de commande
* Suivi du statut des commandes
* Réservation des stocks
* Annulation des commandes

> **Remarque :** Les modules de gestion des commandes et des paiements sont prévus et seront intégrés progressivement à la plateforme.

### 💳 Gestion des paiements

* Gestion des paiements
* Suivi du statut des paiements
* Gestion des transactions
* Confirmation des paiements
* Gestion des échecs de paiement
* Gestion des remboursements

---

## 🏗️ Architecture du projet

Le projet suit une architecture modulaire basée sur Django :

```text
market-platform/
│
├── users/
│   └── Gestion des utilisateurs et authentification
│
├── categorie/
│   └── Gestion des catégories
│
├── product/
│   └── Gestion des produits
│
├── inventory/
│   └── Gestion de l'inventaire
│
├── mouvement_stock/
│   └── Gestion des mouvements de stock
│
├── orders/
│   └── Gestion des commandes
│
├── payments/
│   └── Gestion des paiements
│
└── config/
    └── Configuration du projet Django
```

---

## 🛠️ Technologies utilisées

### Backend

* Python
* Django
* Django REST Framework
* Django ORM
* PostgreSQL / SQLite

### API et authentification

* API REST
* Authentification JWT
* Système de permissions Django
* OpenAPI
* Swagger

### Développement et DevOps

* Git
* GitHub
* Docker
* CI/CD

---

## 🔄 Flux métier

Le fonctionnement global de la plateforme est conçu selon le flux suivant :

```text
Utilisateur
    │
    ▼
Catalogue des produits
    │
    ▼
Panier
    │
    ▼
Commande
    │
    ▼
Vérification de la disponibilité du stock
    │
    ▼
Réservation du stock
    │
    ▼
Paiement
    │
    ├──────────────► Échec du paiement
    │                    │
    │                    ▼
    │              Libération du stock réservé
    │
    ▼
Paiement réussi
    │
    ▼
Commande confirmée
    │
    ▼
Mise à jour du stock
    │
    ▼
Création du mouvement de stock
```

---

## 📊 Gestion du stock

La plateforme distingue le stock physique du stock réservé.

Exemple :

```text
Stock physique
      │
      ▼
quantity = 100
      │
      ▼
Stock réservé
      │
      ▼
reserved_quantity = 20
      │
      ▼
Stock disponible
      │
      ▼
100 - 20 = 80
```

Cette approche permet de réserver des produits pour des commandes en attente sans diminuer immédiatement la quantité physique présente dans l'inventaire.

Lorsqu'une commande est confirmée et payée, le stock peut être réellement déduit et un mouvement de sortie est créé.

---

## 🔐 Authentification

La plateforme utilise un modèle utilisateur Django personnalisé :

```python
AUTH_USER_MODEL = 'users.User'
```

L'authentification de l'API est prévue pour être basée sur des tokens JWT.

Le fonctionnement général est le suivant :

```text
Client
  │
  │ Connexion
  ▼
API Django REST Framework
  │
  ▼
Génération du token JWT
  │
  ▼
Access Token
  │
  ▼
Accès aux endpoints protégés
```

---

## 📚 Documentation de l'API

La documentation de l'API est générée à l'aide d'OpenAPI et Swagger.

Les endpoints de documentation peuvent être accessibles via :

```text
/api/docs/
/api/schema/
```

Les URLs exactes dépendent de la configuration du projet.

---

## ⚙️ Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/juniorFandom/market-platform.git
```

### 2. Accéder au projet

```bash
cd market-platform
```

### 3. Créer un environnement virtuel

```bash
python -m venv env
```

### 4. Activer l'environnement virtuel

#### Windows

```bash
env\Scripts\activate
```

#### Linux / macOS

```bash
source env/bin/activate
```

### 5. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 6. Configurer les variables d'environnement

Créer un fichier `.env` à la racine du projet :

```env
SECRET_KEY=votre-cle-secrete
DEBUG=True

DB_NAME=market_platform
DB_USER=postgres
DB_PASSWORD=votre-mot-de-passe
DB_HOST=localhost
DB_PORT=5432
```

> ⚠️ Ne jamais publier les clés secrètes, mots de passe ou autres informations sensibles sur GitHub.

### 7. Appliquer les migrations

```bash
python manage.py migrate
```

### 8. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

### 9. Démarrer le serveur

```bash
python manage.py runserver
```

L'API sera accessible à l'adresse :

```text
http://127.0.0.1:8000/
```

---

## 🧪 Tests

Pour exécuter l'ensemble des tests :

```bash
python manage.py test
```

Pour tester une application spécifique :

```bash
python manage.py test users
```

---

## 🔑 Variables d'environnement

Le projet utilise des variables d'environnement afin de séparer la configuration et les informations sensibles du code source.

Exemple :

```env
SECRET_KEY=
DEBUG=
DATABASE_URL=
```

Les fichiers contenant des informations sensibles doivent être exclus du dépôt Git.

Exemple de `.gitignore` :

```gitignore
.env
env/
venv/
__pycache__/
*.pyc
db.sqlite3
```

---

## 📌 État du projet

Le projet est actuellement en cours de développement.

### Fonctionnalités réalisées

* [x] Mise en place du projet Django
* [x] Architecture modulaire
* [x] Gestion des produits
* [x] Gestion des catégories
* [x] Gestion de l'inventaire
* [x] Gestion des mouvements de stock
* [x] Mise en place du modèle utilisateur personnalisé

### Fonctionnalités en cours / à venir

* [ ] Authentification des utilisateurs
* [ ] Authentification JWT
* [ ] Gestion des rôles et permissions
* [ ] Gestion des commandes
* [ ] Gestion du panier
* [ ] Réservation du stock
* [ ] Intégration des paiements
* [ ] Gestion des webhooks de paiement
* [ ] Système de notifications
* [ ] Tests automatisés
* [ ] Mise en place du pipeline CI/CD
* [ ] Conteneurisation avec Docker
* [ ] Déploiement en production

---

## 🗺️ Feuille de route

```text
[x] Gestion des produits
[x] Gestion des catégories
[x] Gestion de l'inventaire
[x] Gestion des mouvements de stock
[ ] Authentification des utilisateurs
[ ] Gestion des rôles et permissions
[ ] Gestion des commandes
[ ] Gestion du panier
[ ] Réservation du stock
[ ] Intégration des paiements
[ ] Système de notifications
[ ] Tests automatisés
[ ] CI/CD
[ ] Conteneurisation Docker
[ ] Déploiement en production
```

---

## 🎯 Objectifs du projet

Les principaux objectifs de **Market Platform** sont :

* Centraliser la gestion des activités commerciales
* Simplifier la gestion des produits et des stocks
* Assurer un suivi précis des mouvements de stock
* Gérer les commandes des clients
* Intégrer des solutions de paiement
* Mettre en place une gestion sécurisée des utilisateurs
* Implémenter une gestion des rôles et des permissions
* Construire une architecture modulaire, évolutive et maintenable
* Automatiser les tests et les déploiements grâce au CI/CD

---

## 👨‍💻 Auteur

Projet développé dans le cadre de la conception d'une plateforme modulaire de gestion commerciale basée sur **Django REST Framework**.

---

## 📄 Licence



from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
import json


def charger_donnees(chemin_fichier):
    """Charge les données JSON depuis un fichier."""
    try:
        with open(chemin_fichier, "r", encoding="utf-8") as fichier:
            return json.load(fichier)
    except FileNotFoundError:
        return []


def organiser_par_section(donnees, chemin_preuves=None):
    """Organise les personnes et preuves par sections."""
    sections = {
        "Employes": [],
        "Criminels": [],
        "Suspects": [],
        "Témoins": [],
        "Preuves": [],
    }
    for personne in donnees:
        classe = personne.get("classe", "Inconnu")
        if classe in ["Employe", "Suspect", "Criminel"]:
            sections[classe + "s"].append(personne)

    if chemin_preuves:
        sections["Preuves"].extend(charger_donnees(chemin_preuves))

    return sections


class BaseScreen(Screen):
    """Classe de base pour les écrans."""

    def go_back_to_menu(self, instance):
        app = App.get_running_app()
        app.root.current = "menu_principal"


class MenuPrincipalScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        layout.add_widget(Label(text="Liste des enquêtes", size_hint=(1, 0.1)))

        scroll = ScrollView(size_hint=(1, 0.8))
        scroll_content = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10)
        scroll_content.bind(minimum_height=scroll_content.setter("height"))

        self.enquetes = charger_donnees("fichiers/enquetes.json")
        for enquete in self.enquetes:
            btn = Button(
                text=f"{enquete['nom']} ({enquete['date_de_debut']} - {enquete['date_de_fin']})",
                size_hint_y=None,
                height=40,
            )
            btn.bind(
                on_release=lambda instance, e=enquete: self.switch_to_enquete_screen(e)
            )
            scroll_content.add_widget(btn)

        scroll.add_widget(scroll_content)
        layout.add_widget(scroll)

        buttons_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        toutes_infos_btn = Button(text="Afficher toutes les infos")
        toutes_infos_btn.bind(on_release=self.afficher_toutes_infos)
        buttons_layout.add_widget(toutes_infos_btn)
        layout.add_widget(buttons_layout)

        layout.add_widget(
            Button(
                text="Quitter",
                size_hint=(1, 0.1),
                on_release=lambda instance: App.get_running_app().stop(),
            )
        )

        self.add_widget(layout)

    def switch_to_enquete_screen(self, enquete):
        app = App.get_running_app()
        app.enquete_screen.set_enquete(enquete)
        app.root.current = "enquete"

    def switch_to_global_section(self, instance):
        app = App.get_running_app()
        app.global_screen.set_section(instance.text)
        app.root.current = "global"

    def afficher_toutes_infos(self, instance):
        toutes_les_enquetes = charger_donnees("fichiers/enquetes.json")
        details = "\n\n".join(
            [
                f"Nom: {e['nom']}\nDates: {e['date_de_debut']} - {e['date_de_fin']}\nPersonnes impliquées: {len(e.get('personne_impliquee', []))}\nPreuves: {len(e.get('liste_preuves', []))}"
                for e in toutes_les_enquetes
            ]
        )
        popup = Popup(
            title="Toutes les informations",
            content=Label(text=details, halign="left", valign="top"),
            size_hint=(0.8, 0.8),
        )
        popup.open()


class EnqueteScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        self.enquete_label = Label(text="Enquête : ", size_hint=(1, 0.1))
        layout.add_widget(self.enquete_label)

        self.details_label = Label(
            text="Détails de l'enquête",
            size_hint=(1, 0.5),
            halign="left",
            valign="top",
            text_size=(400, None),
        )
        layout.add_widget(self.details_label)

        buttons_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        personnes_btn = Button(
            text="Voir Personnes Impliquées",
            size_hint=(1, 0.1),
            height=40,  # Fixe la hauteur du bouton
        )
        personnes_btn.bind(on_release=self.afficher_personnes)
        buttons_layout.add_widget(personnes_btn)

        preuves_btn = Button(
            text="Voir Preuves",
            size_hint=(1, 0.1),
            height=40,
        )
        preuves_btn.bind(on_release=self.afficher_preuves)
        buttons_layout.add_widget(preuves_btn)

        layout.add_widget(buttons_layout)

        layout.add_widget(
            Button(
                text="Retour au menu principal",
                size_hint=(1, 0.1),
                on_release=self.go_back_to_menu,
            )
        )

        self.add_widget(layout)
        self.enquete = None

    def set_enquete(self, enquete):
        """Affiche les détails de l'enquête sélectionnée avec un ScrollView si nécessaire."""
        self.enquete = enquete

        # Réinitialisation de la mise en page
        self.clear_widgets()
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Titre de l'enquête
        layout.add_widget(Label(
            text=f"Enquête : {enquete['nom']}",
            font_size=24,
            size_hint=(1, 0.1),
            halign="center",
            valign="middle"
        ))

        # Création d'un conteneur pour les détails
        content_layout = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10)
        content_layout.bind(minimum_height=content_layout.setter("height"))

        # Ajouter les informations principales
        content_layout.add_widget(Label(
            text=f"[b]ID :[/b] {enquete['id']}",
            markup=True,
            font_size=18,
            size_hint_y=None,
            height=40
        ))
        content_layout.add_widget(Label(
            text=f"[b]Dates :[/b] {enquete['date_de_debut']} - {enquete['date_de_fin']}",
            markup=True,
            font_size=18,
            size_hint_y=None,
            height=40
        ))

        # Description si disponible
        if 'description' in enquete:
            content_layout.add_widget(Label(
                text=f"[b]Description :[/b] {enquete['description']}",
                markup=True,
                font_size=16,
                size_hint_y=None,
                height=60
            ))

        # Nombre de preuves
        content_layout.add_widget(Label(
            text=f"[b]Preuves :[/b] {len(enquete.get('liste_preuves', []))}",
            markup=True,
            font_size=18,
            size_hint_y=None,
            height=40
        ))

        # Nombre de personnes impliquées
        content_layout.add_widget(Label(
            text=f"[b]Personnes impliquées :[/b] {len(enquete.get('personne_impliquee', []))}",
            markup=True,
            font_size=18,
            size_hint_y=None,
            height=40
        ))

        # Création d'une ScrollView, uniquement si nécessaire
        if content_layout.height > self.height * 0.7:  # Vérifie si le contenu dépasse
            scroll = ScrollView(size_hint=(1, 0.7))
            scroll.add_widget(content_layout)
            layout.add_widget(scroll)
        else:
            layout.add_widget(content_layout)

        # Boutons pour actions
        buttons_layout = BoxLayout(size_hint=(1, 0.1))

        personnes_btn = Button(
            text="Voir Personnes Impliquées",
            size_hint=(1, 0.1),
            height=40,  # Fixe la hauteur du bouton
        )
        personnes_btn.bind(on_release=self.afficher_personnes)
        buttons_layout.add_widget(personnes_btn)

        preuves_btn = Button(
            text="Voir Preuves",
            size_hint=(1, 0.1),
            height=40,  # Fixe la hauteur du bouton
        )
        preuves_btn.bind(on_release=self.afficher_preuves)
        buttons_layout.add_widget(preuves_btn)

        layout.add_widget(buttons_layout)

        # Bouton pour retourner au menu principal
        retour_btn = Button(
            text="Retour au menu principal",
            size_hint=(1, 0.1),
            on_release=self.go_back_to_menu
        )
        layout.add_widget(retour_btn)

        self.add_widget(layout)

    def show_section(self, instance):
        self.content_label.text = f"Section {instance.text} de l'enquête sélectionnée."

    def afficher_preuves(self, instance):
        if not self.enquete.get("liste_preuves"):
            self.afficher_popup("Preuves", "Aucune preuve disponible.")
            return

    def afficher_personnes(self, instance):
        """Affiche les personnes impliquées dans un Popup."""
        if not self.enquete.get("personne_impliquee"):
            self.afficher_popup("Personnes impliquées", "Aucune personne impliquée.")
            return

        # Conteneur principal pour le contenu du Popup
        content = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # ScrollView pour afficher les personnes impliquées
        scroll = ScrollView(size_hint=(1, 0.8))
        layout = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10)
        layout.bind(minimum_height=layout.setter("height"))

        # Ajouter un bouton pour chaque personne impliquée
        for personne in self.enquete["personne_impliquee"]:
            nom_complet = f"{personne['prenom']} {personne['nom']}"
            btn = Button(
                text=nom_complet,
                size_hint_y=None,
                height=50,
                background_normal="",
                background_color=(0.2, 0.6, 0.8, 1),
            )
            btn.bind(on_release=lambda instance, p=personne: self.afficher_details_item(p))
            layout.add_widget(btn)

        scroll.add_widget(layout)
        content.add_widget(scroll)

        # Bouton pour fermer le Popup
        close_button = Button(
            text="Fermer",
            size_hint=(1, 0.2),
            background_normal="",
            background_color=(0.9, 0.2, 0.2, 1),
        )
        close_button.bind(on_release=lambda instance: popup.dismiss())
        content.add_widget(close_button)

        # Création et affichage du Popup
        popup = Popup(
            title="Personnes impliquées",
            content=content,
            size_hint=(0.8, 0.8),
            auto_dismiss=True,
        )
        popup.open()

    def afficher_details_item(self, item):
        """Affiche les détails d'une personne impliquée dans un Popup."""
        # Formater les détails
        details = "\n".join([f"[b]{k}:[/b] {v}" for k, v in item.items()])
        content = Label(
            text=details,
            markup=True,
            halign="left",
            valign="top",
            size_hint_y=None,
            text_size=(400, None),
        )
        content.bind(
            size=lambda instance, value: setattr(instance, "height", value[1])
        )

        # ScrollView pour gérer les textes longs
        scroll = ScrollView(size_hint=(1, 0.8))
        scroll.add_widget(content)

        # Bouton pour fermer le Popup
        close_button = Button(
            text="Fermer",
            size_hint=(1, 0.2),
            background_normal="",
            background_color=(0.9, 0.2, 0.2, 1),
        )
        close_button.bind(on_release=lambda instance: popup.dismiss())

        # Conteneur principal
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        layout.add_widget(scroll)
        layout.add_widget(close_button)

        # Affichage du Popup
        popup = Popup(
            title=f"Détails de {item.get('prenom', 'Personne')} {item.get('nom', '')}",
            content=layout,
            size_hint=(0.8, 0.8),
            auto_dismiss=True,
        )
        popup.open()

    def afficher_popup(self, titre, contenu):
        popup = Popup(
            title=titre,
            content=Label(text=contenu),
            size_hint=(0.8, 0.8),
            auto_dismiss=True,
        )
        popup.open()



class GlobalScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        self.section_label = Label(text="Section globale : ", size_hint=(1, 0.1))
        layout.add_widget(self.section_label)

        self.scroll_view = ScrollView(size_hint=(1, 0.8))
        self.content_layout = BoxLayout(
            orientation="vertical", size_hint_y=None, spacing=10, padding=10
        )
        self.content_layout.bind(minimum_height=self.content_layout.setter("height"))
        self.scroll_view.add_widget(self.content_layout)
        layout.add_widget(self.scroll_view)

        retour_btn = Button(text="Retour au menu principal", size_hint=(1, 0.1))
        retour_btn.bind(on_release=self.go_back_to_menu)
        layout.add_widget(retour_btn)

        self.add_widget(layout)

    def afficher_details_item(self, item):
        details = "\n".join([f"{k}: {v}" for k, v in item.items()])
        content = BoxLayout(orientation="vertical", spacing=10, padding=10)
        scroll = ScrollView(size_hint=(1, 0.8))
        details_label = Label(
            text=details,
            size_hint_y=None,
            text_size=(400, None),
            halign="left",
            valign="top",
        )
        details_label.bind(
            size=lambda instance, value: setattr(details_label, "height", value[1])
        )
        scroll.add_widget(details_label)
        content.add_widget(scroll)

        close_button = Button(text="Fermer", size_hint=(1, 0.2))
        close_button.bind(on_release=lambda instance: popup.dismiss())
        content.add_widget(close_button)

        popup = Popup(
            title=f"Détails de {item.get('nom', 'élément')}",
            content=content,
            size_hint=(0.8, 0.8),
            auto_dismiss=True,
        )
        popup.open()

    def set_section(self, section_name):
        self.section_label.text = f"Section globale : {section_name}"
        personnes = charger_donnees("fichiers/personnes.json")
        sections = organiser_par_section(
            personnes, chemin_preuves="fichiers/preuves.json"
        )
        self.content_layout.clear_widgets()

        for item in sections[section_name]:
            texte = item.get(
                "nom", f"{item.get('prenom', '')} {item.get('nom', '')}"
            ).strip()
            btn = Button(
                text=texte,
                size_hint=(1, None),
                height=40,
                background_normal="",
                background_color=(0.7, 0.7, 0.7, 1),
            )
            btn.bind(on_release=lambda instance, i=item: self.afficher_details_item(i))
            self.content_layout.add_widget(btn)


class PoliceManagementApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        self.menu_principal_screen = MenuPrincipalScreen(name="menu_principal")
        self.enquete_screen = EnqueteScreen(name="enquete")
        self.global_screen = GlobalScreen(name="global")

        self.screen_manager.add_widget(self.menu_principal_screen)
        self.screen_manager.add_widget(self.enquete_screen)
        self.screen_manager.add_widget(self.global_screen)

        return self.screen_manager


if __name__ == "__main__":
    PoliceManagementApp().run()
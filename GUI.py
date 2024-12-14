from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
import json


def charger_donnees(chemin_fichier):
    with open(chemin_fichier, "r", encoding="utf-8") as fichier:
        return json.load(fichier)


def organiser_par_section(donnees, chemin_preuves=None):
    sections = {
        "Employés": [],
        "Criminels": [],
        "Suspects": [],
        "Témoins": [],
        "Preuves": [],
    }
    for personne in donnees:
        classe = personne.get("classe", "Inconnu")
        if classe == "Employe":
            sections["Employés"].append(personne)
        elif classe == "Suspect":
            sections["Suspects"].append(personne)
        elif classe == "Criminel":
            sections["Criminels"].append(personne)

    if chemin_preuves:
        preuves = charger_donnees(chemin_preuves)
        sections["Preuves"].extend(preuves)

    return sections


class MenuPrincipalScreen(Screen):
    """Écran principal avec la liste des enquêtes et accès global."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Section des enquêtes
        layout.add_widget(Label(text="Choisissez une enquête", size_hint=(1, 0.1)))
        scroll = ScrollView(size_hint=(1, 0.5))
        scroll_content = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10)
        scroll_content.bind(minimum_height=scroll_content.setter("height"))

        for i in range(10):
            btn = Button(text=f"Enquête {i + 1}", size_hint_y=None, height=40)
            btn.bind(on_release=self.switch_to_enquete_screen)
            scroll_content.add_widget(btn)

        scroll.add_widget(scroll_content)
        layout.add_widget(scroll)

        # Accès global
        buttons_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)
        sections = ["Employés", "Criminels", "Suspects", "Témoins", "Preuves"]
        for section in sections:
            btn = Button(text=section)
            btn.bind(on_release=self.switch_to_global_section)
            buttons_layout.add_widget(btn)
        layout.add_widget(buttons_layout)

        self.add_widget(layout)

    def switch_to_enquete_screen(self, instance):
        app = App.get_running_app()
        app.root.current = "enquete"
        app.enquete_screen.set_enquete(instance.text)

    def switch_to_global_section(self, instance):
        app = App.get_running_app()
        app.global_screen.set_section(instance.text)
        app.root.current = "global"


class EnqueteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        self.enquete_label = Label(text="Enquête : ", size_hint=(1, 0.1))
        self.layout.add_widget(self.enquete_label)

        buttons_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        self.sections = ["Employés", "Criminels", "Suspects", "Témoins", "Preuves"]
        for section in self.sections:
            btn = Button(text=section)
            btn.bind(on_release=self.show_section)
            buttons_layout.add_widget(btn)
        self.layout.add_widget(buttons_layout)

        self.content_label = Label(
            text="Détails spécifiques à l'enquête...", size_hint=(1, 0.7)
        )
        self.layout.add_widget(self.content_label)

        self.layout.add_widget(
            Button(
                text="Retour au menu principal",
                size_hint=(1, 0.1),
                on_release=self.go_back_to_menu,
            )
        )

        self.add_widget(self.layout)

    def set_enquete(self, enquete_name):
        self.enquete_label.text = f"Enquête : {enquete_name}"

    def show_section(self, instance):
        self.content_label.text = f"Section {instance.text} de l'enquête sélectionnée."

    def go_back_to_menu(self, instance):
        app = App.get_running_app()
        app.root.current = "menu_principal"


class GlobalScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        self.section_label = Label(text="Section globale : ", size_hint=(1, 0.1))
        self.layout.add_widget(self.section_label)

        self.scroll_view = ScrollView(size_hint=(1, 0.8))
        self.content_layout = BoxLayout(
            orientation="vertical", size_hint_y=None, spacing=10, padding=10
        )
        self.content_layout.bind(minimum_height=self.content_layout.setter("height"))
        self.scroll_view.add_widget(self.content_layout)
        self.layout.add_widget(self.scroll_view)

        bottom_bar = BoxLayout(size_hint=(1, 0.1))
        retour_btn = Button(text="Retour au menu principal", size_hint=(1, 1))
        retour_btn.bind(on_release=self.go_back_to_menu)
        bottom_bar.add_widget(retour_btn)
        self.layout.add_widget(bottom_bar)

        self.add_widget(self.layout)

    def afficher_details_item(self, item):
        """Affiche un pop-up contenant les détails d'un item sélectionné (personne ou preuve)."""
        # Construire les détails sous forme de texte
        details = "\n".join([f"{k}: {v}" for k, v in item.items()])

        # Contenu principal du pop-up
        content = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Ajouter un scrollview pour afficher les détails
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

        # Bouton pour fermer le pop-up
        close_button = Button(text="Fermer", size_hint=(1, 0.2))
        close_button.bind(on_release=lambda instance: popup.dismiss())
        content.add_widget(close_button)

        # Création du pop-up
        popup = Popup(
            title=(
                f"Détails de {item['nom']}" if "nom" in item else "Détails de l'élément"
            ),
            content=content,
            size_hint=(0.8, 0.8),
            auto_dismiss=True,
        )
        popup.open()

    def set_section(self, section_name):
        """Met à jour l'écran pour afficher une section globale."""
        self.section_label.text = f"Section globale : {section_name}"

        # Charger les données des personnes et des preuves
        personnes = charger_donnees("fichiers/personnes.json")
        sections = organiser_par_section(
            personnes, chemin_preuves="fichiers/preuves.json"
        )

        # Effacer l'ancien contenu
        self.content_layout.clear_widgets()

        # Ajouter les items (personnes ou preuves) en boutons
        for item in sections[section_name]:
            # Si l'élément est une preuve, afficher son nom
            texte = (
                item["nom"]
                if section_name == "Preuves"
                else f"{item['prenom']} {item['nom']}"
            )
            btn = Button(
                text=texte,
                size_hint=(1, None),
                height=40,  # Petit rectangle
                background_normal="",
                background_color=(0.7, 0.7, 0.7, 1),  # Gris clair
            )
            btn.bind(on_release=lambda instance, i=item: self.afficher_details_item(i))
            self.content_layout.add_widget(btn)

    def go_back_to_menu(self, instance):
        app = App.get_running_app()
        app.root.current = "menu_principal"


class PoliceManagementApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.menu_principal_screen = MenuPrincipalScreen(name="menu_principal")
        self.screen_manager.add_widget(self.menu_principal_screen)

        self.enquete_screen = EnqueteScreen(name="enquete")
        self.screen_manager.add_widget(self.enquete_screen)

        self.global_screen = GlobalScreen(name="global")
        self.screen_manager.add_widget(self.global_screen)

        return self.screen_manager


if __name__ == "__main__":
    PoliceManagementApp().run()

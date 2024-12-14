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
        personnes_btn = Button(text="Personnes impliquées")
        personnes_btn.bind(on_release=self.afficher_personnes)
        buttons_layout.add_widget(personnes_btn)

        preuves_btn = Button(text="Preuves")
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
        self.enquete = enquete
        self.enquete_label.text = f"Enquête : {enquete['nom']}"
        self.details_label.text = (
            f"ID: {enquete['id']}\nDates: {enquete['date_de_debut']}"
        )

    def show_section(self, instance):
        self.content_label.text = f"Section {instance.text} de l'enquête sélectionnée."

    def afficher_personnes(self, instance):
        if not self.enquete.get("personne_impliquee"):
            self.afficher_popup("Personnes impliquées", "Aucune personne impliquée.")
            return

        content = BoxLayout(orientation="vertical", spacing=10, padding=10)
        scroll = ScrollView(size_hint=(1, 0.8))
        layout = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10)
        layout.bind(minimum_height=layout.setter("height"))

        for personne in self.enquete["personne_impliquee"]:
            btn = Button(
                text=f"{personne['prenom']} {personne['nom']}",
                size_hint_y=None,
                height=40,
            )
            btn.bind(
                on_release=lambda instance, p=personne: self.afficher_details_item(p)
            )
            layout.add_widget(btn)

        scroll.add_widget(layout)
        content.add_widget(scroll)

        content.add_widget(
            Button(
                text="Fermer",
                size_hint=(1, 0.2),
                on_release=lambda instance: popup.dismiss(),
            )
        )

        popup = Popup(
            title="Personnes impliquées", content=content, size_hint=(0.8, 0.8)
        )
        popup.open()

    def afficher_preuves(self, instance):
        if not self.enquete.get("liste_preuves"):
            self.afficher_popup("Preuves", "Aucune preuve disponible.")
            return

        content = BoxLayout(orientation="vertical", spacing=10, padding=10)
        scroll = ScrollView(size_hint=(1, 0.8))
        layout = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10)
        layout.bind(minimum_height=layout.setter("height"))

        for preuve in self.enquete["liste_preuves"]:
            btn = Button(text=f"Preuve ID: {preuve}", size_hint_y=None, height=40)
            btn.bind(
                on_release=lambda instance, p=preuve: self.afficher_details_item(p)
            )
            layout.add_widget(btn)

        scroll.add_widget(layout)
        content.add_widget(scroll)

        content.add_widget(
            Button(
                text="Fermer",
                size_hint=(1, 0.2),
                on_release=lambda instance: popup.dismiss(),
            )
        )

        popup = Popup(title="Preuves", content=content, size_hint=(0.8, 0.8))
        popup.open()

    def afficher_details_item(self, item):
        details = "\n".join([f"{k}: {v}" for k, v in item.items()])
        self.afficher_popup("Détails", details)

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
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from utilitaire.commandes_terminale import *


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

        self.close_button = Button(
            text="Fermer",
            size_hint=(1, None),
            background_normal="",
            background_color=(0.9, 0.2, 0.2, 1),
            height=50,
        )

        self.details_label = Label(
            text="Détails de l'enquête",
            size_hint=(1, 0.5),
            halign="left",
            valign="top",
            text_size=(400, None),
        )
        layout.add_widget(self.details_label)

        self.add_widget(layout)
        self.enquete = None

    def set_enquete(self, enquete):
        self.enquete = enquete

        # Réinitialisation de la mise en page
        self.clear_widgets()
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Titre de l'enquête
        layout.add_widget(
            Label(
                text=f"Enquête : {enquete['nom']}",
                font_size=24,
                size_hint=(1, 0.1),
                halign="center",
                valign="middle",
            )
        )

        # Création d'un conteneur pour les détails
        content_layout = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10)
        content_layout.bind(minimum_height=content_layout.setter("height"))

        # Ajouter les informations principales
        content_layout.add_widget(
            Label(
                text=f"[b]ID :[/b] {enquete['id']}",
                markup=True,
                font_size=18,
                size_hint_y=None,
                height=40,
            )
        )
        content_layout.add_widget(
            Label(
                text=f"[b]Dates :[/b] {enquete['date_de_debut']} - {enquete['date_de_fin']}",
                markup=True,
                font_size=18,
                size_hint_y=None,
                height=40,
            )
        )

        # Nombre de preuves
        content_layout.add_widget(
            Label(
                text=f"[b]Preuves :[/b] {len(enquete.get('liste_preuves', []))}",
                markup=True,
                font_size=18,
                size_hint_y=None,
                height=40,
            )
        )

        # Nombre de personnes impliquées
        content_layout.add_widget(
            Label(
                text=f"[b]Personnes impliquées :[/b] {len(enquete.get('personne_impliquee', []))}",
                markup=True,
                font_size=18,
                size_hint_y=None,
                height=40,
            )
        )

        # Nombre d'évènnement
        content_layout.add_widget(
            Label(
                text=f"[b]Liste d'évènnement :[/b] {len(enquete.get('liste_evenement', []))}",
                markup=True,
                font_size=18,
                size_hint_y=None,
                height=40,
            )
        )

        # Affichage des enquêtes liées
        enquetes_liees = enquete.get("enquetes_liees", [])
        if enquetes_liees:
            content_layout.add_widget(
                Label(
                    text="[b]Enquêtes liées :[/b]",
                    markup=True,
                    font_size=18,
                    size_hint_y=None,
                    height=40,
                )
            )
            for enquete_liee in enquetes_liees:
                # On suppose que chaque enquete_liee est un dictionnaire
                nom_enquete = enquete_liee.get("nom", "Nom non spécifié")

                # Ajoute le nom de l'enquête au contenu
                content_layout.add_widget(
                    Label(
                        text=f" - {nom_enquete}",
                        font_size=16,
                        size_hint_y=None,
                        height=30,
                    )
                )
        else:
            content_layout.add_widget(
                Label(
                    text="[b]Enquêtes liées :[/b] Aucune enquête liée",
                    markup=True,
                    font_size=18,
                    size_hint_y=None,
                    height=40,
                )
            )

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
            size_hint=(1, None),
            height=45,
            on_release=self.afficher_personnes,
        )
        buttons_layout.add_widget(personnes_btn)

        preuves_btn = Button(
            text="Voir Preuves",
            size_hint=(1, None),
            height=45,
            on_release=self.afficher_preuves,
        )
        buttons_layout.add_widget(preuves_btn)

        enquete_liee_btn = Button(
            text="Voir Enquêtes Liées",
            size_hint=(1, None),
            height=45,
            on_release=self.afficher_enquete_liee,
        )
        buttons_layout.add_widget(enquete_liee_btn)

        evennement_btn = Button(
            text="Voir Liste Des Evennements",
            size_hint=(1, None),
            height=45,
            on_release=self.afficher_liste_evennement,
        )
        buttons_layout.add_widget(evennement_btn)

        layout.add_widget(buttons_layout)

        # Bouton pour retourner au menu principal
        retour_btn = Button(
            text="Retour au menu principal",
            size_hint=(1, None),
            height=75,
            on_release=self.go_back_to_menu,
        )
        layout.add_widget(retour_btn)
        self.add_widget(layout)

    def show_section(self, instance):
        self.content_label.text = f"Section {instance.text} de l'enquête sélectionnée."

    def afficher_preuves(self, instance):
        """Affiche les preuves dans un Popup."""
        if not self.enquete.get("liste_preuves"):
            self.afficher_popup("Preuves", "Aucune preuve disponible.")
            return

        # Conteneur principal pour le contenu du Popup
        content = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # ScrollView pour afficher les personnes impliquées
        scroll = ScrollView(size_hint=(1, 0.8))
        layout = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10)
        layout.bind(minimum_height=layout.setter("height"))

        # Ajouter un bouton pour chaque preuve
        for preuve in self.enquete["liste_preuves"]:
            btn = Button(
                text=preuve["nom"],
                size_hint_y=None,
                height=50,
                background_normal="",
                background_color=(0.2, 0.6, 0.8, 1),
            )
            btn.bind(
                on_release=lambda instance, p=preuve: self.afficher_details_item(p)
            )
            layout.add_widget(btn)

        scroll.add_widget(layout)
        content.add_widget(scroll)

        if self.close_button.parent:
            self.close_button.parent.remove_widget(self.close_button)

        # Bouton pour fermer le Popup
        self.close_button.bind(on_release=lambda instance: popup.dismiss())
        content.add_widget(self.close_button)

        # Création et affichage du Popup
        popup = Popup(
            title="Preuves",
            content=content,
            size_hint=(0.8, 0.8),
            auto_dismiss=True,
        )
        popup.open()

    def afficher_enquete_liee(self, instance):
        if not self.enquete.get("enquetes_liees"):
            self.afficher_popup("Enquêtes liées", "Aucune enquête liée.")
            return

        content = BoxLayout(orientation="vertical", spacing=10, padding=10)
        scroll = ScrollView(size_hint=(1, 0.8))
        layout = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10)
        layout.bind(minimum_height=layout.setter("height"))

        for enquete in self.enquete["enquetes_liees"]:
            btn = Button(
                text=f"{enquete['nom']}",
                size_hint_y=None,
                height=50,
                background_normal="",
                background_color=(0.2, 0.6, 0.8, 1),
            )
            btn.bind(
                on_release=lambda instance, e=enquete: self.afficher_details_item(e)
            )
            layout.add_widget(btn)

        scroll.add_widget(layout)
        content.add_widget(scroll)

        if self.close_button.parent:
            self.close_button.parent.remove_widget(self.close_button)

        # Bouton pour fermer le Popup
        self.close_button.bind(on_release=lambda instance: popup.dismiss())
        content.add_widget(self.close_button)

        popup = Popup(title="Enquêtes liées", content=content, size_hint=(0.8, 0.8))
        popup.open()

    def afficher_liste_evennement(self, instance):
        if not self.enquete.get("liste_evenement"):
            self.afficher_popup("Enquêtes liées", "Aucun évennement trouvé.")
            return

        content = BoxLayout(orientation="vertical", spacing=10, padding=10)
        scroll = ScrollView(size_hint=(1, 0.8))
        layout = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10)
        layout.bind(minimum_height=layout.setter("height"))

        for evennement in self.enquete["liste_evenement"]:
            btn = Button(
                text=f"{evennement['nom']}",
                size_hint_y=None,
                height=50,
                background_normal="",
                background_color=(0.2, 0.6, 0.8, 1),
            )
            btn.bind(
                on_release=lambda instance, e=evennement: self.afficher_details_item(e)
            )
            layout.add_widget(btn)

        scroll.add_widget(layout)
        content.add_widget(scroll)

        if self.close_button.parent:
            self.close_button.parent.remove_widget(self.close_button)

        # Bouton pour fermer le Popup
        self.close_button.bind(on_release=lambda instance: popup.dismiss())
        content.add_widget(self.close_button)

        popup = Popup(
            title="Listes des évennements", content=content, size_hint=(0.8, 0.8)
        )
        popup.open()

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
                height=50,
                background_normal="",
                background_color=(0.2, 0.6, 0.8, 1),
            )
            btn.bind(
                on_release=lambda instance, p=personne: self.afficher_details_item(p)
            )
            layout.add_widget(btn)

        scroll.add_widget(layout)
        content.add_widget(scroll)

        if self.close_button.parent:
            self.close_button.parent.remove_widget(self.close_button)

        # Bouton pour fermer le Popup
        self.close_button.bind(on_release=lambda instance: popup.dismiss())
        content.add_widget(self.close_button)

        popup = Popup(
            title="Personnes impliquées", content=content, size_hint=(0.8, 0.8)
        )
        popup.open()

    def afficher_details_item(self, item):
        """Affiche les détails dans un Popup."""
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
        content.bind(size=lambda instance, value: setattr(instance, "height", value[1]))

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

        if "date_de_naissance" in item:
            popup = Popup(
                title=f"Détails de {item.get('prenom', 'Personne')} {item.get('nom', '')}",
                content=layout,
                size_hint=(0.8, 0.8),
                auto_dismiss=True,
            )
            popup.open()
        elif "date_preuve" in item:
            popup = Popup(
                title=f"Détails de la preuve '{item.get('nom')}'",
                content=layout,
                size_hint=(0.8, 0.8),
                auto_dismiss=True,
            )
            popup.open()
        else:
            popup = Popup(
                title=f"Détails de l'enquête liée'{item.get('nom')}'",
                content=layout,
                size_hint=(0.8, 0.8),
                auto_dismiss=True,
            )
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

        self.close_button.bind(on_release=lambda instance: popup.dismiss())
        content.add_widget(self.close_button)

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

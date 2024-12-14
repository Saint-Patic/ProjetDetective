from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


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

        # Exemples d'enquêtes
        for i in range(10):
            btn = Button(text=f"Enquête {i + 1}", size_hint_y=None, height=40)
            btn.bind(on_release=self.switch_to_enquete_screen)
            scroll_content.add_widget(btn)

        scroll.add_widget(scroll_content)
        layout.add_widget(scroll)

        # Accès global (Employés, Criminels, etc.)
        buttons_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)
        sections = ["Employés", "Criminels", "Suspects", "Témoins", "Preuves"]
        for section in sections:
            btn = Button(text=section)
            btn.bind(on_release=self.switch_to_global_section)
            buttons_layout.add_widget(btn)
        layout.add_widget(buttons_layout)

        self.add_widget(layout)

    def switch_to_enquete_screen(self, instance):
        """Passe à l'écran de gestion d'une enquête."""
        app = App.get_running_app()
        app.root.current = "enquete"
        app.enquete_screen.set_enquete(instance.text)

    def switch_to_global_section(self, instance):
        """Passe à une section globale (Employés, Criminels, etc.)."""
        app = App.get_running_app()
        app.global_screen.set_section(instance.text)
        app.root.current = "global"


class EnqueteScreen(Screen):
    """Écran de gestion d'une enquête spécifique."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        self.enquete_label = Label(text="Enquête : ", size_hint=(1, 0.1))
        self.layout.add_widget(self.enquete_label)

        # Boutons pour les sous-sections (Employés, Criminels, etc.)
        buttons_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        self.sections = ["Employés", "Criminels", "Suspects", "Témoins", "Preuves"]
        for section in self.sections:
            btn = Button(text=section)
            btn.bind(on_release=self.show_section)
            buttons_layout.add_widget(btn)
        self.layout.add_widget(buttons_layout)

        # Contenu de la section affichée
        self.content_label = Label(
            text="Détails spécifiques à l'enquête...", size_hint=(1, 0.7)
        )
        self.layout.add_widget(self.content_label)

        # Bouton de retour
        self.layout.add_widget(
            Button(
                text="Retour au menu principal",
                size_hint=(1, 0.1),
                on_release=self.go_back_to_menu,
            )
        )

        self.add_widget(self.layout)

    def set_enquete(self, enquete_name):
        """Met à jour l'écran avec l'enquête sélectionnée."""
        self.enquete_label.text = f"Enquête : {enquete_name}"

    def show_section(self, instance):
        """Affiche une section spécifique (Employés, Criminels, etc.)."""
        self.content_label.text = (
            f"Section {instance.text} de l'enquête sélectionnée.\n(Données ici...)"
        )

    def go_back_to_menu(self, instance):
        """Retourne au menu principal."""
        app = App.get_running_app()
        app.root.current = "menu_principal"


class GlobalScreen(Screen):
    """Écran global pour les listes (Employés, Criminels, etc.)."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        self.section_label = Label(text="Section globale : ", size_hint=(1, 0.1))
        self.layout.add_widget(self.section_label)

        # Placeholder pour le contenu
        self.content_label = Label(text="Détails globaux ici...", size_hint=(1, 0.8))
        self.layout.add_widget(self.content_label)

        # Bouton de retour
        self.layout.add_widget(
            Button(
                text="Retour au menu principal",
                size_hint=(1, 0.1),
                on_release=self.go_back_to_menu,
            )
        )

        self.add_widget(self.layout)

    def set_section(self, section_name):
        """Met à jour l'écran pour afficher une section globale."""
        self.section_label.text = f"Section globale : {section_name}"
        self.content_label.text = f"Liste globale de {section_name.lower()}."

    def go_back_to_menu(self, instance):
        """Retourne au menu principal."""
        app = App.get_running_app()
        app.root.current = "menu_principal"


class PoliceManagementApp(App):
    def build(self):
        # Gestion des écrans
        self.screen_manager = ScreenManager()

        # Écran principal
        self.menu_principal_screen = MenuPrincipalScreen(name="menu_principal")
        self.screen_manager.add_widget(self.menu_principal_screen)

        # Écran de gestion d'une enquête
        self.enquete_screen = EnqueteScreen(name="enquete")
        self.screen_manager.add_widget(self.enquete_screen)

        # Écran pour les sections globales
        self.global_screen = GlobalScreen(name="global")
        self.screen_manager.add_widget(self.global_screen)

        return self.screen_manager


if __name__ == "__main__":
    PoliceManagementApp().run()

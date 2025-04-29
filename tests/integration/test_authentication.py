import unittest
import time
import random
import string
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class AuthenticationTest(unittest.TestCase):
    """Tests d'intégration pour l'inscription et la connexion des utilisateurs."""
    
    def setUp(self):
        """Initialiser le navigateur avant chaque test."""
        # Créer un dossier pour les captures d'écran si nécessaire
        os.makedirs("screenshots", exist_ok=True)
        
        # Configuration des options Chrome
        chrome_options = Options()
        # Utiliser --headless pour les tests CI/CD
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        self.driver.get("http://localhost:5173/")
        
        # Délai d'attente explicite
        self.wait = WebDriverWait(self.driver, 15)
    
    def tearDown(self):
        """Nettoyer après chaque test."""
        if self.driver:
            self.driver.save_screenshot("screenshots/final_state.png")
            self.driver.quit()
    
    def generate_random_credentials(self, role="listener"):
        """Générer des informations aléatoires pour l'inscription."""
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return {
            'username': f"{role}_{random_suffix}",
            'email': f"{role}_{random_suffix}@example.com",
            'password': "Test123456!",
            'first_name': f"Test{role.capitalize()}",
            'last_name': "User",
            'birth_date': "1990-01-01",
            'favorite_genres': "Rock, Jazz, Pop" if role == "listener" else "Classical, Pop, Electronic",
            'role': role
        }
    
    def click_auth_button(self):
        """Cliquer sur le bouton d'authentification dans la navbar."""
        try:
            self.driver.save_screenshot("screenshots/before_auth_click.png")
            
            # Utiliser JavaScript pour trouver et cliquer sur le bouton d'authentification
            self.driver.execute_script("""
                const authButton = document.querySelector('.auth-button');
                if (authButton) {
                    authButton.click();
                } else {
                    throw new Error('Auth button not found');
                }
            """)
            
            # Attendre que le formulaire d'authentification apparaisse
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".auth-form-container")))
            self.driver.save_screenshot("screenshots/after_auth_click.png")
            return True
        except Exception as e:
            print(f"Erreur lors de l'ouverture du formulaire d'authentification: {str(e)}")
            self.driver.save_screenshot("screenshots/auth_click_error.png")
            return False
    
    def switch_to_register(self):
        """Passer du formulaire de connexion au formulaire d'inscription."""
        try:
            self.driver.save_screenshot("screenshots/before_mode_switch.png")
            
            # Attendre que le formulaire soit chargé
            time.sleep(1)
            
            # Utiliser JavaScript pour trouver et cliquer sur le lien "Create Account"
            self.driver.execute_script("""
                const switchLink = document.querySelector('.auth-switch .text-button');
                if (switchLink) {
                    switchLink.click();
                } else {
                    // Recherche alternative
                    const links = Array.from(document.querySelectorAll('button, a'));
                    const createAccountLink = links.find(link => 
                        link.textContent.includes('Create Account') || 
                        link.textContent.includes('Sign up') ||
                        link.textContent.includes('Register')
                    );
                    
                    if (createAccountLink) {
                        createAccountLink.click();
                    } else {
                        throw new Error('Register link not found');
                    }
                }
            """)
            
            # Attendre que le formulaire d'inscription apparaisse (vérifier la présence du champ email)
            self.wait.until(EC.presence_of_element_located((By.ID, "email")))
            self.driver.save_screenshot("screenshots/after_mode_switch.png")
            return True
        except Exception as e:
            print(f"Erreur lors du passage à l'inscription: {str(e)}")
            self.driver.save_screenshot("screenshots/mode_switch_error.png")
            return False
    
    def register_user(self, credentials):
        """Remplir et soumettre le formulaire d'inscription."""
        try:
            # Capturer l'état avant de commencer
            self.driver.save_screenshot("screenshots/before_registration.png")
            
            # Sélectionner le rôle si c'est un artiste
            if credentials['role'] == 'artist':
                try:
                    self.driver.execute_script("""
                        const artistRadio = document.querySelector('input[value="artist"]');
                        if (artistRadio) {
                            artistRadio.click();
                        } else {
                            throw new Error('Artist radio button not found');
                        }
                    """)
                    print("Rôle artiste sélectionné")
                except Exception as e:
                    print(f"Erreur lors de la sélection du rôle artiste: {str(e)}")
            
            # Remplir les champs obligatoires avec une approche plus robuste
            fields = [
                ("username", credentials['username']),
                ("email", credentials['email']),
                ("password", credentials['password']),
                ("confirmPassword", credentials['password'])
            ]
            
            # Ajouter les champs optionnels
            optional_fields = [
                ("firstName", credentials.get('first_name', '')),
                ("lastName", credentials.get('last_name', '')),
                ("birthDate", credentials.get('birth_date', '')),
                ("favoriteGenres", credentials.get('favorite_genres', ''))
            ]
            
            # Remplir tous les champs en utilisant JavaScript pour plus de fiabilité
            for field_id, value in fields + optional_fields:
                if value:  # Ne remplit que si la valeur n'est pas vide
                    try:
                        self.driver.execute_script(f"""
                            const field = document.getElementById('{field_id}');
                            if (field) {{
                                field.value = '{value}';
                                field.dispatchEvent(new Event('input', {{ bubbles: true }}));
                                field.dispatchEvent(new Event('change', {{ bubbles: true }}));
                            }}
                        """)
                        print(f"Champ {field_id} rempli avec '{value}'")
                    except Exception as e:
                        print(f"Erreur lors du remplissage du champ {field_id}: {str(e)}")
            
            # Capturer l'état après avoir rempli le formulaire
            self.driver.save_screenshot("screenshots/filled_form.png")
            
            # Rechercher et cliquer sur le bouton de soumission
            self.driver.execute_script("""
                // Chercher par différentes stratégies
                let submitButton = document.querySelector('.submit-button');
                
                if (!submitButton) {
                    // Chercher par texte
                    const buttons = Array.from(document.querySelectorAll('button'));
                    submitButton = buttons.find(button => 
                        button.textContent.includes('Create Account') || 
                        button.textContent.includes('Sign up') ||
                        button.textContent.includes('Register')
                    );
                }
                
                if (submitButton) {
                    console.log('Submit button found, clicking...');
                    submitButton.click();
                } else {
                    console.log('Submit button not found, trying form submit...');
                    const form = document.querySelector('form');
                    if (form) form.submit();
                    else throw new Error('No submit button or form found');
                }
            """)
            
            # Capture après avoir cliqué sur le bouton
            self.driver.save_screenshot("screenshots/after_submit_click.png")
            
            # Attendre le résultat (succès ou échec)
            time.sleep(5)  # Délai plus long pour s'assurer du traitement complet
            
            # Capturer l'état final pour diagnostiquer
            self.driver.save_screenshot("screenshots/registration_result.png")
            
            # Vérifier s'il y a un message d'erreur
            try:
                error_element = self.driver.find_element(By.CSS_SELECTOR, ".error-message")
                error_text = error_element.text
                print(f"Erreur d'inscription détectée: {error_text}")
                return False
            except NoSuchElementException:
                # Pas d'erreur visible, c'est bon signe
                pass
            
            # Vérifier si nous sommes connectés (chercher le menu utilisateur ou le nom d'utilisateur)
            page_source = self.driver.page_source
            is_logged_in = (
                credentials['username'] in page_source or 
                "user-menu" in page_source or 
                "logout" in page_source.lower()
            )
            
            if is_logged_in:
                print(f"Inscription réussie pour {credentials['role']}! L'utilisateur semble être connecté.")
                return True
            else:
                print(f"L'inscription de {credentials['role']} semble avoir échoué - aucun indicateur de connexion trouvé.")
                return False
            
        except Exception as e:
            print(f"Exception lors de l'inscription: {str(e)}")
            self.driver.save_screenshot("screenshots/registration_exception.png")
            return False
    
    def login_user(self, username, password):
        """Remplir et soumettre le formulaire de connexion."""
        try:
            self.driver.save_screenshot("screenshots/before_login.png")
            
            # Remplir les champs avec JavaScript
            self.driver.execute_script(f"""
                const usernameField = document.getElementById('username');
                const passwordField = document.getElementById('password');
                
                if (usernameField) {{
                    usernameField.value = '{username}';
                    usernameField.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
                
                if (passwordField) {{
                    passwordField.value = '{password}';
                    passwordField.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
            """)
            
            # Capturer le formulaire rempli
            self.driver.save_screenshot("screenshots/login_form_filled.png")
            
            # Cliquer sur le bouton de connexion
            self.driver.execute_script("""
                // Chercher par classe
                let loginButton = document.querySelector('.submit-button');
                
                if (!loginButton) {
                    // Chercher par texte
                    const buttons = Array.from(document.querySelectorAll('button'));
                    loginButton = buttons.find(button => 
                        button.textContent.includes('Login') || 
                        button.textContent.includes('Sign in')
                    );
                }
                
                if (loginButton) {
                    loginButton.click();
                } else {
                    const form = document.querySelector('form');
                    if (form) form.submit();
                    else throw new Error('No login button or form found');
                }
            """)
            
            # Attendre le résultat
            time.sleep(3)
            self.driver.save_screenshot("screenshots/after_login.png")
            
            # Vérifier si nous sommes connectés
            page_source = self.driver.page_source
            is_logged_in = (
                username in page_source or 
                "user-menu" in page_source or 
                "logout" in page_source.lower()
            )
            
            if is_logged_in:
                print(f"Connexion réussie avec {username}")
            else:
                print(f"Échec de connexion avec {username}")
                
            return is_logged_in
            
        except Exception as e:
            print(f"Exception lors de la connexion: {str(e)}")
            self.driver.save_screenshot("screenshots/login_exception.png")
            return False
    
    def logout_user(self):
        """Se déconnecter de l'application."""
        try:
            self.driver.save_screenshot("screenshots/before_logout.png")
            
            # Chercher et cliquer sur le bouton de déconnexion en utilisant JavaScript
            logout_success = self.driver.execute_script("""
                // Essayer d'abord de trouver un bouton de déconnexion direct
                let logoutButton = document.querySelector('.logout-button');
                
                if (!logoutButton) {
                    // Chercher par texte
                    const buttons = Array.from(document.querySelectorAll('button'));
                    logoutButton = buttons.find(button => 
                        button.textContent.includes('Logout') || 
                        button.textContent.includes('Sign out')
                    );
                }
                
                if (logoutButton) {
                    logoutButton.click();
                    return true;
                }
                
                // Essayer de cliquer sur le menu utilisateur d'abord
                const userMenu = document.querySelector('.user-menu, .username');
                if (userMenu) {
                    userMenu.click();
                    // Attendre un moment puis chercher le bouton de déconnexion
                    setTimeout(() => {
                        const logoutBtn = document.querySelector('.logout-button') || 
                                         Array.from(document.querySelectorAll('button')).find(btn => 
                                             btn.textContent.includes('Logout') || 
                                             btn.textContent.includes('Sign out')
                                         );
                        if (logoutBtn) logoutBtn.click();
                    }, 500);
                    return true;
                }
                
                return false;
            """)
            
            if not logout_success:
                print("Impossible de trouver un bouton de déconnexion")
                return False
            
            # Attendre que le bouton d'authentification réapparaisse
            time.sleep(2)
            self.driver.save_screenshot("screenshots/after_logout.png")
            
            # Vérifier que l'utilisateur est bien déconnecté
            is_logged_out = ".auth-button" in self.driver.page_source or "login" in self.driver.page_source.lower()
            
            if is_logged_out:
                print("Déconnexion réussie")
            else:
                print("Échec de déconnexion")
                
            return is_logged_out
            
        except Exception as e:
            print(f"Exception lors de la déconnexion: {str(e)}")
            self.driver.save_screenshot("screenshots/logout_exception.png")
            return False
    
    def test_listener_registration_and_login(self):
        """Test d'inscription et connexion d'un auditeur."""
        print("\n--- Test d'inscription et connexion d'un AUDITEUR ---")
        
        # Générer des identifiants aléatoires
        listener_credentials = self.generate_random_credentials(role="listener")
        print(f"Test avec username: {listener_credentials['username']}, email: {listener_credentials['email']}")
        
        # 1. Ouvrir le formulaire d'authentification
        auth_form_opened = self.click_auth_button()
        self.assertTrue(auth_form_opened, "Échec d'ouverture du formulaire d'authentification")
        
        # 2. Passer au formulaire d'inscription
        switched_to_register = self.switch_to_register()
        self.assertTrue(switched_to_register, "Échec de passage au formulaire d'inscription")
        
        # 3. Remplir le formulaire et s'inscrire en tant qu'auditeur
        registration_success = self.register_user(listener_credentials)
        
        # Si l'inscription échoue, essayer avec des identifiants simplifiés
        if not registration_success:
            print("Premier essai d'inscription échoué, tentative avec formulaire minimal...")
            
            # Recharger la page et réessayer
            self.driver.get("http://localhost:5173/")
            time.sleep(2)
            
            # Simplifier les identifiants pour la deuxième tentative
            minimal_credentials = {
                'username': f"listener_{random.randint(1000, 9999)}",
                'email': f"listener_{random.randint(1000, 9999)}@test.com",
                'password': "Password123!",
                'role': 'listener'
                # Pas de champs optionnels
            }
            
            print(f"Deuxième tentative avec: {minimal_credentials['username']}, {minimal_credentials['email']}")
            
            # Recommencer le processus
            self.click_auth_button()
            self.switch_to_register()
            registration_success = self.register_user(minimal_credentials)
            
            # Utiliser ces identifiants pour la suite si ça fonctionne
            if registration_success:
                listener_credentials = minimal_credentials
        
        # Vérifier que l'inscription a réussi
        self.assertTrue(registration_success, "L'inscription en tant qu'auditeur a échoué après multiples tentatives")
        
        # 4. Se déconnecter
        logout_success = self.logout_user()
        self.assertTrue(logout_success, "La déconnexion a échoué")
        
        # 5. Se reconnecter
        self.click_auth_button()
        login_success = self.login_user(listener_credentials['username'], listener_credentials['password'])
        self.assertTrue(login_success, "La connexion avec les identifiants créés a échoué")
        
        print("Test d'authentification d'auditeur réussi!")
    
    def test_artist_registration_and_login(self):
        """Test d'inscription et connexion d'un artiste."""
        print("\n--- Test d'inscription et connexion d'un ARTISTE ---")
        
        # Générer des identifiants aléatoires
        artist_credentials = self.generate_random_credentials(role="artist")
        print(f"Test avec username: {artist_credentials['username']}, email: {artist_credentials['email']}")
        
        # 1. Ouvrir le formulaire d'authentification
        auth_form_opened = self.click_auth_button()
        self.assertTrue(auth_form_opened, "Échec d'ouverture du formulaire d'authentification")
        
        # 2. Passer au formulaire d'inscription
        switched_to_register = self.switch_to_register()
        self.assertTrue(switched_to_register, "Échec de passage au formulaire d'inscription")
        
        # 3. Remplir le formulaire et s'inscrire en tant qu'artiste
        registration_success = self.register_user(artist_credentials)
        
        # Si l'inscription échoue, essayer avec des identifiants simplifiés
        if not registration_success:
            print("Premier essai d'inscription échoué, tentative avec formulaire minimal...")
            
            # Recharger la page et réessayer
            self.driver.get("http://localhost:5173/")
            time.sleep(2)
            
            # Simplifier les identifiants pour la deuxième tentative
            minimal_credentials = {
                'username': f"artist_{random.randint(1000, 9999)}",
                'email': f"artist_{random.randint(1000, 9999)}@test.com",
                'password': "Password123!",
                'role': 'artist'
                # Pas de champs optionnels
            }
            
            print(f"Deuxième tentative avec: {minimal_credentials['username']}, {minimal_credentials['email']}")
            
            # Recommencer le processus
            self.click_auth_button()
            self.switch_to_register()
            registration_success = self.register_user(minimal_credentials)
            
            # Utiliser ces identifiants pour la suite si ça fonctionne
            if registration_success:
                artist_credentials = minimal_credentials
        
        # Vérifier que l'inscription a réussi
        self.assertTrue(registration_success, "L'inscription en tant qu'artiste a échoué après multiples tentatives")
        
        # 4. Se déconnecter
        logout_success = self.logout_user()
        self.assertTrue(logout_success, "La déconnexion a échoué")
        
        # 5. Se reconnecter
        self.click_auth_button()
        login_success = self.login_user(artist_credentials['username'], artist_credentials['password'])
        self.assertTrue(login_success, "La connexion avec les identifiants créés a échoué")
        
        print("Test d'authentification d'artiste réussi!")

if __name__ == "__main__":
    unittest.main()
# import kivy
import requests
# from kivy.app import App
# from kivy.uix.label import Label
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.textinput import TextInput
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.button import Button
# from kivymd.uix.screen import Screen
from kivymd.uix.list import OneLineListItem, MDList, TwoLineListItem, ThreeLineListItem
from kivymd.uix.list import OneLineListItem, TwoLineAvatarListItem, ImageLeftWidget
# from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
# from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
# from kivy.factory import Factory
from kivy.properties import ObjectProperty
import os
from firebase_admin import credentials, initialize_app, storage
import json
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.image import AsyncImage

cred = credentials.Certificate("auth.json")
initialize_app(cred, {'storageBucket': 'pipai212.appspot.com'})

help_str = '''
ScreenManager:
    WelcomeScreen:
    MainScreen:
    LoginScreen:
    SignupScreen:
    ProfileScreen:
    MainScreenUser:
    MemberScreen:
    AddScreen:
    RemoveScreen:
    EditProfileScreen:
    ChangeNameScreen:
    ChangeEmailScreen:
    ChangePasswordScreen:
    ChangeAvatarScreen:
    HistoryScreen:
<WelcomeScreen>:
    name:'welcomescreen'
    Image:
        source: 'logo.png'
        pos_hint: {'center_x': 0.5,'center_y': 0.6}
        halign: 'center'
        size_hint: (0.2,0.2)
    MDLabel:
        text:'Smart Door Locking'
        font_style:'H2'
        halign:'center'
        pos_hint: {'center_y':0.8}
    MDFillRoundFlatButton:
        text:'Login'
        pos_hint : {'center_x':0.5,'center_y':0.25}
        size_hint: (0.13,0.1)
        on_press: 
            root.manager.current = 'loginscreen'
            root.manager.transition.direction = 'left'
        
    MDFillRoundFlatButton:
        text:'Signup'
        pos_hint : {'center_x':0.5,'center_y':0.4}
        size_hint: (0.13,0.1)
        on_press:
            root.manager.current = 'signupscreen'
            root.manager.transition.direction = 'left'

<LoginScreen>:
    name:'loginscreen'
    MDLabel:
        text:'Login'
        font_style:'H2'
        halign:'center'
        pos_hint: {'center_y':0.9}
    MDTextField:
        id:login_username
        pos_hint: {'center_y':0.6,'center_x':0.5}
        size_hint : (0.7,0.1)
        hint_text: 'Username'
        helper_text:'Required'
        helper_text_mode:  'on_error'
        icon_right: 'account'
        icon_right_color: app.theme_cls.primary_color
        required: True
        mode: "rectangle"
    MDTextField:
        id:login_password
        pos_hint: {'center_y':0.4,'center_x':0.5}
        size_hint : (0.7,0.1)
        hint_text: 'Password'
        helper_text:'Required'
        helper_text_mode:  'on_error'
        icon_right: 'key-variant'
        icon_right_color: app.theme_cls.primary_color
        required: True
        mode: "rectangle"
        password: True
    MDFillRoundFlatButton:
        text:'Login'
        size_hint: (0.13,0.07)
        pos_hint: {'center_x':0.5,'center_y':0.2}
        on_press:
            app.login()
            app.username_changer() 


    MDTextButton:
        text: 'Create an account'
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press:
            root.manager.current = 'signupscreen'
            root.manager.transition.direction = 'up'
<SignupScreen>:
    name:'signupscreen'
    MDLabel:
        text:'Signup'
        font_style:'H2'
        halign:'center'
        pos_hint: {'center_y':0.9}
    MDTextField:
        id:signup_fullname
        pos_hint: {'center_y':0.75,'center_x':0.5}
        size_hint : (0.7,0.1)
        hint_text: 'Fullname'
        helper_text:'Required'
        helper_text_mode:  'on_error'
        icon_right: 'account-circle-outline'
        icon_right_color: app.theme_cls.primary_color
        required: True
        mode: "rectangle"
    MDTextField:
        id:signup_username
        pos_hint: {'center_y':0.6,'center_x':0.5}
        size_hint : (0.7,0.1)
        hint_text: 'Username'
        helper_text:'Required'
        helper_text_mode:  'on_error'
        icon_right: 'account-circle'
        icon_right_color: app.theme_cls.primary_color
        required: True
        mode: "rectangle"
    MDTextField:
        id:signup_email
        pos_hint: {'center_y':0.45,'center_x':0.5}
        size_hint : (0.7,0.1)
        hint_text: 'Email'
        helper_text:'Required'
        helper_text_mode:  'on_error'
        icon_right: 'account'
        icon_right_color: app.theme_cls.primary_color
        required: True
        mode: "rectangle"
    MDTextField:
        id:signup_password
        pos_hint: {'center_y':0.3,'center_x':0.5}
        size_hint : (0.7,0.1)
        hint_text: 'Password'
        helper_text:'Required'
        helper_text_mode:  'on_error'
        icon_right: 'key-variant'
        icon_right_color: app.theme_cls.primary_color
        required: True
        mode: "rectangle"
        password: True
    MDFillRoundFlatButton:
        text:'Signup'
        size_hint: (0.13,0.07)
        pos_hint: {'center_x':0.5,'center_y':0.2}
        on_press: app.signup()
    MDTextButton:
        text: 'Already have an account'
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press:
            root.manager.current = 'loginscreen'
            root.manager.transition.direction = 'down'


<MainScreen>:
    name: 'mainscreen'
    MDLabel:
        id:username_info
        text:'Hello Main'
        font_style:'H3'
        halign:'center'
        pos_hint: {'center_y':0.8}
    MDFillRoundFlatButton:
        text:'Profile'
        size_hint: (0.3,0.07)
        pos_hint : {'center_x':0.5,'center_y':0.6}
        on_press: app.profile()
    MDFillRoundFlatButton:
        text:'History'
        size_hint: (0.3,0.07)
        pos_hint : {'center_x':0.5,'center_y':0.5}
        on_press: app.history()
    MDFillRoundFlatButton:
        text:'Member List'
        size_hint: (0.3,0.07)
        pos_hint : {'center_x':0.5,'center_y':0.4}
        on_press: app.member()
    MDFillRoundFlatButton:
        text:'Ét Ô Ét'
        size_hint: (0.3,0.07)
        pos_hint : {'center_x':0.5,'center_y':0.3}
        on_press: root.manager.current = 'profilescreen'
    MDTextButton:
        text: 'Log out'
        color: 1, 0, 0, 1
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: app.logout()

    
<MainScreenUser>:
    name: 'mainscreenuser'
    MDLabel:
        id:username_info
        text:'Hello Main'
        font_style:'H3'
        halign:'center'
        pos_hint: {'center_y':0.8}
    MDFillRoundFlatButton:
        text:'Profile'
        size_hint: (0.3,0.07)
        pos_hint : {'center_x':0.5,'center_y':0.6}
        on_press: app.profile()
    MDTextButton:
        text: 'Log out'
        color: 1, 0, 0, 1
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: app.logout()
        
<ProfileScreen>:
    name: 'profilescreen'
    MDLabel:
        id:profile_label
        text: 'Profile'
        halign:'center'
        font_style: 'H4'
        pos_hint: {'center_x':0.5, 'center_y':0.95}
    MDLabel:
        id:username_label
        text: 'Username:'
        halign:'center'
        font_style: 'H6'
        pos_hint: {'center_x':0.5, 'center_y':0.65}
    MDLabel:
        id:username_id
        halign:'center'
        pos_hint: {'center_x':0.5, 'center_y':0.6}
    MDLabel:
        id:email_label
        text: 'Email:'
        font_style: 'H6'
        halign:'center'
        pos_hint: {'center_x':0.5, 'center_y':0.55}
    MDLabel:
        id:email_id
        halign:'center'
        pos_hint: {'center_x':0.5, 'center_y':0.5}
    MDLabel:
        id:name_label
        text: 'Name:'
        font_style: 'H6'
        halign:'center'
        pos_hint: {'center_x':0.5, 'center_y':0.45}
    MDLabel:
        id:name_id
        halign:'center'
        pos_hint: {'center_x':0.5, 'center_y':0.4}
    MDLabel:
        id:role_label
        text: 'Role:'
        font_style: 'H6'
        halign:'center'
        pos_hint: {'center_x':0.5, 'center_y':0.35}
    MDLabel:
        id:role_id
        halign:'center'
        pos_hint: {'center_x':0.5, 'center_y':0.3}
    MDLabel:
        id:admin_label
        text: 'Admin:'
        font_style: 'H6'
        halign:'center'
        pos_hint: {'center_x':0.5, 'center_y':0.25}
    MDLabel:
        id:admin_id
        halign:'center'
        pos_hint: {'center_x':0.5, 'center_y':0.2}
    MDTextButton:
        text: 'Home'
        color: 1, 0, 0, 1
        pos_hint: {'center_x':0.3,'center_y':0.1}
        on_press: root.manager.current = 'mainscreen'
    MDTextButton:
        text: 'Edit'
        color: 1, 0, 0, 1
        pos_hint: {'center_x':0.7,'center_y':0.1}
        on_press: root.manager.current = 'editprofilescreen'
        
<MemberScreen>:
    name: 'memberscreen' 
    MDLabel:
        id:member_label
        text: 'List of member'
        halign:'center'
        font_style: 'H6'
        pos_hint: {'center_x':0.5, 'center_y':0.2}
    ScrollView:
        halign: 'center'
        MDList:
            id: container 
            halign: 'center'
            pos_hint: {'center_x':0.5, 'center_y':0.5}
    MDTextButton:
        text: 'Home'
        color: 1, 0, 0, 1
        pos_hint: {'center_x':0.3,'center_y':0.1}
        on_press: root.manager.current = 'mainscreen'
    MDTextButton:
        text: 'Add'
        color: 1, 0, 0, 1
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: app.addmember()
    MDTextButton:
        text: 'Remove'
        color: 1, 0, 0, 1
        pos_hint: {'center_x':0.7,'center_y':0.1}
        on_press: app.removemember()
        
<AddScreen>:
    name: 'addscreen' 
    MDLabel:
        id:member_label
        text: 'Enter account name'
        halign:'center'
        font_style: 'H6'
        pos_hint: {'center_x':0.5, 'center_y':0.3}
    ScrollView:
        halign: 'center'
        MDList:
            id: container 
            halign: 'center'
            pos_hint: {'center_x':0.5, 'center_y':0.5}    
    MDFillRoundFlatButton:
        text:'Add'
        size_hint: (0.3,0.07)
        pos_hint : {'center_x':0.8,'center_y':0.2}
        on_press: app.addmemberfirebase()
    MDTextButton:
        text: 'Home'
        color: 1, 0, 0, 1
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: root.manager.current = 'mainscreen'
    MDTextField:
        id:add_username
        pos_hint: {'center_y':0.2,'center_x':0.3}
        size_hint : (0.5,0.1)
        hint_text: 'Username'
        helper_text:'Required'
        helper_text_mode:  'on_error'
        required: True
        mode: "rectangle"
<RemoveScreen>:
    name: 'removescreen' 
    MDLabel:
        id:member_label
        text: 'Enter account name'
        halign:'center'
        font_style: 'H6'
        pos_hint: {'center_x':0.5, 'center_y':0.3}
    ScrollView:
        halign: 'center'
        MDList:
            id: container 
            halign: 'center'
            pos_hint: {'center_x':0.5, 'center_y':0.5}    
    MDFillRoundFlatButton:
        text:'Remove'
        size_hint: (0.3,0.07)
        pos_hint : {'center_x':0.8,'center_y':0.2}
        on_press: app.removememberfirebase()
    MDTextButton:
        text: 'Home'
        color: 1, 0, 0, 1
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: root.manager.current = 'mainscreen'
    MDTextField:
        id:remove_username
        pos_hint: {'center_y':0.2,'center_x':0.3}
        size_hint : (0.5,0.1)
        hint_text: 'Username'
        helper_text:'Required'
        helper_text_mode:  'on_error'
        required: True
        mode: "rectangle"
        
<EditProfileScreen>:
    name:'editprofilescreen'
    MDLabel:
        text:'Edit Profile'
        font_style:'H2'
        halign:'center'
        pos_hint: {'center_y':0.9}
    MDFillRoundFlatButton:
        text:'Change name'
        size_hint: (0.4,0.07)
        pos_hint : {'center_x':0.5,'center_y':0.6}
        on_press: root.manager.current = 'changenamescreen'
    MDFillRoundFlatButton:
        text:'Change email'
        size_hint: (0.4,0.07)
        pos_hint : {'center_x':0.5,'center_y':0.5}
        on_press: root.manager.current = 'changeemailscreen'
    MDFillRoundFlatButton:
        text:'Change password'
        size_hint: (0.4,0.07)
        pos_hint : {'center_x':0.5,'center_y':0.4}
        on_press: root.manager.current = 'changepasswordscreen'
    MDFillRoundFlatButton:
        text:'Change avatar'
        size_hint: (0.4,0.07)
        pos_hint : {'center_x':0.5,'center_y':0.3}
        on_press: root.manager.current = 'changeavatarscreen'
    MDTextButton:
        text: 'Back'
        color: 1, 0, 0, 1
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: root.manager.current = 'profilescreen'
        
<ChangeNameScreen>:
    name:'changenamescreen'
    MDLabel:
        text:'Change name'
        font_style:'H2'
        halign:'center'
        pos_hint: {'center_y':0.9}
    MDFillRoundFlatButton:
        text:'Change'
        size_hint: (0.3,0.07)
        pos_hint : {'center_x':0.8,'center_y':0.5}
        on_press: app.changename()
    MDTextField:
        id:change_username
        pos_hint: {'center_y':0.5,'center_x':0.3}
        size_hint : (0.5,0.1)
        hint_text: 'New fullname'
        helper_text:'Required'
        helper_text_mode:  'on_error'
        required: True
        mode: "rectangle"
    MDTextButton:
        text: 'Back'
        color: 1, 0, 0, 1
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: root.manager.current = 'editprofilescreen'
        
<ChangeEmailScreen>:
    name:'changeemailscreen'
    MDLabel:
        text:'Change email'
        font_style:'H2'
        halign:'center'
        pos_hint: {'center_y':0.9}
    MDFillRoundFlatButton:
        text:'Change'
        size_hint: (0.3,0.07)
        pos_hint : {'center_x':0.8,'center_y':0.5}
        on_press: app.changeemail()
    MDTextField:
        id:change_email
        pos_hint: {'center_y':0.5,'center_x':0.3}
        size_hint : (0.5,0.1)
        hint_text: 'New email'
        helper_text:'Required'
        helper_text_mode:  'on_error'
        required: True
        mode: "rectangle"
    MDTextButton:
        text: 'Back'
        color: 1, 0, 0, 1
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: root.manager.current = 'editprofilescreen'
        
<ChangePasswordScreen>:
    name:'changepasswordscreen'
    MDLabel:
        text:'Change password'
        font_style:'H2'
        halign:'center'
        pos_hint: {'center_y':0.9}
    MDFillRoundFlatButton:
        text:'Change'
        size_hint: (0.3,0.07)
        pos_hint : {'center_x':0.5,'center_y':0.4}
        on_press: app.changepassword()
    MDTextField:
        id:change_password
        pos_hint: {'center_x':0.5,'center_y':0.6}
        size_hint : (0.5,0.1)
        hint_text: 'Password'
        helper_text:'Required'
        helper_text_mode:  'on_error'
        required: True
        mode: "rectangle"
        password: True
    MDTextField:
        id:change_password_again
        pos_hint: {'center_x':0.5,'center_y':0.5}
        size_hint : (0.5,0.1)
        hint_text: 'Type password again'
        helper_text:'Required'
        helper_text_mode:  'on_error'
        required: True
        mode: "rectangle"
        password: True
    MDTextButton:
        text: 'Back'
        color: 1, 0, 0, 1
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: root.manager.current = 'editprofilescreen'
        
<ChangeAvatarScreen>:
    name:'changeavatarscreen'
    MDFillRoundFlatButton:
        text:'Open album'
        size_hint: (0.3,0.07)
        pos_hint : {'center_x':0.5,'center_y':0.5}
        on_press:  app.show_load()

    MDTextButton:
        text: 'Back'
        color: 1, 0, 0, 1
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: root.manager.current = 'editprofilescreen'
        
<HistoryScreen>:
    name: 'historyscreen' 
    MDLabel:
        id:history_label
        text: 'Access history'
        halign:'center'
        font_style: 'H6'
        pos_hint: {'center_x':0.5, 'center_y':0.2}
    ScrollView:
        halign: 'center'
        MDList:
            id: container 
            halign: 'center'
            pos_hint: {'center_x':0.5, 'center_y':0.5}
    MDTextButton:
        text: 'Home'
        color: 1, 0, 0, 1
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: root.manager.current = 'mainscreen'

<LoadDialog>:
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        FileChooserListView:
            id: filechooser

        BoxLayout:
            size_hint_y: None
            height: 30
            Button:
                text: "Cancel"
                on_release: app.dismiss_popup()

            Button:
                text: "Load"
                on_release: app.load(filechooser.path, filechooser.selection)
'''
class WelcomeScreen(Screen):
    pass
class MainScreen(Screen):
    pass
class MainScreenUser(Screen):
    pass
class LoginScreen(Screen):
    pass
class SignupScreen(Screen):
    pass
class ProfileScreen(Screen):
    pass
class MemberScreen(Screen):
    pass
class AddScreen(Screen):
    pass
class RemoveScreen(Screen):
    pass
class EditProfileScreen(Screen):
    pass
class ChangeNameScreen(Screen):
    pass
class ChangeEmailScreen(Screen):
    pass
class ChangePasswordScreen(Screen):
    pass
class ChangeAvatarScreen(Screen):
    pass
class HistoryScreen(Screen):
    pass
sm = ScreenManager()
sm.add_widget(WelcomeScreen(name = 'loginscreen'))
sm.add_widget(MainScreen(name = 'mainscreen'))
sm.add_widget(MainScreen(name = 'mainscreenuser'))
sm.add_widget(LoginScreen(name = 'loginscreen'))
sm.add_widget(SignupScreen(name = 'signupscreen'))
sm.add_widget(ProfileScreen(name = 'profilescreen'))
sm.add_widget(AddScreen(name = 'addscreen'))
sm.add_widget(RemoveScreen(name = 'removescreen'))
sm.add_widget(EditProfileScreen(name = 'editprofilescreen'))
sm.add_widget(ChangeNameScreen(name = 'changenamescreen'))
sm.add_widget(ChangeEmailScreen(name = 'changeemailscreen'))
sm.add_widget(ChangePasswordScreen(name = 'changepasswordscreen'))
sm.add_widget(ChangeAvatarScreen(name = 'changeavatarscreen'))
sm.add_widget(HistoryScreen(name = 'historyscreen'))


class MyApp(MDApp):
    def build(self):
        self.strng = Builder.load_string(help_str)
        self.url = "https://pipai212-default-rtdb.asia-southeast1.firebasedatabase.app/.json"
        return self.strng

    auth = 'qWHfUcSoXuqEmYzzm1yIsOamNCPrIfd0L85cQQN8'

    def signup(self):
        signupEmail = self.strng.get_screen('signupscreen').ids.signup_email.text
        signupPassword = self.strng.get_screen('signupscreen').ids.signup_password.text
        signupUsername = self.strng.get_screen('signupscreen').ids.signup_username.text
        signupFullname = self.strng.get_screen('signupscreen').ids.signup_fullname.text
        if signupEmail.split() == [] or signupPassword.split() == [] or signupUsername.split() == []:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Invalid Input', text='Please Enter a valid Input', size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        if len(signupUsername.split()) > 1:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Invalid Username', text='Please enter username without space',
                                   size_hint=(0.7, 0.2), buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        else:
            request = requests.get(self.url + '?auth=' + self.auth)
            data = request.json()
            usernames = set()
            for key, value in data.items():
                usernames.add(key)
            if signupUsername in usernames:
                cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
                self.dialog = MDDialog(title='Existed Username', text='This username has been used before',
                                       size_hint=(0.7, 0.2), buttons=[cancel_btn_username_dialogue])
                self.dialog.open()
            else:
                print(signupEmail, signupPassword)
                signup_info = str(
                    {f'\"{signupUsername}\":{{"Password":\"{signupPassword}\","Email":\"{signupEmail}\","Name":\"{signupFullname}\","Admin":0, "Link":0}}'})
                signup_info = signup_info.replace(".", "-")
                signup_info = signup_info.replace("\'", "")
                to_database = json.loads(signup_info)
                print((to_database))
                requests.patch(url=self.url, json=to_database)
                self.strng.get_screen('loginscreen').manager.current = 'loginscreen'

    def login(self):
        loginUsername = self.strng.get_screen('loginscreen').ids.login_username.text
        loginPassword = self.strng.get_screen('loginscreen').ids.login_password.text

        self.login_check = False
        supported_loginUsername = loginUsername.replace('.', '-')
        supported_loginPassword = loginPassword.replace('.', '-')

        request = requests.get(self.url + '?auth=' + self.auth)
        data = request.json()
        usernames = set()
        for key, value in data.items():
            usernames.add(key)

        if supported_loginUsername in usernames and supported_loginPassword == data[supported_loginUsername]['Password']:
            self.username = loginUsername
            self.login_check = True
            if data[supported_loginUsername]['Admin'] == 1:
                self.admin_check = True
                self.strng.get_screen('mainscreen').manager.current = 'mainscreen'
            else:
                self.strng.get_screen('mainscreenuser').manager.current = 'mainscreenuser'
        else:
            print("user no longer exists")

    def logout(self):
        self.username = None
        self.strng.get_screen('welcomescreen').manager.current = 'welcomescreen'

    def profile(self):
        request = requests.get(self.url + '?auth=' + self.auth)
        data = request.json()
        self.strng.get_screen('profilescreen').ids.username_id.text = f"{self.username}"
        self.strng.get_screen('profilescreen').ids.email_id.text = f"{data[self.username]['Email'].replace('-','.')}"
        self.strng.get_screen('profilescreen').ids.name_id.text = f"{data[self.username]['Name']}"
        self.strng.get_screen('profilescreen').ids.role_id.text = f"Admin" if f"{data[self.username]['Admin']}" == "1" else f"Member"
        if f"{data[self.username]['Admin']}" == "1":
            self.strng.get_screen('profilescreen').ids.admin_id.text = f"{self.username}"
        elif f"{data[self.username]['Admin']}" == "0":
            self.strng.get_screen('profilescreen').ids.admin_id.text = f"Do not belong"
        else:
            self.strng.get_screen('profilescreen').ids.admin_id.text = f"{data[self.username]['Admin']}"
        src = data[self.username]["Link"]
        if src == 0:
            src = "https://firebasestorage.googleapis.com/v0/b/pipai212.appspot.com/o/51e6kpkyuIL._AC_SL1200_.jpg?alt=media&token=9d179ce3-19b2-4cf3-af87-2b95defc843d"
        else:
            src = src.replace("-", ".")
        img = AsyncImage(source=src)
        img.pos_hint = {'center_x':0.5,'center_y':0.8}
        img.size_hint = (0.4,0.25)
        img.allow_stretch = True
        img.keep_ratio = False
        self.strng.get_screen('profilescreen').add_widget(img)
        self.strng.get_screen('profilescreen').manager.current = 'profilescreen'

    def member(self):
        request = requests.get(self.url + '?auth=' + self.auth)
        data = request.json()
        self.strng.get_screen('memberscreen').ids.container.clear_widgets()
        for i in data[self.username]['Member']:
            self.strng.get_screen('memberscreen').ids.container.add_widget(OneLineListItem(text=f"{i}"))
        self.strng.get_screen('memberscreen').manager.current = 'memberscreen'

    def addmember(self):
        request = requests.get(self.url + '?auth=' + self.auth)
        data = request.json()
        self.strng.get_screen('addscreen').ids.container.clear_widgets()
        for i in data[self.username]['Member']:
            self.strng.get_screen('addscreen').ids.container.add_widget(OneLineListItem(text=f"{i}"))
        self.strng.get_screen('addscreen').manager.current = 'addscreen'

    def addmemberfirebase(self):
        member = self.strng.get_screen('addscreen').ids.add_username.text
        info = str(
            {f'\"{member}\":"name"'})
        info = info.replace(".", "-")
        info = info.replace("\'", "")
        to_database = json.loads(info)
        url = "https://pipai212-default-rtdb.asia-southeast1.firebasedatabase.app/"
        res = requests.patch(url=url + f'{self.username}' + "/Member/.json", json=to_database)
        info = str(
            {f'"Admin":\"{self.username}\"'})
        info = info.replace(".", "-")
        info = info.replace("\'", "")
        to_database = json.loads(info)
        requests.patch(url = url + f'{member}' + "/.json", json = to_database)
        print(res)
        request = requests.get(self.url + '?auth=' + self.auth)
        data = request.json()
        self.strng.get_screen('memberscreen').ids.container.clear_widgets()
        for i in data[self.username]['Member']:
            self.strng.get_screen('memberscreen').ids.container.add_widget(OneLineListItem(text=f"{i}"))
        self.strng.get_screen('memberscreen').manager.current = 'memberscreen'

    def removemember(self):
        request = requests.get(self.url + '?auth=' + self.auth)
        data = request.json()
        self.strng.get_screen('removescreen').ids.container.clear_widgets()
        for i in data[self.username]['Member']:
            self.strng.get_screen('removescreen').ids.container.add_widget(OneLineListItem(text=f"{i}"))
        self.strng.get_screen('removescreen').manager.current = 'removescreen'

    def removememberfirebase(self):
        member = self.strng.get_screen('removescreen').ids.remove_username.text
        info = str(
            {f'\"{member}\":"name"'})
        info = info.replace(".", "-")
        info = info.replace("\'", "")
        to_database = json.loads(info)
        url = "https://pipai212-default-rtdb.asia-southeast1.firebasedatabase.app/"
        res = requests.delete(url=url +f'{self.username}' + "/Member/" +f'{member}' +".json")
        info = str(
            {f'"Admin":0'})
        info = info.replace(".", "-")
        info = info.replace("\'", "")
        to_database = json.loads(info)
        requests.patch(url=url + f'{member}' + "/.json", json=to_database)

        print(res)
        request = requests.get(self.url + '?auth=' + self.auth)
        data = request.json()
        self.strng.get_screen('memberscreen').ids.container.clear_widgets()
        for i in data[self.username]['Member']:
            self.strng.get_screen('memberscreen').ids.container.add_widget(OneLineListItem(text=f"{i}"))
        self.strng.get_screen('memberscreen').manager.current = 'memberscreen'

    def changename(self):
        name = self.strng.get_screen('changenamescreen').ids.change_username.text
        info = str(
            {f'"Name":\"{name}\"'})
        info = info.replace(".", "-")
        info = info.replace("\'", "")
        to_database = json.loads(info)
        url = "https://pipai212-default-rtdb.asia-southeast1.firebasedatabase.app/"
        res = requests.patch(url=url + f'{self.username}' + "/.json", json=to_database)
        self.profile()

    def changeemail(self):
        email = self.strng.get_screen('changeemailscreen').ids.change_email.text
        info = str(
            {f'"Email":\"{email}\"'})
        info = info.replace(".", "-")
        info = info.replace("\'", "")
        to_database = json.loads(info)
        url = "https://pipai212-default-rtdb.asia-southeast1.firebasedatabase.app/"
        res = requests.patch(url=url + f'{self.username}' + "/.json", json=to_database)
        self.profile()

    def changepassword(self):
        password = self.strng.get_screen('changepasswordscreen').ids.change_password.text
        password_again = self.strng.get_screen('changepasswordscreen').ids.change_password_again.text
        if password != password_again:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Wrong password', text='Password are not the same', size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        else:
            info = str(
                {f'"Password":\"{password}\"'})
            info = info.replace(".", "-")
            info = info.replace("\'", "")
            to_database = json.loads(info)
            url = "https://pipai212-default-rtdb.asia-southeast1.firebasedatabase.app/"
            res = requests.patch(url=url + f'{self.username}' + "/.json", json=to_database)
            self.profile()

    def history(self):
        request = requests.get(self.url + '?auth=' + self.auth)
        data = request.json()
        history = data["history"]
        self.strng.get_screen('historyscreen').ids.container.clear_widgets()
        count = 0
        for i in history:
            img = ImageLeftWidget(source = history[i]["link"].replace("-","."))
            str = i
            user = history[i]["user"]
            items = TwoLineAvatarListItem(text = str, secondary_text = user)
            items.add_widget(img)
            self.strng.get_screen('historyscreen').ids.container.add_widget(items)
            count +=1
        self.strng.get_screen('historyscreen').manager.current = 'historyscreen'

    def close_username_dialog(self, obj):
        self.dialog.dismiss()

    def username_changer(self):
        if self.login_check:
            request = requests.get(self.url + '?auth=' + self.auth)
            data = request.json()
            self.strng.get_screen('mainscreen').ids.username_info.text = f"Welcome {data[self.username]['Name']}"
            self.strng.get_screen('mainscreenuser').ids.username_info.text = f"Welcome {data[self.username]['Name']}"

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
    def load(self, path, filename):

        fileName = f'{os.path.join(path, filename[0])}'

        bucket = storage.bucket()
        blob = bucket.blob(fileName)
        blob.upload_from_filename(fileName)

        # Opt : if you want to make public access from the URL
        blob.make_public()
        print(blob.public_url)
        info = str(
            {f'"Link" : \"{blob.public_url}\"'})
        info = info.replace(".", "-")
        info = info.replace("\'", "")
        to_database = json.loads(info)
        url = "https://pipai212-default-rtdb.asia-southeast1.firebasedatabase.app/"
        res = requests.patch(url=url + f'{self.username}' + ".json", json=to_database)


        self.dismiss_popup()
        self.profile()

    def dismiss_popup(self):
        self._popup.dismiss()

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

if __name__ == "__main__":
    MyApp().run()

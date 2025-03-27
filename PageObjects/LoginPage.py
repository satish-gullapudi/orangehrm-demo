from PageObjects.BasePage import BasePage


class LoginPage(BasePage):
    section = "LOGIN_PAGE"

    def __init__(self, driver):
        super().__init__(driver)
    
    def enter_username(self, username):
        self.type_in_field(self.section, "user_name_input_field_xpath", username)
    
    def enter_password(self, password):
        self.type_in_field(self.section, "password_input_field_xpath", password)
    
    def click_login_submit_btn(self):
        self.click_element(self.section, "login_submit_btn_xpath")
    
    def login_application(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_submit_btn()
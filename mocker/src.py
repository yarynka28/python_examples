import configparser


class MyClass:
    def my_method(self):
        self.algor_conf = configparser.ConfigParser()
        self.algor_conf.read('./path')
        return self.algor_conf['DynamicProgramingParamaters']['wealth_state_total']
class Step:
    __answer_text = ''
    __send_buttons = False
    __buttons = []
    __client_answer_cases = []

    def set_answer_text(self, text):
        if isinstance(text, str):
            self.__answer_text = text
        else:
            raise TypeError('Answer text must be a "str" instance.')

    @property
    def answer_text(self):
        return self.__answer_text

    def set_send_buttons(self, boolean):
        if boolean:
            self.__send_buttons = True
        else:
            self.__send_buttons = False

    @property
    def send_buttons(self):
        return self.__send_buttons

    @property
    def buttons(self):
        return self.__buttons

    def set_buttons(self, buttons):
        if type(buttons) in (list, tuple, set) and all([isinstance(string, str) for string in buttons]):
            self.__buttons = buttons
        else:
            raise TypeError('Buttons must me a string collection.')

    def add_client_answer_case(self, method):
        # try:
        #     print(dir(self))
        #     print(method)
        #     # self.__client_answer_cases.append(method)
        # except AttributeError:
        #     raise ValueError(f'Answer case must be a method of {self.__name__}.')
        # except TypeError:
        #     raise ValueError(f'Answer case must be a function.')
        method(123)
    @property
    def client_answer_cases(self):
        return self.__client_answer_cases

import requests
import json

class Auth():
    def __init__(self, host, login, password):
        self.host=host
        self.login=login
        self.password=password
        self.set_token()

    def set_token(self):
       self.token=self.get_token()
       
    def get_token(self):
        ## Метод интеграции на сервере
        method='/v1/authorization/login'
        url = f'http://{self.host}:8090{method}'
        ## Заголовок для отправки в формате json
        headers = {'Content-type': 'application/json',  
                   'Accept': 'text/plain',
                   'Content-Encoding': 'utf-8'
                  }
        ## Данные тела запроса
        data ={"login": self.login,
               "password": self.password,
               "encryptionType": "None"
              }
        ## Формирование запроса
        response=requests.post(url, headers=headers, data = json.dumps(data))    ## Присвоил переменной данные ответа сервера объект JSON
        try:    ## Пытаемся перехватить ошибку если вместо json объектра сервер ответил кодом 200, но не вернул json объект 
            responseData = response.json()    ## Присвоил переменной данные ответа сервера объект JSON
        except:    ## Если возникает какая либо ошибка переменная принимает значение заглушки в JSON
            responseData={"accessToken": "None",
                          "currentServer": "Some Error with JSON object"}
        server_guid = responseData['currentServer'] ## Получаем GUID сервера
        token = responseData['accessToken']    ## Готовая конструкция для дальнейшего использования токена
        return token

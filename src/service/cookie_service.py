from flask import make_response, redirect, Response, request


class CookieService:
    def __init__(self):
        self.__cookie_config = {
            "httponly": True,
            "samesite": "Strict",
            "max_age": 1800
        }
        self.__cookie_name = ("status", "name", "midia_format", "error_msg")
    
    @property
    def cookie_config(self):
        return self.__cookie_config
    
    @property
    def cookie_name(self):
        return self.__cookie_name


    def set(self, midia_request: dict) -> Response:
        cookie = make_response(redirect("/resp"))
        if midia_request.get("status"):
            cookie.set_cookie("name", str(midia_request['name']), **self.cookie_config)
            cookie.set_cookie("midia_format", str(midia_request['midia_format'].value), **self.cookie_config)

        cookie.set_cookie("status", str(midia_request['status']), **self.cookie_config)
        cookie.set_cookie("error_msg", str(midia_request['error_msg']), **self.cookie_config)

        return cookie

    def get_all(self) -> dict:
        cookies = {}
        for cookie_key in self.cookie_name:
            cookies[cookie_key] = request.cookies.get(cookie_key, "")
        return cookies


    def clear_all(self, response) -> None:
        for cookie_key in self.cookie_name:
            response.delete_cookie(cookie_key)
        return response

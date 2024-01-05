from rxconfig import config
import reflex as rx
from creds import app_key, api_key
import requests
import json

class ButtonState(rx.State):
    text_value: str = "Time to Button Mash"

def index():
    return rx.vstack(
        rx.text(ButtonState.text_value),
        rx.button(
            "Looking Fancy",
            color_scheme="red", 
            size="lg",
            on_click=ButtonState.set_text_value(
                "You Punched that fancy pants"
            ),
        ),
    )


class State(rx.State):

    search_query: str
    search_results: list[dict]

    def search_monitors(self,):
        headers = {
            "DD-API-KEY": api_key,
            "DD-APPLICATION-KEY": app_key
        }
        response = requests.get(
            "https://api.datadoghq.com/api/v1/monitor/search",
            headers=headers,
            params={"query": self.search_query}
        )
        if response.status_code == 200:
            # print(response.json()['monitors'])
            self.search_results = response.json()['monitors']
                      
        else:
            print("you suck it didnt work")
            
def defeat():
    
    return rx.vstack(
        rx.button(
            "Click this to Submit",
            color_scheme="green",
            size="lg",
            on_click=State.search_monitors),

        rx.input(
            value=State.search_query,
            on_change=State.set_search_query,
                ),
        rx.foreach(State.search_results, lambda result: rx.box(rx.text(result['name']), style={"box_shadow": "rgba(0, 0.67, 0.85, 0.89) 3px 5px 12px"})
             )
        )
           
app = rx.App()
app.add_page(index)
app.add_page(defeat)
app.compile()


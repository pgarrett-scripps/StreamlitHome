import dataclasses
import base64

import streamlit as st
from streamlit_card import card

st.set_page_config(layout="wide")


with open("background.jpg", "rb") as f:
    data = f.read()
    encoded = base64.b64encode(data)
data = "data:image/png;base64," + encoded.decode("utf-8")


st.title('Proteomics Tools')

# wide mode

CARD_STYLE = {
                "card": {
                    "width": "250px",
                    # <- make the card use the width of its container, note that it will not resize the height of the card automatically
                    "height": "250px",  # <- if you want to set the card height to 300px
                }
            }


@dataclasses.dataclass
class App:
    title: str
    desc: str
    image: str
    url: str
    styles: dict

apps = [
    App(title="PepFrag",
        desc="Peptide Fragment Ion Calculator",
        image=data,
        url="https://pep-frag.streamlit.app/",
        styles=CARD_STYLE),

    App(title="PdbCov",
        desc="3D Protein Coverage Analyzer",
        image=data,
        url="https://pdb-cov.streamlit.app/",
        styles=CARD_STYLE),

    App(title="DTA-PdbCov",
        desc="Pdb-Cov link generator for DtaSelectFilter files",
        image=data,
        url="https://dta-pdb-cov.streamlit.app/",
        styles=CARD_STYLE)
]

COLS = 5
cols = st.columns(COLS)
for i, app in enumerate(apps):
    with cols[i % COLS]:
        card(
            title=app.title,
            text=app.desc,
            image=app.image,
            url=app.url,
            styles=app.styles
        )

st.write("")
st.write("contact: pgarrett@scripps.edu")

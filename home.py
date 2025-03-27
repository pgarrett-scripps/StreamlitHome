from app_loader import AppLoader

import streamlit as st

st.set_page_config(
    page_title="ProteomicsTools",
    page_icon=":rocket:",
    layout="wide"
)


def custom_card(title, description, url, emoji, bg_color="#f0f8ff", height="350px", width="100%"):
    """
    Create a custom card component using st.markdown with emoji

    Args:
        title (str): Title of the card
        description (str): Description text for the card
        url (str): URL to link to when card is clicked
        emoji (str): Emoji to display on the card
        bg_color (str, optional): Background color of the card. Defaults to light blue.
        height (str, optional): Height of the card. Defaults to "300px".
        width (str, optional): Width of the card. Defaults to "100%".
    """
    # Custom CSS for the card with responsive design
    card_css = f"""
    <style>
    .custom-card-container {{
        display: flex;
        justify-content: center;
        margin-bottom: 15px;
        width: 100%;
    }}
    .custom-card {{
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        overflow: hidden;
        transition: transform 0.3s ease;
        height: {height};
        width: {width};
        max-width: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
        background-color: {bg_color};
        text-align: center;
        padding: 20px;
        box-sizing: border-box;
    }}
    .custom-card:hover {{
        transform: scale(1.03);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }}
    .card-emoji {{
        font-size: 64px;
        margin-bottom: 15px;
    }}
    .card-content {{
        display: flex;
        flex-direction: column;
        justify-content: flex-start;   /* Align cards to the top-left */
        align-items: center;
        height: 100%;
        width: 100%;
    }}
    .card-title {{
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 15px;
        width: 100%;
    }}
    .card-description {{
        font-size: 15px;
        color: #666;
        width: 100%;
    }}
    @media (max-width: 768px) {{
        .custom-card {{
            width: 100%;
            max-width: none;
        }}
    }}
    </style>
    """

    # Card HTML
    card_html = f"""
    {card_css}
    <div class="custom-card-container">
        <a href="{url}" target="_blank" style="text-decoration: none; color: inherit; width: 100%;">
            <div class="custom-card">
                <div class="card-emoji">{emoji}</div>
                <div class="card-content">
                    <div class="card-title">{title}</div>
                    <div class="card-description">{description}</div>
                </div>
            </div>
        </a>
    </div>
    """

    # Render markdown
    st.markdown(card_html, unsafe_allow_html=True)


# Example usage in your main script would replace the previous card() call:
@st.cache_resource
def render_apps(config):
    for i, category in enumerate(config['categories']):
        st.header(config['categories'][category], divider=True)
        apps = AppLoader.get_apps_by_category(config, category)

        COLS = 4
        cols = st.columns(COLS, vertical_alignment='top')
        for j, app in enumerate(apps):
            with cols[j % COLS]:
                custom_card(
                    title=app.title,
                    description=app.description,
                    url=app.url,
                    emoji=app.emoji,
                    bg_color="#f0f8ff",
                    height="270px",
                    width="100%"
                )


config = AppLoader.load_from_yaml('conf.yml')
render_apps(config)
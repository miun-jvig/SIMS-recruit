# style.py

def load_styles():
    return """
    <style>
    /* Ändra bakgrundsfärgen på hela sidan */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f0f2f6 !important; /* Bakgrundsfärg för hela applikationen */
    }

    .top-menu {
        background-color: #333;
        color: white;
        padding: 10px;
        font-size: 18px;
    }
    .top-menu a {
        color: white;
        text-decoration: none;
        margin-right: 20px;
        padding: 10px;
    }
    .top-menu a:hover {
        background-color: #575757;
        border-radius: 5px;
    }
    .profile {
        float: right;
    }
    .profile img {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        margin-left: 10px;
    }
     .side-menu {
        background-color: #6C4FA1;
        padding: 20px;
        border-radius: 20px;
        text-align: center;
    }
    .side-menu h2 {
        color: black !important; /* Tvingar rubriktexten till svart */
        text-align: center;
        font-size: 24px !important; /* Gör rubriken större */
        background-color: transparent !important; /* Förhindrar att rubrikens bakgrund ändras */
    }
    .stButton > button {
        width: 100%;
        padding: 12px;
        margin-bottom: 3px;
        background-color: #333;
        border: none;
        border-radius: 10px;
        color: white;
        font-size: 25px;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .content {
        padding: 20px;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .icon {
        width: 25px;
        height: 25px;
        margin-left: 10px;
    }
    </style>
    """

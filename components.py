import streamlit as st
from streamlit_lottie import st_lottie
import requests
from PIL import Image
import json
import pandas as pd

## names of the users
NAMES = ["sourabh", "sabarish", "raghav", "rakshith", "anirban", "sudhir",
         "rishabh"]

def _load_lottie_url(url):
    """Load the animation from the web link"""

    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def _load_lottie_file(path):
    """Load the animation from a json file"""
    with open(path, "r") as file:
        return json.load(file)


def header_content():
    """The header content below the title"""

    st.write("We'll write a silly/funny/witty story together. You write"
             " when you are tagged by someone. And then you tag someone "
             "else. The faster you write your bit, the sooner the next "
             "person can write theirs. There's no rule on how long you "
             "can take to write your bit, but of course, there's peer "
             "pressure.")
    st.write("-- Sabarish Vadarevu")


def load_animation_url(url, height):
    """Load a animation image"""

    animation = _load_lottie_url(url)
    st_lottie(animation, height=height)


def load_animation_path(path, height):
    """Load a animation image"""

    animation = _load_lottie_file(path)
    st_lottie(animation, height=height)


def load_images(image_names):
    """Load the images from the disk"""

    img_root_dir = "images/"
    images = []
    for image_name in image_names:
        img_path = img_root_dir + image_name
        images.append(Image.open(img_path))

    return images


def get_ordered_images():
    """Load the images in the order as the names"""

    names = get_names_in_order()
    image_names = [names[0] + '_2']  # fix the first ranker image
    image_names.extend(names[1:])

    image_names = map(lambda name: name+'.png', image_names)

    # load the images
    images = load_images(image_names)

    return images, [name.title() for name in names]


def get_names_in_order():
    """Return a list of names in the ranking order"""

    # todo: logic here
    return NAMES


def leaderboard(image, data, rank):
    """Control the leaderboard section"""

    img_col, _, tex_col = st.columns([1, 0.2, 2])
    with img_col:
        st.image(image, width=350)
    with tex_col:
        st.subheader(data)
        vote = st.slider("Rate", 0, 5, 0, key=f"slider_{rank}",
                         help='Provide vote')
        st.write(f"Your vote {vote}")


def get_user_name(disable):
    """Get the user name if he has not entered yet"""

    return st.selectbox("Please select yourself!",
                        [name.title() for name in NAMES],
                        disabled=disable,
                        help="You can select yourself only once. Please do not"
                             " choose yourself with different identity")


def get_database():
    """Get the database based on the present scenario"""



def update_slider():
    """Update the slider information based on the user"""


def restart_competition():
    """Operation when restart competition button is clicked"""
    restart = st.button("Restart Competition")
    if restart:
        st.write('Enter Password')





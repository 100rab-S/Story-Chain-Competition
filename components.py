import streamlit as st
from streamlit_lottie import st_lottie
import requests
from PIL import Image
import json
import pandas as pd


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


def get_ordered_images(df):
    """Load the images in the order as the names"""

    names = list(df.index)
    image_names = [names[0] + '_2']  # fix the first ranker image
    image_names.extend(names[1:])

    image_names = map(lambda name: name+'.png', image_names)
    # load the images
    images = load_images(image_names)

    return images


def _get_table(name, table):
    """Display a small table of all votes received by a person"""

    df = pd.DataFrame(table)
    df.index = [name.title() for name in df.index]
    df = df.rename(columns={name: "Points voted"})

    return df


def leaderboard(image, df, rank):
    """Control the leaderboard section"""

    row = df.iloc[rank - 1]
    name, data = row.name, row
    # get data for the slider
    if "user_name" in st.session_state: # if the user has been detected
        # Update the default value of sliders by the vote the user has provided
        slid_value = int(data[st.session_state.user_name.lower()])

    else:  # if the user has not been detected yet. Set the defaults to 0
        slid_value = 0

    img_col, _, text_col = st.columns([1, 0.2, 2])
    with img_col:
        st.image(image, width=350)

    with text_col:
        st.subheader(name.title())
        st.write(f"Total: {data['total']}")
        vote = st.slider("Rate", 0, 5, slid_value, key=f"slider_{name}",
                         help='Give vote', on_change=slider_callback,
                         kwargs={"name": name, "df": df})
        st.write(f"Your vote {vote}")

        # if more details are required
        if st.button("Show more details", key=f"table_{name}"):
            df = _get_table(name, data)
            st.write("Dataframe representing votes received from "
                     "different users")
            st.table(df)


def user_name_callback():
    """Deal with the user name callback"""

    if st.session_state.user_name_chosen:  # if the name is already chosen
        st.error("You have already chosen an Identity, cannot change it now!")
        st.session_state.name = st.session_state.user_name

    else:  # if the name is being chosen for the first time
        st.session_state.user_name_chosen = True
        st.session_state.user_name = st.session_state.name


def slider_callback(name, df):
    """Whenever the slider value changes this function is called"""

    # if user has not been detected yet
    if "user_name" not in st.session_state:
        st.error("Choose your identity to vote.")
        st.session_state[f"slider_{name}"] = 0  # set the slider back to zero

    # if the user is voting himself
    elif name == st.session_state.user_name.lower():
        st.error("You cannot vote yourself!")
        st.session_state[f"slider_{name}"] = 0  # set the slider to zero

    # if the user has been detected. update the database with the new values
    else:
        df.loc[name, st.session_state.user_name.lower()] = \
            st.session_state[f"slider_{name}"]
        save_dataset(df)


def _create_dataset(names):
    """Create a dataframe if it does not exist or is required to create new"""

    # remove the first name
    names = names[1:]
    df = pd.DataFrame(0, index=names, columns=names)
    df['total'] = df.sum(axis=1)

    return df


def load_dataset(names):
    """Load the dataset from the disk or create new dataset"""

    try:
        df = pd.read_csv("dataset/database.csv")
        df = df.set_index("Unnamed: 0")
        df['total'] = df.sum(axis=1)

    except FileNotFoundError:  # if no file then create a new file
        # should only run once in lifetime or to restart competition
        df = _create_dataset(names)

    # sort the dataframe based on the total vote
    df.sort_values('total', ascending=False, inplace=True)

    return df


def save_dataset(df):
    """Save the dataset to the disk"""

    # drop the total column
    df.drop('total', axis=1, inplace=True)
    df.to_csv("dataset/database.csv")


# def check_password():
#     """Returns `True` if the user had the correct password."""
#
#     def password_entered():
#         """Checks whether a password entered by the user is correct."""
#         if st.session_state["password"] == st.secrets["password"]:
#             st.session_state["password_correct"] = True
#             del st.session_state["password"]  # don't store password
#         else:
#             st.session_state["password_correct"] = False
#
#     if "password_correct" not in st.session_state:
#         # First run, show input for password.
#         st.text_input("Password", type="password", on_change=password_entered,
#                       key="password")
#         return False
#     elif not st.session_state["password_correct"]:
#         # Password not correct, show input + error.
#         st.text_input("Password", type="password", on_change=password_entered,
#                       key="password")
#         st.error("😕 Incorrect Password")
#         return False
#     else:
#         # Password correct.
#         reset_database()
#         return True
#
#
# def restart_competition():
#     """Operation when restart competition button is clicked"""
#     restart = st.button("Restart Competition", key='restart_button')
#     if ("restart_button" in st.session_state):
#         st.session_state["restart"] = False
#         password = st.text_input("Enter the password")
#         st.write("hello")
#         if password == st.secrets["password"]:
#             st.session_state["restart"] = True
#             st.write("Hurray!")
#             st.write(password)
#
#         else:
#             st.write("wrong password")









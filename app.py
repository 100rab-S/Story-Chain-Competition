import streamlit as st
import components as cp
import pandas as pd


# database for the application
# df = cp.get_database()

# Page related config
st.set_page_config(page_title="Akridata-DSA",
                   page_icon=":trophy:", layout="wide")

# --Load Assets
# won_anim_url = "https://assets5.lottiefiles.com/packages/lf20_cv6rdeii.json"
won_anim_file_path = "images/won.json"

##### ---Header Section
with st.container():
    col1, _, _, col4 = st.columns([2, 1, 0.5, 0.75])
    with col1:
        st.header('Story Chain Competition :trophy:')
    with col4:
        cp.restart_competition()

with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        cp.header_content()

    with right_column:
        cp.load_animation_path(won_anim_file_path, height=400)
        # st.write("Wow")

#### User login section ####
st.write("---")
st.header('Who are you?')

if "user_name" not in st.session_state:
    user_name = cp.get_user_name(disable=False)
    st.session_state.user_name = user_name

else:
    user_name = cp.get_user_name(disable=True)
    st.session_state.user_name = user_name
    st.write(f"Welcome {user_name}!")

st.write(st.session_state)

### add data to the sliders based on the user
# cp.update_slider(df)


##### -- Ranking section
with st.container():
    st.write("---")
    st.header("Leader-board")


# collect data from the user


# get the images in the ranking order
images, names = cp.get_ordered_images()

for rank, (image, name) in enumerate(zip(images, names), 1):  # iterate through the images and plot
    with st.container():
        st.write(f"Rank: {rank}")
        cp.leaderboard(image, name, rank)






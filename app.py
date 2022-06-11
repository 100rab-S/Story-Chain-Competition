import streamlit as st
import components as cp


# Page related config
st.set_page_config(page_title="Akridata-DSA",
                   page_icon=":trophy:", layout="wide")

# --Load Assets and define states
won_anim_file_path = "images/won.json"
NAMES = ["sourabh", "sabarish", "raghav", "rakshith", "anirban", "sudhir",
         "rishabh"]

if "user_name_chosen" not in st.session_state:
    st.session_state.user_name_chosen = False

if "greet_displayed" not in st.session_state:
    st.session_state.greet_displayed = False

# database for the application
df = cp.load_dataset(NAMES)

# st.write(st.session_state)

# ---Header Section
with st.container():
    col1, _, _, col4 = st.columns([2, 1, 0.5, 0.75])
    with col1:
        st.header('Story Chain Competition :trophy:')
    with col4:
        if st.button("Restart Competition"):
            st.write("Work in progress :hammer_and_wrench:")
        # if (st.button("Restart Competition", key="restart_button")) or \
        #     (st.session_state.restart_button):
        #     st.session_state.restart_button = True
        #     cp.check_password()
        # if st.button("Restart Competition"):
        #     st.session_state.check_pass = True
        #
        # if ("check_pass" in st.session_state) and \
        #         (st.session_state['check_pass']):
        #     cp.check_password()
        #     pass
        # cp.restart_competition()
        # if st.button("Restart Competition", key="restart") or \
        #         st.session_state['restart']:
        #     st.write(cp.check_password())
        # cp.check_password()

# ---- desc and animation
with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        cp.header_content()
    with right_column:
        cp.load_animation_path(won_anim_file_path, height=400)


# #### User login section ####
st.write("---")
st.header('Who are you?')
st.selectbox("Please select yourself", [name.title() for name in NAMES],
             on_change=cp.user_name_callback, key='name')

# greet the user
if ("user_name" in st.session_state) and (not st.session_state.greet_displayed):
    st.write(f"Welcome {st.session_state.user_name}!")
    st.session_state.greet_displayed = True

# st.write(st.session_state)
# st.dataframe(df)

# -- Ranking section
with st.container():
    st.write("---")
    st.header("Leader-board")

### Data for the sliders
# cp.update_slider(df)

# collect data from the user


# get the images in the ranking order
images = cp.get_ordered_images(df)

# iterate through the images and plot
for rank, (image, row) in enumerate(zip(images, df.iterrows()), 1):
    with st.container():
        st.write(f"Rank: {rank}")
        cp.leaderboard(image, row, rank)

# st.write(st.session_state)


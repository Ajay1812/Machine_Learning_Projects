
import streamlit as st

def update_first():
    st.session_state.second = st.session_state.first

def update_second():
    st.session_state.first = st.session_state.second

st.title('🪞 Mirrored Widgets using Session State')

st.text_input(label='Textbox 1', key='first', on_change=update_first)
st.text_input(label='Textbox 2', key='second', on_change=update_second)








# import streamlit as st

# select_box1 = st.sidebar.selectbox("Select an option for box 1", options=["Option 1", "Option 2", "Option 3"])
# select_box2 = st.sidebar.selectbox("Select an option for box 2", options=["Option A", "Option B", "Option C"])

# st.write("You selected option:", select_box1, "in box 1 and option:", select_box2, "in box 2")

# # Save the selected options to session state
# st.write("Session state", "Session state has been set")
# st.text("Select box 1: " + select_box1)
# st.text("Select box 2: " + select_box2)



# import streamlit as st

# # First select box
# options = ['Option 1', 'Option 2', 'Option 3']
# selected_option = st.cache(lambda: st.selectbox('Choose an option', options))

# checkbox_value = st.cache(lambda: st.checkbox('Check me'))

# # Second select box
# if checkbox_value:
#     options2 = ['Option A', 'Option B', 'Option C']
#     selected_option2 = st.selectbox('Choose another option', options2)
#     st.write(f'You selected: {selected_option2}')
#     st.write(checkbox_value)
# else:
#     st.write('The checkbox is not checked')


# checkbox_value_2 = st.cache(lambda: st.checkbox('Check me'))

# options_3 = ['Option 4', 'Option 5', 'Option 6']


# if checkbox_value_2:
#     options4 = ['Option 4', 'Option 5', 'Option 6']
#     selected_option_4 = st.selectbox('Choose another option', options4)
#     st.write(f'You selected: {selected_option_4}')
#     st.write(checkbox_value_2)
# else:
#     st.write('The checkbox is not checked')





# import streamlit as st

# options1 = ['option 1', 'option 2', 'option 3']
# options2 = ['apple', 'banana', 'cherry']

# selected_option1 = st.selectbox('Choose an option from list 1', options1, index=1)
# selected_option2 = st.selectbox('Choose an option from list 2', options2, index=2)

# st.write('You selected from list 1: ', selected_option1)
# st.write('You selected from list 2: ', selected_option2)

# import streamlit as st

# options = ['option 1', 'option 2', 'option 3']

# single_select = st.selectbox('Choose a single option:', options)
# multi_select = st.multiselect('Choose multiple options:', options)

# if single_select:
#     st.write('You selected a single option: ', single_select)
# if multi_select:
#     st.write('You selected multiple options: ', multi_select)



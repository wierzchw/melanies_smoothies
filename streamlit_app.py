# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize your smoothie! :cup_with_straw:")
st.write(
  """
  Choose the fruits you want in your custom smoothie.
  """
)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
# st.dataframe(data=my_dataframe, use_container_width=True)

name_on_order = st.text_input('Name on smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

ingredients_list = st.multiselect('Select up to 5 ingredients', my_dataframe, max_selections=5)
if ingredients_list:
    ingredients_string = ''
    for ingredient in ingredients_list:
        ingredients_string += ingredient + ' '
    # st.write(ingredients_string)

    time_to_insert = st.button('Submit order')
    
    if time_to_insert:
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """','""" + name_on_order + """')"""
        # st.write(my_insert_stmt)
        # st.stop()
        
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered '+name_on_order+'!', icon="✅")

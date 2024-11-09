# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Cutomize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
) 

#option = st.selectbox(
#    "What is your favorite fruit",
#    ("Banana", "Strawberries", "Peaches"),
#)

#st.write("You selected:", option)

name_on_smoothie = st.text_input("Name on Smoothie:")
st.write("Name on Smoothie will be:", name_on_smoothie)
#session = get_active_session()
cxn=st.connection("snowflake")
session = cxn.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect ("choose upto 5 ingredient", 
                                   my_dataframe,
                                   max_selections =5
                                  ) 

if ingredients_list:
    st.write (ingredients_list)
    st.text (ingredients_list)
    
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen +' '
    
    st.write (ingredients_string)
    st.text (ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_smoothie + """')"""

    st.write(my_insert_stmt)
    #if ingredients_string:
    #    session.sql(my_insert_stmt).collect()
    #    st.success('Your Smoothie is ordered!', icon="✅")

    time_to_submit = st.button ("Submit Order")
    if time_to_submit:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

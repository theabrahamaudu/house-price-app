import pandas as pd
import streamlit as st
import requests
df = pd.read_csv("./app/preprocessed_data.csv")


def run():
    st.image("https://seeafricatoday.com/wp-content/uploads/2020/06/Nigeira-mansion-2-1024x683.jpg")
    st.title("House Price App")
    st.subheader("Get an estimate of home prices in Nigeria")
    st.title("")
    st.text("Please enter your housing description")

    state = st.selectbox("State", sorted(df.state.unique()))

    town = st.selectbox("Town", sorted(df.town.unique()))

    house_type = st.selectbox("House Type", sorted(df.house_type.unique()))

    bedrooms = st.selectbox("Number of Bedrooms", sorted(df.bedrooms.unique()))

    toilets = st.selectbox("Number of Toilets", sorted(df.toilets.unique()))

    bathrooms = st.selectbox("Number of Bathrooms", sorted(df.bathrooms.unique()))

    parking_space = st.selectbox("Number of Parking Spaces", sorted(df.parking_space.unique()))

    data = {
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "toilets": toilets,
        "parking_space": parking_space,
        "house_type": house_type,
        "town": town,
        "state": state
        }

    if st.button("Get Price"):
        response = requests.post("http://127.0.0.1:8000/predict", json=data)

        prediction = response.text

        st.success(f"A {house_type} with your specifications in {town}, {state}\n"
                   f"will cost about ₦{float(prediction):,}")


if __name__=="__main__":
        run()
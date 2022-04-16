import streamlit as st
import requests
import stqdm

import streamlit as st
import datetime
from datetime import date
from dateutil import parser


#username = st.text_input('Enter your Username')

#if username in st.secrets["users"]["things_i_like"]:

    #st.write("My cool secrets:", st.secrets["my_cool_secrets"]["things_i_like"])

col1, col2 = st.columns(2)

with col1:
    #st.header()
    AppId = title = st.text_input('Enter your App ID')

with col2:
    #st.header()
    AppAPI = title = st.text_input('Enter your API Key')

with col1:
    #st.header()
    UsersCollectionId = title = st.text_input('Enter the ID of your users collections')


    #st.text("")
    #st.text("")
    #st.text("")
    #st.write("Learn how to get your user collection ID here [link](https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py)")



st.text("")
st.text("")
st.text("")

if 'var_list' not in st.session_state:
    st.session_state.var_list = {}

if 'records_list' not in st.session_state:
    st.session_state.records_list = []

if 'filteredrecords' not in st.session_state:
    st.session_state.filteredrecords = []

if 'finallistofemails' not in st.session_state:
    st.session_state.finallistofemails = []

if 'filters' not in st.session_state:
    st.session_state.filters = {}


if 'Date_filter_one' not in st.session_state:
    st.session_state.Date_filter_one = ""
if 'Bool_filter_one' not in st.session_state:
    st.session_state.Bool_filter_one = ""


if 'AppId' not in st.session_state:
    st.session_state.AppId = ""
if 'AppAPI' not in st.session_state:
    st.session_state.AppAPI = ""
if 'UsersCollectionId' not in st.session_state:
    st.session_state.UsersCollectionId = ""

if AppId:
    st.session_state.AppId = AppId
if AppAPI:
    st.session_state.AppAPI = AppAPI
if UsersCollectionId:
    st.session_state.UsersCollectionId = UsersCollectionId

if 'created_at_after' not in st.session_state:
    st.session_state.created_at_after = ""
if 'updated_at_after' not in st.session_state:
    st.session_state.updated_at_after = ""

with col1:
    if st.session_state.AppId and st.session_state.AppAPI and st.session_state.UsersCollectionId:

        #st.text("Data Entered")


        # Headers are fixed for all API calls
        headers = {
            'Authorization': f"Bearer {st.session_state.AppAPI}",
            "Content-Type": "application/json"
        }

        #Retrieve users properties
        url = f"https://api.adalo.com/v0/apps/{st.session_state.AppId}/collections/{st.session_state.UsersCollectionId}?offset=0&limit=100"
        response = requests.get(url, headers=headers)
        #st.write(response.json()["records"][0])
        st.session_state.var_list = response.json()["records"][0]


properties = []
for property, value in st.session_state.var_list.items():
    if type(value) is str :
        properties.append(property)






#with col2:
#    option = st.selectbox('select the user email property', properties)
#    st.session_state.Date_filter_one = option




with col1:
    created_at_after = st.date_input('Created After')
    created_at_after = str(created_at_after)+"T00:00:00.995"
    st.session_state.created_at_after = parser.parse(created_at_after)

    #st.text(st.session_state.created_at_after)

with col2:
    updated_at_after = st.date_input('Updated After')
    updated_at_after = str(updated_at_after)+"T00:00:00.995"
    st.session_state.updated_at_after = parser.parse(updated_at_after)

    #st.text(st.session_state.updated_at_after)


st.markdown("""---""")


records = []
with col2:
    if st.button("Retrieve All Users"):
        headers = {
            'Authorization': f"Bearer {st.session_state.AppAPI}",
            "Content-Type": "application/json"
        }
        for i in range(0, 3000, 100):
            url = f"https://api.adalo.com/v0/apps/{st.session_state.AppId}/collections/{st.session_state.UsersCollectionId}?offset={i}&limit=100"
            Property = st.session_state.Date_filter_one
            response = requests.get(url, headers=headers)
            for property in response.json()["records"]:
                records.append(property)

        st.session_state.records_list = records

    #This the final list of emails we're sending the emails to
emails = []

count = 0
for record in records:
    if st.session_state.updated_at_after   < parser.parse(record["updated_at"][:-1]) and st.session_state.created_at_after   < parser.parse(record["created_at"][:-1]):
            count += 1


import pandas as pd
df = pd.DataFrame.from_records(st.session_state.records_list)
#st.dataframe(df)

filters = {}
for column in df.columns:
    filters[column] = df[column].tolist()

st.session_state.filters = filters

filters_ = {}

for filter_name, filter in st.session_state.filters.items():
    filter__name = filter_name
    try:
        if set(filter):
            filter_name = st.sidebar.multiselect(
               f'{filter_name}',
                set(filter),[])

            filters_[filter__name] = filter_name
    except:
        pass

filteredrecords = []
    
for record in st.session_state.records_list:
    include = True
    for f, i in filters_.items():
        
        if i:
            if record[f] not in i:
                include = False
            else:
                pass
        
    if include and record not in filteredrecords:
        filteredrecords.append(record)

st.session_state.filteredrecords = filteredrecords

#st.write(filteredrecords)


st.header(f"{len(st.session_state.filteredrecords)} Records Post Filtering")
st.header(f"{len(st.session_state.records_list)} Total Number of Users")


finallistofemails = []
for record in st.session_state.filteredrecords:
    finallistofemails.append(record["Email"])

st.session_state.finallistofemails = finallistofemails

st.write(finallistofemails)
st.write(filteredrecords)

with col1:
    title = st.text_input('The title of your notification', 'Test title')
    body = st.text_input('The body of your notification', 'Test body')

with col2:
    if st.button("Send  Notification"):
        # Headers are fixed for both API calls
        headers = {
            'Authorization': "Bearer a2bdw98jjaesx1jfrh5n5l2lo",
            "Content-Type": "application/json"
        }
        for email in stqdm(finallistofemails):
            url = "https://api.adalo.com/notifications"

            data = {
                "appId": "7a236e7c-cba2-48fd-b61b-3584186ff918",
                "audience": {"email": email},
                "notification": {"titleText": title,
                                 "bodyText": body}
            }

            response = requests.post(url, json=data, headers=headers)


import mysql.connector as mysql
import pandas as pd
import time
from datetime import datetime
from PIL import Image
import json
import base64
import yagmail
import re
from re import search
import smtplib
 
import streamlit as st
import streamlit.components.v1 as components
from streamlit import caching
 
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from sqlalchemy import create_engine
from mysql.connector.constants import ClientFlag
from uuid import uuid4
import yaml

st.set_page_config(
    page_title="Diploma In Data Science BootCamp",
    page_icon=":brain:",
    layout="wide",
    initial_sidebar_state="expanded",
    )
with open('credintials.yml', 'r') as f:
    credintials = yaml.load(f, Loader=yaml.FullLoader)
    db_credintials = credintials['db']
    system_pass = credintials['system_pass']['admin']
    # email_sender = credintials['email_sender']
def get_database_connection():
    db = mysql.connect(host = db_credintials['host'],
                      user = db_credintials['user'],
                      passwd = db_credintials['passwd'],
                      database = db_credintials['database'],
                      auth_plugin= db_credintials['auth_plugin'])
    cursor = db.cursor()

    return cursor, db
 
cursor, db = get_database_connection()
 
#cursor.execute("SHOW DATABASES")
 
#databases = cursor.fetchall() ## it returns a list of all databases present
 
#st.write(databases)
 

 

#cursor.execute('''CREATE TABLE s_info (id varchar(255),
                                             #sname varchar(255),
	                                         #email varchar(255),
                                             #institution varchar(255),
                                             #pnum varchar(40),
                                             #re_date date,
                                             #gpa varchar(255),
                                             #status varchar(255))''')
#tables = cursor.fetchall()
#st.write(tables)
def admin_panel():
    username=st.sidebar.text_input('Username',key='user')
    password=st.sidebar.text_input('Password',type='password',key='pass')
    st.session_state.login=st.sidebar.checkbox('Login')
 
    if st.session_state.login==True:
        if username=="na" and password=='p':
            st.sidebar.success('Login Success')

            date1=st.date_input('Date1')
            date2=st.date_input('Date2')
            cursor.execute(f"select * from s_info where re_date between '{date1}' and '{date2}'")
            # db.commit()
            tables =cursor.fetchall()
            # st.write(tables)
            for i in tables:
                st.write(i[1])
                st.write(i[2])
                st.write(i[6])
                Accept=st.button('Accept',key=i[0])
                if Accept:
                    st.write('Accepted')
                    cursor.execute(f"Update s_info set status='Accepted' where id='{i[0]}'")
                    db.commit()
                Reject=st.button('Reject',key=i[0])
                if Reject:
                    st.write('Rejected')
                    cursor.execute(f"Update s_info set status='Rejected' where id='{i[0]}'")
                    db.commit()

        else:
            st.sidebar.warning('Wrong Credintials')
def s_form():
    id=uuid4()
    id=str(id)[:10]

    with st.form(key='member form'):
        sname=st.text_input('Student Name')
        email=st.text_input('E_Mail')
        institution=st.text_input('Instiution')
        pnum=st.text_input('Phone')
        gpa=st.text_input('GPA')
        re_date=st.date_input('Registration Date')
        status='In Progress'
        if st.form_submit_button('Submit'):
            query = f'''INSERT INTO s_info (id,sname,
                                              email,institution,pnum,gpa,re_date,status) VALUES ('{id}','{sname}','{email}'
                                                ,'{institution}','{pnum}','{gpa}','{re_date}','{status}')'''
            cursor.execute(query)
            db.commit()
            st.success(f'Congratulation *{sname}*! You have successfully Registered')
            st.code(id)
            st.warning("Please Store this code!!!")

def info():
    id=st.text_input('Your Code')
    Submit=st.button(label='Search')
    if Submit:
        cursor.execute(f"select * from s_info where id='{id}'")
        tables = cursor.fetchall()
        st.write(tables)

def stat():
    id=st.text_input('Your Id')
    submit=st.button('Search',key='sub')
    if submit:
        cursor.execute(f"Select status from s_info where id='{id}'")
        table=cursor.fetchall()
        st.write(table)
def main():
    #st.image('./index.jpg')
    st.title(' Data Science BootCamp Admission')
    selected=st.sidebar.selectbox('Select',
                        ('-----------',
                        'Registration',
                        'Information',
                        'Status',
                        'Only Admin',
                        
                        ))
    if selected=='Only Admin':
        admin_panel()
    elif selected=='Registration':
        s_form()
    elif selected=='Information':
        info()
    elif selected=='Status':
       stat()
if __name__=='__main__':
    main()
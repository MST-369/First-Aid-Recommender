import streamlit as st
from supabase import create_client
import httpx
import pandas as pd
import time
import plotly.express as px
from datetime import datetime
import numpy as np
from scipy.signal import sosfiltfilt, butter
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
import joblib

# Supabase connection setup
A = 'https://tgyzaqrrxsjqwlkanrqh.supabase.co/'
K = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRneXphcXJyeHNqcXdsa2FucnFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjY3MDI1NzIsImV4cCI6MjA0MjI3ODU3Mn0.gkOxXIxUR0axX5syhUhQlOBCTqodeMVkSu5YP_sUjJw'
SB = create_client(A, K)

# App Title
st.title("Welcome to First AID Recommender App")

# Arrange the buttons side by side using columns

tab1,tab2 =st.tabs(["Data", "Report"])
df=pd.DataFrame()

def Append_timeFrame(df,start):
    dft=[]
    for i in range(len(df)):
        dft.append(pd.Timestamp(start))
        start = pd.Timestamp(start)+pd.to_timedelta(1000, unit='microseconds')
    df['Timestamp']=dft
    df=df.set_index('Timestamp')
    return df


def Drop(df):
    for i in df.index:
        if df.loc[i].isna().any():
            df=df.drop(index=i)
    return df

def Normalize(df):
    ## Bring the minimum to positive
    df2=df.describe()
    minimum=min(df2.loc['min'])
    if minimum<0:
        for i in df.columns:
            df.loc[:,i]=df.loc[:,i]+abs(minimum)
    df2=df.describe()
    ## Turn the maximum value to 1
    maximum= max(df2.loc['max'])
    for i in df.columns:
        df.loc[:,i]=df.loc[:,i]/maximum
    df2=df.describe()
    return df

def DataSmoothing(df):
    d=dict()
    c=0
    fs=100
    for k in df.columns:
        for i in range(0,len(df),fs):
            min_i,mi,max_j,ma=-1,1000,-1,-1000
            for j in range(min(fs,(len(df)-i))):
                if df.iloc[i+j][k]>ma:
                    ma=df.iloc[i+j][k]
                    max_j=i+j
                if df.iloc[i+j][k]<mi:
                    mi=df.iloc[i+j][k]
                    min_i=i+j
            if k not in list(d.keys()):
                    d[k]=[]
            if min_i<max_j:
                d[k].extend([mi,ma])
            else:
                d[k].extend([mi,ma])
    d=pd.DataFrame(d)
    return d

def filter(df,d):
    import numpy as np
    from scipy.signal import sosfiltfilt, butter
    sos = butter(2, .2, output='sos')
    filtered = dict()
    for i in df.columns:
        if i not in list(filtered.keys()):
            filtered[i]=[]
        x=np.array(d.loc[:,i])
        filtered[i]=sosfiltfilt(sos,x )
    filtered=pd.DataFrame(filtered)
    return filtered 

def oscillations(filtered):
    val=[]
    t20=[]
    for k in filtered.columns:
        m=filtered.loc[:,k].mean()
        c=0
        f=1
        a=list(filtered.loc[:,k])
        a=sorted(a)[:len(a)//5]
        f=0
        for i in range(0,len(filtered)):
            if filtered.iloc[i][k]>a[-1]:
                f=1
            if filtered.iloc[i][k]<a[-1] and f==1:
                f=0
                c+=1
        val.append(c)
        t20.append(a[-1])
    return val,t20





with tab1:
    start_col, stop_col = st.columns(2)

    # Create buttons inside the columns
    sta = start_col.button('Fetch')
    sto = stop_col.button('Stop')

    # Create placeholders for dynamic status and content updates
    status_placeholder = st.empty()
    content_placeholder = st.empty()

    # Variable to track previous state
    pre = -1

    # Start button clicked
    if sta:
        while True:
            # Initial status check
            if pre == -1:
                status_placeholder.success("Trying!!")
                time.sleep(3)

            # Query the ready status from Supabase
            ready = SB.table('status').select('ready').execute()

            if ready.data[0]['ready'] != pre and ready.data[0]['ready'] == 1:
                status_placeholder.success("YES!!! Received the data")
                pre = 1
                df = pd.DataFrame(SB.table('readings').select('*').execute().data)
                if "df" not in st.session_state:
                    st.session_state["df"] = df
                content_placeholder.write(df.head(10))
                print('length : ',len(df))
                SB.table('status').update({'ready': 0}).eq('id', 1).execute()
                break
            else:
                if ready.data[0]['ready'] != pre and ready.data[0]['ready'] == 0:
                    status_placeholder.error("No data!!")
                    pre = 0

            # Break the loop if the stop button is clicked
    if sto:
        status_placeholder.empty()
        status_placeholder.success("Thank you!")
        time.sleep(3)




with tab2:
    figure = st.empty()
    df=pd.DataFrame()
    if "df" in st.session_state:
        nms=["RectoFemoral", "BicepsFemoral", "VastoMedial", "EMGSemitendinoso", "FlexoExtension"]
        df=st.session_state["df"]
        df=df.iloc[::-1,:]
        start =datetime.now()
        df=Drop(df)
        print('dropping..')
        df=df.iloc[::-1]
        df=Append_timeFrame(df,start)
        df2=df.copy()
        
        end = df.index[-1]
        sec=pd.Timestamp(end)-pd.Timestamp(start)
        sec = sec.total_seconds()
        print('Normalizing..')
        df=Normalize(df)
        print("smoothing..")
        d=DataSmoothing(df)
        filtered=filter(df,d)
        val,t20=oscillations(filtered)
        d3=df.describe()
        print("plotting..")
        fig=px.line(filtered)
        figure.plotly_chart(fig)
        test=[[d3.loc['min'][nms[0]],d3.loc['max'][nms[0]],d3.loc['std'][nms[0]],val[0],t20[0],
                          d3.loc['min'][nms[1]],d3.loc['max'][nms[1]],d3.loc['std'][nms[1]],val[1],t20[1],
                          d3.loc['min'][nms[2]],d3.loc['max'][nms[2]],d3.loc['std'][nms[2]],val[2],t20[2],
                          d3.loc['min'][nms[3]],d3.loc['max'][nms[3]],d3.loc['std'][nms[3]],val[0],t20[3],
                          d3.loc['min'][nms[4]],d3.loc['max'][nms[4]],d3.loc['std'][nms[4]],val[4],t20[4],sec]]
        st.write(df.describe())
         ### Normalizing values
        scaler = joblib.load('C:/Users/KOTA SRI SURYA TEJA/Desktop/Capstone/scaler.pkl')
        print('Loading..')
        test = scaler.transform(test)
        model = tf.keras.models.load_model('C:/Users/KOTA SRI SURYA TEJA/Desktop/Capstone/final_model.h5')
        test = np.expand_dims(test,axis=0)
        result = model.predict(test)
        cls = ['Abrnormal', 'Normal']
        print("result",result[0][0][0])
        ans = np.array(result).tolist()
        if round(ans[0][0][0])==1:
            st.success("Result : "+cls[round(ans[0][0][0])])
            SB.table('status').update({'result': 'Normal'}).eq('id', 1).execute()
        else:
            st.error("Result : "+cls[round(ans[0][0][0])])
            SB.table('status').update({'status': 'Abnormal'}).eq('id', 1).execute()
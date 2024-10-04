import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
  page_title="Analysis Portal (SubhaMondal)",
  page_icon='💦'
)

st.title(":rainbow[Data Analytics Portal]")
st.subheader(":gray[Explore Your Data]",divider='rainbow')

file = st.file_uploader("Drop Csv or Excel File",type=['csv','xlsx'])

if(file!=None):
  if(file.name.endswith('csv')):
    data=pd.read_csv(file)
  else:
    data=pd.read_excel(file)
  st.dataframe(data)
  st.info("File is successfully Uploaded ",icon='🐥')
  # st.balloons()


  st.subheader(":rainbow[Basic Information of Your Dataset]",divider="rainbow")
  tab1,tab2,tab3,tab4,icon = st.tabs(["Summary","Top and Bottom Rows","Data Types","Columns",'👈'])
  
  with tab1:
    st.write(f'There are :orange[{data.shape[0]}] rows in Your Dataset and :orange[{data.shape[1]}] Columns in the Dataset')
    st.subheader(":gray[Statistical summary of the Dataset]")
    st.dataframe(data.describe())

  with tab2:
    st.subheader(":gray[Top Rows]")
    toprow=st.slider("Nomber of\t :orange[Top] rows you want",1,20,key="1")
    st.dataframe(data.head(toprow))

    st.subheader(":gray[Bottom Rows]")
    topBottom=st.slider("Nomber of\t :orange[Bottom] rows you want",1,20,key="2")
    st.dataframe(data.tail(topBottom))

  with tab3:
    st.subheader(":gray[Data Type of Columns]")
    st.dataframe(data.dtypes)

  with tab4:
    st.subheader(":gray[Columns Names in Your Dataset]")
    st.write(list(data.columns))


  st.subheader(":rainbow[Column Values to Count]",divider="rainbow")
  with st.expander('Value Count'):
    col1,col2=st.columns(2)
    with col1:
      column=st.selectbox("Choose Column Name",options=list(data.columns))
    with col2:
      toprows=st.number_input('Top Rows',min_value=1,step=1)

    Count=st.button('Count')
    if(Count==True):
      result=data[column].value_counts().reset_index().head(toprows)
      st.dataframe(result)
      st.subheader(":gray[Visulization]")
      fig =  px.bar(data_frame=result,x=column,y='count',text='count',template='plotly_white')
      st.plotly_chart(fig)
      fig = px.line(data_frame=result,x=column,y='count',text='count',template='plotly_white')
      st.plotly_chart(fig)
      fig = px.pie(data_frame=result,names=column,values='count')
      st.plotly_chart(fig)

  st.subheader(":rainbow[Group By: Simplify Your Data Analysis]",divider="rainbow")
  st.write("The 'Group By' option lets you organize and summarize your data by specific categories or groups.")
  with st.expander("Group Operations"):
    gup1,gup2,gup3=st.columns(3)
    with gup1:
      groupcolumn=st.multiselect("Choose columns to GroupBy",options=list(data.columns))
    with gup2:
      operation_col=st.selectbox("Choose column for Operation",options=list(data.columns))
    with gup3:
      operation=st.selectbox("Choose Operation",options=['sum','max','min','median','count'])
    
    if(groupcolumn):
      resultG= data.groupby(groupcolumn).agg(
        Result=(operation_col,operation)
      ).reset_index()
      st.dataframe(resultG)
      asc= st.selectbox("You can check Highest and Lowest Value 🐥",options=['Highest','Lowest'])
      resultrows=st.number_input("Nomber of rows you want",min_value=1,step=1)
      if (asc=='Lowest'):
        st.dataframe(resultG.sort_values(by='Result',ascending=True).head(resultrows))
      else:
        st.dataframe(resultG.sort_values(by='Result',ascending=False).head(resultrows))

      st.subheader(":gray[Data Visulization]",divider="gray")
      graphs= st.selectbox("Choose Your Graphs",options=['line','bar','scatter','pie','sunburst'])
      if(graphs=='line'):
        x_axis=st.selectbox('Choose X axis',options=list(resultG.columns))
        y_axis=st.selectbox('Choose Y axis',options=list(resultG.columns))
        color = st.selectbox('Color information',options=[None]+list(resultG.columns))
        fig = px.line(data_frame=resultG,x=x_axis,y=y_axis,color=color,markers='o')
        st.plotly_chart(fig)
      elif(graphs=='bar'):
        x_axis=st.selectbox('Choose X axis',options=list(resultG.columns))
        y_axis=st.selectbox('Choose Y axis',options=list(resultG.columns))
        color = st.selectbox('Color information',options=[None]+list(resultG.columns))
        facet_color = st.selectbox('Colum info ',options=[None]+list(resultG.columns))
        fig = px.bar(data_frame=resultG,x=x_axis,y=y_axis,color=color,facet_col=facet_color,barmode='group')
        st.plotly_chart(fig)
      elif(graphs=='scatter'):
        x_axis=st.selectbox('Choose X axis',options=list(resultG.columns))
        y_axis=st.selectbox('Choose Y axis',options=list(resultG.columns))
        color = st.selectbox('Color information',options=[None]+list(resultG.columns))
        size =st.selectbox('Choose Numerical Size Column',options=[None]+ list(resultG.columns))
        fig = px.scatter(data_frame=resultG,x=x_axis,y=y_axis,color=color,size=size)
        st.plotly_chart(fig)
      elif(graphs=='pie'):
        values=st.selectbox('Choose Numerical Values',options=list(resultG.columns))
        names=st.selectbox('Choose Labels',options=list(resultG.columns))
        fig = px.pie(data_frame=resultG,values=values,names=names)
        st.plotly_chart(fig)
      elif(graphs=='sunburst'):
        path=st.multiselect('Choose your path',options=list(resultG.columns))
        fig = px.sunburst(data_frame=resultG,path=path,values='Result')
        st.plotly_chart(fig)











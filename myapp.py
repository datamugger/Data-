# import libraries
import pandas as pd
import plotly.express as px
import streamlit as st
import openpyxl


# Configuration
st.set_page_config(
    page_title='Data Analytics Portal',
    page_icon='📊'
)

# Title
st.title(':rainbow[Data Analytics Portal]')

# Header
st.subheader(':gray[Explore Data with ease.]', divider='rainbow')

# File Uploader
file = st.file_uploader('Drop csv or excel file', type=['csv', 'xlsx'])

# Read the File
if(file != None):
    # check file type 
    if(file.name.endswith('csv')):
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)

    # show data
    st.dataframe(data)

    #st.info('File is successfully Uploaded')
    st.info('File is successfully Uploaded', icon='🚨')

    # Basic Information of the data
    st.subheader(':rainbow[Basic information of the dataset]', divider='rainbow')
    
    # we want to show the information in tabs format
    tab1, tab2, tab3, tab4 = st.tabs(4)

    with tab1:
        st.write(f'There are {data.shape[0]} rows and {data.shape[1]} columns in the dataset.')
        st.subheader(':gray[Statistical Summary of the dataset]')
        st.dataframe(data.describe())

    with tab2:
        st.subheader(':gray[Top Rows]')
        toprows = st.slider('Number of rows you want', 1, data.shape[0], key='topslider')
        st.dataframe(data.head(toprows))

        st.subheader(':gray[Bottom Rows]')
        bottomrows = st.slider('Number of rows you want', 1, data.shape[0], key='bottomslider')
        st.dataframe(data.tail(bottomrows))

    with tab3:
        st.subheader(':gray[Data types of column]')
        st.dataframe(data.dtypes.rename_axis('Columns').reset_index(name='Data type').set_index('Columns'))

    with tab4:
        st.subheader(':gray[Column Names in Dataset]')
        st.write(list(data.columns))

    ## Day 3
    st.subheader(':rainbow[Column Values To Count]', divider='rainbow')

    with st.expander('Select a Column and Number of rows'):
        col1, col2 = st.columns(2)

        with col1:
            column = st.selectbox('Select a Column', options= list(data.columns))

        with col2:
            toprows = st.number_input('Top rows', min_value=1,step=1)

        count = st.button('Count')
        if(count == True):
            result = data[column].value_counts().reset_index().head(toprows)
            st.dataframe(result)

            # Visualization Charts
            st.subheader('Visualization', divider='gray')

            # Bar-Chart
            fig = px.bar(result, x=column, y='count', text='count', template='plotly_white') 
            st.plotly_chart(fig)  

            # Line Chart
            fig = px.line(data_frame=result, x=column, y='count', text='count', template='plotly_white')
            st.plotly_chart(fig)

            # Pie-Chart
            fig=px.pie(data_frame=result, names=column, values='count')
            st.plotly_chart(fig)


    ## Day 4
    st.subheader(':rainbow[Groupby : Simplify your data analysis]', divider='rainbow')
    st.write('The groupby lets you summarize data by specific categories and groups')

    with st.expander('Group by your columns'):
        col1, col2, col3 = st.columns(3)
        with col1:
            groupby_cols = st.multiselect('Choose your column to groupby', options = list(data.columns))

        with col2:
            operation_col = st.selectbox('Choose column for operation', options=list(data.columns))

        with col3:
            operation = st.selectbox('Choose operation', options=['sum', 'max', 'min', 'count', 'mean'])

        if(groupby_cols):
            result = data.groupby(groupby_cols).agg(
                newcol = (operation_col, operation)
            ).reset_index()

            st.dataframe(result)

            ## Day 5
            st.subheader(':gray[Data Visualization]', divider='gray')

            graphs = st.selectbox('Choose your graph', options=['line','bar','scatter','pie','sunburst'])
            if(graphs == 'line'):
                x_axis = st.selectbox('Choose X axis', options=list(result.columns))
                y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
                color = st.selectbox('Color Information', options=[None] + list(result.columns))
                fig = px.line(data_frame=result, x=x_axis, y=y_axis, color=color, markers='o')
                st.plotly_chart(fig)

            elif(graphs == 'bar'):
                x_axis = st.selectbox('Choose X axis', options=list(result.columns))
                y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
                color = st.selectbox('Color Information', options=[None] + list(result.columns))
                facet_col = st.selectbox('Column Information', options=[None] + list(result.columns))
                fig = px.bar(data_frame=result, x=x_axis, y=y_axis, color=color, facet_col = facet_col, barmode='group')
                st.plotly_chart(fig)

            elif(graphs == 'scatter'):
                x_axis = st.selectbox('Choose X axis', options=list(result.columns))
                y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
                color = st.selectbox('Color Information', options=[None] + list(result.columns))
                size = st.selectbox('Size Column',options=[None]+list(result.columns))
                fig = px.scatter(data_frame=result, x=x_axis, y=y_axis, color=color, size=size)
                st.plotly_chart(fig)

            elif(graphs == 'pie'):
                values = st.selectbox('Choose numerical values', options=list(result.columns))
                names = st.selectbox('Choose labels', options=list(result.columns))
                fig = px.pie(data_frame=result, values=values, names=names)
                st.plotly_chart(fig)

            elif(graphs == 'sunburst'):
                path = st.multiselect('Choose your Path', options=list(result.columns))
                fig = px.sunburst(data_frame=result, path=path, values='newcol')
                st.plotly_chart(fig)

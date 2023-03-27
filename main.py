

from textblob import TextBlob
import pandas as pd
import streamlit as st
import cleantext
from PIL import Image
from urllib.parse import quote
import requests
from io import BytesIO
import streamlit.components.v1 as components

   




page_bg_img = """
<style>

[data-testid="stAppViewContainer"] {
padding: 0 100px; 
background-image: url("https://firebasestorage.googleapis.com/v0/b/diffusion-library.appspot.com/o/wooden-table-with-movie-reel-in-black-colour-icon-on-it-in-photorealistic-style%2F6.jpg?alt=media&token=f0b05809-2e31-46c2-b2db-98c7f1ac84bb");
#background-image: url("https://th.bing.com/th/id/OIP.LDqs_kFylu8Olf3WJ-sHWgHaEo?w=264&h=180&c=7&r=0&o=5&dpr=1.6&pid=1.7");
padding: 0 100px; 
height: 200vh;
display: flex;
justify-content: center;

background-repeat: no-repeat;
background-position: center;
background-size: 100% 100%;

}

[data-testid="stHeader"] {
background: rgba(0,0,0,0);
}
{

[data-testid="stToolbar"] {

}

</style>
"""

style="background-color: rgba(255, 255, 255, 0.5);"
st.markdown(page_bg_img, unsafe_allow_html=True)
st.header('Sentiment Analysis on Movie Reviews')
col1, col2, col3 = st.columns([1,2,1]);

def get_movie_info(title):
    url = f'http://www.omdbapi.com/?apikey=111588ce&t={quote(title)}'
    response = requests.get(url)
    #return response.json()
    movie_data = response.json()
    if movie_data['Response'] == 'True':
        poster_url = movie_data['Poster']
        poster_response = requests.get(poster_url)
        poster_image = Image.open(BytesIO(poster_response.content))
        movie_data['poster_image'] = poster_image
    return movie_data

with st.expander('Analyze Reviews'):
    txt = st.text_input('Enter Movie Title: ')
    if txt:
        movie_info = get_movie_info(txt)
        if movie_info['Response'] == 'True':
            st.write(f"Title: {movie_info['Title']}")
            col2.image(movie_info['poster_image'])
            st.write(f"Year: {movie_info['Year']}")
            st.write(f"Rated: {movie_info['Rated']}")
            st.write(f"Runtime: {movie_info['Runtime']}")
            st.write(f"Plot: {movie_info['Plot']}")
            st.write(f"Actors: {movie_info['Actors']}")
            st.write(f"Director: {movie_info['Director']}")
            st.write(f"Genre: {movie_info['Genre']}")
            st.write(f"Language: {movie_info['Language']}")
            st.write(f"Released: {movie_info['Released']}")
            st.write(f"Country: {movie_info['Country']}")
            st.write(f"IMDb Rating: {movie_info['imdbRating']}")
        else:
            st.write("Movie not found")

    text = st.text_input('Review here: ')
    if text:
        blob = TextBlob(text)
        st.write('Polarity: ', round(blob.sentiment.polarity, 2))
        st.write('Subjectivity: ', round(blob.sentiment.subjectivity, 2))

    pre = st.text_input('Clean Text: ')
    if pre:
        st.write(cleantext.clean(pre, clean_all=False, extra_spaces=True,
                                 stopwords=True, lowercase=True, numbers=True, punct=True))

with st.expander('Analyze Data'):
    upl = st.file_uploader('Upload file')


    def score(x):
        blob1 = TextBlob(x)
        return blob1.sentiment.polarity


    #
    def analyze(x):
        if x >= 0.5:
            return "Positive"
        elif x > 0:
            return "Somewhat Positive"
        elif x == 0:
            return "Neutral"
        elif x > -0.5:
            return "Somewhat Negative"
        else:
            return "Negative"


    #
    if upl:
        df = pd.read_excel(upl)
        # del df['Unnamed: 0']
        df['score'] = df['review'].apply(score)
        df['analysis'] = df['score'].apply(analyze)
        st.write(df.head(10))


        @st.cache_data
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')


        csv = convert_df(df)

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='sentiment.csv',
            mime='text/csv',
        )

st.header('Data Insight')
with st.container():
    st.header("Distribution of Positive and Negative Reviews")
    st.markdown(
        "This bar chart show the distribution of positive and negative reviews in the dataset. By looking at the graph you can clearly seen that dataset is balanced."
    )
    image = Image.open('sentiment_distribution.png')
    st.image(image)

with st.container():
    st.header("Total Numbers of words in reviews")
    st.markdown(
        "This Histogram display the total number of word in each reviews."
    )
    image = Image.open('positive_words.png')
    st.image(image)

with st.container():
    st.header("Most Common Positive words")
    st.markdown(
        "This graph illustrates the most common positive words that are found in the dataset."
    )
    image = Image.open('newplot.png')
    st.image(image)
with st.container():
    st.header("Most Common Negative words")
    st.markdown(
        "This graph illustrates the most common negative words that are found in the dataset."
    )
    image = Image.open('bar.png')
    st.image(image)

with st.container():
    st.header("WorldCloud for Positive")
    st.markdown(
        "This WordCloud display the most common positive words that we find in the dataset. WordCloud helps to analyze the test data through visualization and importance of the words can be explained by its frequency."
    )
    image = Image.open('positive.png')
    st.image(image)

with st.container():
    st.header("WordCloud for Negative")
    st.markdown(
        "This is the WordCloud for most common negative words."
    )
    image = Image.open('word.png')
    st.image(image)













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
#background-image: url("https://firebasestorage.googleapis.com/v0/b/diffusion-library.appspot.com/o/photorealistic-style-with-dark-background-with-movie-reel-in-it%2F3.jpg?alt=media&token=c5f9a8be-cdad-4b1b-80ad-e4e087e7788b");
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
                                 stopwords=True, lowercase=True, numbers=True, punct=True)





# Function to get movie recommendations based on sentiment analysis
# Function to get movie recommendations based on sentiment analysis
 def get_movie_recommendations(query, year):
    # Get search results for the user's query
    params = {
        "apikey": "111588ce",
        "s": query,
        "type": "movie",
        "r": "json",
        "y": year,
       

    }
    response = requests.get("http://www.omdbapi.com/", params=params)
    data = response.json()

    # Check if the search was successful
    if data["Response"] == "False":
        st.write(data["Error"])
    else:
        # Create a DataFrame with the search results
        movies_df = pd.DataFrame(data["Search"])

        # Add a column for the sentiment of the movie reviews
        movies_df["sentiment"] = movies_df["imdbID"].apply(
            lambda id: TextBlob(get_movie_reviews(id)).sentiment.polarity
        )
        movies_df["director"] = movies_df["imdbID"].apply(
            lambda id: get_movie_director(id)
        )
        movies_df["cast"] = movies_df["imdbID"].apply(
            lambda id: get_movie_cast(id)
        )
        movies_df["plot"] = movies_df["imdbID"].apply(
            lambda id: get_movie_plot(id)
        )
        movies_df["awards"] = movies_df["imdbID"].apply(
            lambda id: get_movie_awards(id)
        )
        movies_df["runtime"] = movies_df["imdbID"].apply(
            lambda id: get_movie_runtime(id)
        )
        # Add a column for the trailer URL
        movies_df["trailer"] = movies_df.apply(
            lambda row: get_movie_trailer(row["Title"], row["Year"]),
            axis=1
        )

        # Add a column for the movie rating
        movies_df["rating"] = movies_df["imdbID"].apply(
            lambda id: get_movie_rating(id)
        )
        # Add a column for the poster image
        movies_df["poster"] = movies_df["imdbID"].apply(
            lambda id: get_movie_poster(id)
        )


        # Sort the DataFrame by sentiment in descending order
        movies_df = movies_df.sort_values(by="sentiment", ascending=False)

        # Return the top 10 movies with the highest sentiment
        return movies_df[["Title", "Year", "director", "cast", "plot", "sentiment" , "awards", "runtime", "trailer", "poster"]][:10]


# Function to get the reviews for a movie
def get_movie_reviews(id):
    params = {
        "apikey": "111588ce",
        "i": id,
        "type": "movie",
        "r": "json",
        "plot": "full",
    }
    response = requests.get("http://www.omdbapi.com/", params=params)
    data = response.json()
    return data["Plot"]

def get_movie_rating(imdb_id):
    """Returns the rating for a given movie IMDB ID."""
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey=111588ce"
    data = requests.get(url).json()
    rating = data.get("imdbRating")
    if rating and rating != "N/A":
        return float(rating)
    else:
        return None

def get_movie_cast(imdb_id):
    """Returns the cast for a given movie IMDB ID."""
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey=111588ce"
    data = requests.get(url).json()
    cast = data.get("Actors")
    if cast and cast != "N/A":
        return cast.split(", ")
    else:
        return None
def get_movie_plot(imdb_id):
    """Returns the plot for a given movie IMDB ID."""
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey=111588ce"
    data = requests.get(url).json()
    plot = data.get("Plot")
    return plot

def get_movie_director(imdb_id):
    """Returns the director information for a given movie IMDB ID."""
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey=111588ce"
    data = requests.get(url).json()
    director = data.get("Director")
    if director and director != "N/A":
        return director
    else:
        return None
def get_movie_awards(imdb_id):
    """Returns the awards for a given movie IMDB ID."""
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey=111588ce"
    data = requests.get(url).json()
    awards = data.get("Awards")
    if awards and awards != "N/A":
        return awards
    else:
        return None
def get_movie_runtime(imdb_id):
    """Returns the runtime for a given movie IMDB ID."""
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey=111588ce"
    data = requests.get(url).json()
    runtime = data.get("Runtime")
    if runtime and runtime != "N/A":
        return runtime
    else:
        return None
import requests
import urllib.parse

YOUTUBE_API_KEY = "AIzaSyCWqqBCEwGQmern61gI0fB7xoW4tWanA5k"

def get_movie_trailer(title, year):
    # Build the search query for the YouTube API
    query = f"{title} {year} trailer"
    query = urllib.parse.quote_plus(query)

    # Make a request to the YouTube API to search for the trailer
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=1&key={YOUTUBE_API_KEY}&q={query}"
    response = requests.get(url).json()

    # Extract the trailer URL from the API response
    if "items" in response and len(response["items"]) > 0:
        trailer_id = response["items"][0]["id"]["videoId"]
        trailer_url = f"https://www.youtube.com/watch?v={trailer_id}"
        return trailer_url
    else:
        return None


# Function to get the poster image for a movie
def get_movie_poster(imdb_id):
    """Returns the poster URL for a given movie IMDB ID."""
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey=111588ce"
    data = requests.get(url).json()
    poster_url = data.get("Poster")
    if poster_url and poster_url != "N/A":
        return poster_url
    else:
        return "https://via.placeholder.com/image not"  # default poster image



# Streamlit app
def app():
 with st.expander('Movie Recommendation'):
    # Get user input

    query = st.text_input("Enter the Movie Genre:")
    year = st.text_input("Enter a year:")

    if query:
        st.markdown(f"<h3 style='text-align: center;'>Top 10 recommended movies for '{query}':</h3>", unsafe_allow_html=True)

        # Get movie recommendations based on sentiment analysis
        recommendations = get_movie_recommendations(query, year)

        # Display the recommendations as a table with posters
        for _, row in recommendations.iterrows():
            st.subheader(f"Title: {row['Title']}")
            st.image(row["poster"])
            st.write(f"Year: {row['Year']}")
            st.write(f"Director: {row['director']}")
            st.write(f"Cast: {row['cast']}")
            st.write(f"Plot: {row['plot']}")
            st.write(f"Sentiment: {row['sentiment']:.2f}")
            st.write(f"Awards: {row['awards']}")
            st.write(f"Runtime: {row['runtime']}")
            trailer_url = row["trailer"]
            #if trailer_url:
            st.markdown(f"[Watch the trailer]({trailer_url})")
            st.write("---")

if __name__ == "__main__":
    app()

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












# Movie Collection App

A web application to manage and review your movie collection. The application uses Flask for the web framework, SQLAlchemy for database management, and TMDB (The Movie Database) API for fetching movie details.

## Features

- **Home Page:** Displays the list of movies in the collection, sorted by their rating in descending order.
- **Edit Page:** Allows users to update the rating and review of a movie in the collection.
- **Delete Functionality:** Users can delete a movie from the collection.
- **Add Movie Page:** Users can search for movies using the TMDB API and add them to their collection.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/movie-collection-app.git
    cd movie-collection-app
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    - Create a `.env` file in the root directory.
    - Add your TMDB API key to the `.env` file:
      ```sh
      TMDB_API_KEY=<Your_TMDB_API_Key>
      ```

5. Initialize the database:
    ```sh
    flask db init
    flask db migrate
    flask db upgrade
    ```

6. Run the application:
    ```sh
    flask run
    ```

## Usage

### Home Page
- Displays the list of movies in the collection.
- Movies are ordered by their rating from highest to lowest.

### Edit Movie
- To edit a movie, click on the "Edit" button next to the movie on the home page.
- Update the rating and review, then click "Done".

### Delete Movie
- To delete a movie, click on the "Delete" button next to the movie on the home page.

### Add Movie
- To add a new movie, navigate to the "Add Movie" page.
- Enter the movie title and click "Add Movie".
- Select the correct movie from the list of search results.

## File Structure

```
movie-collection-app/
│
├── templates/
│   ├── add.html
│   ├── edit.html
│   ├── index.html
│   ├── layout.html
│   ├── select.html
│
├── .env
├── app.py
├── requirements.txt
├── models.py
├── forms.py
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── README.md
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

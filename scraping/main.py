import os
from utils.genres.index import get_all_genres, get_all_musics_from_genre, download_preview_songs

def ensure_directory_exists(path: str) -> None:
    """Assure que le répertoire existe."""
    if not os.path.exists(path):
        os.makedirs(path)

def download_genre_music(genre, href, base_path):
    """Télécharge les musiques pour un genre donné."""
    genre_path = os.path.join(base_path, genre)
    ensure_directory_exists(genre_path)

    df_music = get_all_musics_from_genre(href)

    # Télécharger les chansons de prévisualisation
    download_preview_songs(df_music, genre)

if __name__ == "__main__":
    df_genres = get_all_genres()
    df_genres = df_genres.head(1)  # Pour tester, on ne prend que le premier genre
    base_path = "../data/genres"

    ensure_directory_exists(base_path)  # Création du répertoire de base une seule fois

    # Traitement pour chaque genre trouvé
    for index, row in df_genres.head(1).iterrows():
        download_genre_music(row['genre'], row['href'], base_path)

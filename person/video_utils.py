from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.preprocessing import image
from sklearn.feature_extraction.text import TfidfVectorizer
from django.conf import settings
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from django.utils.html import strip_tags
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import video


def get_video_tags(video):
    """Retrieve tags for a Video as a space-separated string."""
    tags = video.tags.all()
    return ' '.join(tag.name for tag in tags)
def preprocess_content(text):
    """Preprocess the text content by cleaning it."""
    return text.replace('\n', ' ').strip()

def preprocess_combined_content(title, description, tags):
    """Combine title, description, and tags into a single string."""
    combined = f"{title} {description} {tags}"
    return preprocess_content(combined)

def compute_similarity(text1, text2):
    """Compute similarity between two pieces of text."""
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity[0][0]
def find_similar_videos(target_video_id):
    """Find videos similar to the given target video using title, description, and tags."""
    # Get the target video and its content and tags
    target_video = video.objects.get(id=target_video_id)
    target_content = preprocess_combined_content(
        target_video.title,
        target_video.description,
        get_video_tags(target_video)
    )

    # Retrieve all videos except the target video
    videos = video.objects.exclude(id=target_video_id)
    video_data = [
        (vid, preprocess_combined_content(vid.title, vid.description, get_video_tags(vid)))
        for vid in videos
    ]

    # Calculate similarity
    similarities = []
    for vid, vid_content in video_data:
        similarity_score = compute_similarity(target_content, vid_content)
        similarities.append((vid, similarity_score))

    # Sort by similarity score
    similar_videos = sorted(similarities, key=lambda x: x[1], reverse=True)
    return [(vid,score) for vid, score in similar_videos]
############
# find images
#############
from .models import video as Video, Image, Category

def get_tags_as_string(instance, field_name):
    """Retrieve tags for an instance as a space-separated string."""
    tags = getattr(instance, field_name).all()
    return ' '.join(tag.name for tag in tags)

def preprocess_text_images(title, description, tags):
    """Combine and preprocess title, description, and tags into a single string."""
    combined_text = f"{title} {description} {tags}"
    return combined_text.replace('\n', ' ').strip()

def calculate_text_similarity(text1, text2):
    """Calculate similarity score between two pieces of text."""
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity_score[0][0]


def find_similar_images_to_video(video_id):
    """Find images that are similar to the given video based on title, description, and tags."""
    # Retrieve the target video
    video = Video.objects.get(id=video_id)

    # Prepare video content for similarity comparison
    video_tags = get_tags_as_string(video, 'tags')
    video_content = preprocess_text_images(video.title, video.description, video_tags)

    # Retrieve all images and prepare their content for comparison
    images = Image.objects.all()
    image_data = [
        (image, preprocess_text_images(
            image.title,
            image.description,
            get_tags_as_string(image, 'tags_img')
        ))
        for image in images
    ]

    # Calculate similarity scores between the video and all images
    image_similarity_scores = []
    for image, image_content in image_data:
        similarity_score = calculate_text_similarity(video_content, image_content)
        image_similarity_scores.append((image, similarity_score))

    # Sort images by similarity score in descending order
    similar_images = sorted(image_similarity_scores, key=lambda x: x[1], reverse=True)

    # Return only the image objects
    return [(image,score) for image, score in similar_images]
##############for posts

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Q
from .models import Post, video as Video, Category

def extract_text_from_html(html_content):
    """Extract text from HTML content."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()
def preprocess_text(title, description, content, tags):
    """Combine and preprocess title, description, content, and tags into a single string."""
    combined_text = f"{title} {description} {content} {tags}"
    return combined_text.replace('\n', ' ').strip()

def calculate_text_similarity(text1, text2):
    """Calculate similarity score between two pieces of text."""
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity_score[0][0]


def find_similar_posts_to_video(video_id,object_data):
    """Find posts that are similar to the given video based on title, description, content, and tags."""
    # Retrieve the target video
    video = Video.objects.get(id=video_id)

    # Prepare video content for similarity comparison
    video_tags = get_tags_as_string(video, 'tags')
    video_content = preprocess_text(video.title, video.description, '', video_tags)

    # Retrieve all posts and prepare their content for comparison
    posts = object_data
    post_data = [
        (post, preprocess_text(
            post.title,
            '',  # No description field in Post
            extract_text_from_html(post.content),
            get_tags_as_string(post, 'tags')
        ))
        for post in posts
    ]

    # Calculate similarity scores between the video and all posts
    post_similarity_scores = []
    for post, post_content in post_data:
        similarity_score = calculate_text_similarity(video_content, post_content)
        post_similarity_scores.append((post, similarity_score))

    # Sort posts by similarity score in descending order
    similar_posts = sorted(post_similarity_scores, key=lambda x: x[1], reverse=True)

    # Return only the post objects
    return [(post,score) for post, score in similar_posts]

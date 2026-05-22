from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Q
from .models import Image, Category,video as Video

def get_tags_as_string(instance, field_name):
    """Retrieve tags for an instance as a space-separated string."""
    tags = getattr(instance, field_name).all()
    return ' '.join(tag.name for tag in tags)

def preprocess_text(title, description, tags):
    """Combine and preprocess title, description, and tags into a single string."""
    combined_text = f"{title} {description} {tags}"
    return combined_text.replace('\n', ' ').strip()

def calculate_text_similarity(text1, text2):
    """Calculate similarity score between two pieces of text."""
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity_score[0][0]


def find_similar_images_to_image(image_id):
    """Find images similar to the given image based on title, description, and tags."""
    # Retrieve the target image
    target_image = Image.objects.get(id=image_id)
    similar_items = []

    # Prepare the target image's content for comparison
    target_tags = get_tags_as_string(target_image, 'tags_img')
    target_content = preprocess_text(target_image.title, target_image.description, target_tags)

    # Retrieve all images and prepare their content for comparison
    images = Image.objects.exclude(id=image_id)  # Exclude the target image itself
    image_data = [
        (image, preprocess_text(
            image.title,
            image.description,
            get_tags_as_string(image, 'tags_img')
        ))
        for image in images
    ]

    # Calculate similarity scores between the target image and all other images
    image_similarity_scores = []
    for image, image_content in image_data:
        similarity_score = calculate_text_similarity(target_content, image_content)
        image_similarity_scores.append((image, similarity_score))

    # Sort images by similarity score in descending order
    similar_images = sorted(image_similarity_scores, key=lambda x: x[1], reverse=True)

    # Return only the image objects
    return [(image, score) for image, score in similar_images]
########################
# vidoes to images
#################

def find_similar_videos_to_image(image_id):
    """Find videos similar to the given image based on title, description, and tags."""
    # Retrieve the target image
    target_image = Image.objects.get(id=image_id)

    # Prepare the target image's content for comparison
    target_tags = get_tags_as_string(target_image, 'tags_img')
    target_content = preprocess_text(target_image.title, target_image.description, target_tags)

    # Retrieve all videos and prepare their content for comparison
    videos = Video.objects.all()  # You might want to filter videos based on some criteria
    video_data = [
        (video, preprocess_text(
            video.title,
            video.description,
            get_tags_as_string(video, 'tags')
        ))
        for video in videos
    ]

    # Calculate similarity scores between the target image and all videos
    video_similarity_scores = []
    for video, video_content in video_data:
        similarity_score = calculate_text_similarity(target_content, video_content)
        video_similarity_scores.append((video, similarity_score))

    # Sort videos by similarity score in descending order
    similar_videos = sorted(video_similarity_scores, key=lambda x: x[1], reverse=True)

    # Return only the video objects
    return [(video,score) for video, score in similar_videos]
############
# text to Images

def extract_text_from_html(html_content):
    """Extract plain text from HTML content."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()


def find_similar_posts_to_image(image_id,object_data):
    """Find posts similar to the given image based on title, description, and tags."""
    # Retrieve the target image
    target_image = Image.objects.get(id=image_id)

    # Prepare the target image's content for comparison
    target_tags = ' '.join(tag.name for tag in target_image.tags_img.all())
    target_content = preprocess_text(target_image.title, target_image.description, target_tags)

    # Retrieve all posts and prepare their content for comparison
    posts = object_data  # You might want to filter posts based on some criteria
    post_data = [
        (post, preprocess_text(
            post.title,
            extract_text_from_html(post.content),
            ' '.join(tag.name for tag in post.tags.all())
        ))
        for post in posts
    ]

    # Calculate similarity scores between the target image and all posts
    post_similarity_scores = []
    for post, post_content in post_data:
        similarity_score = calculate_text_similarity(target_content, post_content)
        post_similarity_scores.append((post, similarity_score))

    # Sort posts by similarity score in descending order
    similar_posts = sorted(post_similarity_scores, key=lambda x: x[1], reverse=True)

    # Return only the post objects
    return [(post,score) for post, score in similar_posts]

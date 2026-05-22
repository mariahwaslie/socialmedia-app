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
from .models import BlogPost, Post,Image,video

def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()

def extract_text_features(html_texts):
    texts = [extract_text_from_html(html) for html in html_texts]
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(texts)
    return tfidf_matrix

def get_text_features(posts):
    texts = [extract_text_from_html(post.content) for post in posts]
    return texts
def compute_similarity(text_features):
    return cosine_similarity(text_features, text_features)

def compute_tfidf_matrix(texts):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(texts)
    return tfidf_matrix


def calculate_similarity(tfidf_matrix):
    similarity_matrix = cosine_similarity(tfidf_matrix)
    return similarity_matrix

def get_recommendations(post_id, all_posts, similarity_matrix):

    items = [post.id for post in all_posts]
    if post_id not in items:
        print(f"Debug: post_id {post_id} is not in the items list.")
    idx = items.index(post_id)
    similar_items = similarity_matrix[idx]
    recommended_indices = similar_items.argsort()[-10:][::-1]  # Get top 10 similar items

    recommendations = [(all_posts[i],recommended_indices) for i in recommended_indices if i != idx]  # Exclude the original post
    return recommendations
    # Rest of your code


def get_similar_blogposts(post_id, all_posts, all_blogposts):
    # Extract HTML content
    post_html_texts = [post.content for post in all_posts if post.id == post_id]
    blog_html_texts = [blog.content for blog in all_blogposts]

    # Combine post and blog texts
    all_html_texts = post_html_texts + blog_html_texts

    # Extract features
    text_features = extract_text_features(all_html_texts)

    # Compute similarity matrix
    similarity_matrix = compute_similarity(text_features)

    # Get index of the post
    post_index = 0  # Assuming single post, index 0

    # Get similarity scores for blogposts
    blog_indices = range(len(post_html_texts), len(post_html_texts) + len(blog_html_texts))
    similar_blog_indices = similarity_matrix[post_index, blog_indices].argsort()[-10:][::-1]

    similar_blog_indices = [int(idx) for idx in similar_blog_indices]

    # Retrieve similar blogposts
    similar_blogposts = [(all_blogposts[i],similar_blog_indices[i]) for i in similar_blog_indices]

    return similar_blogposts

# Function to extract images from HTML content


def get_similar_images(post, all_images):
    # Extract the text from the post content using BeautifulSoup
    post_text = BeautifulSoup(post.content, "html.parser").get_text()

    # Combine the post text with its tags for a more comprehensive feature
    post_tags = " ".join([tag.name for tag in post.tags.all()])
    post_features = f"{post_text} {post_tags}"

    # Prepare a list of combined features for all images
    image_features = []
    for image in all_images:
        if not hasattr(image, 'tags_img'):

            continue

        image_tags = " ".join([tag.name for tag in image.tags_img.all()])
        image_description = image.description
        combined_features = f"{image_description} {image_tags}"
        if combined_features.strip():  # Ensure non-empty feature
            image_features.append(combined_features)

    # Check if features are valid
    if not image_features:
        return []  # Handle the case where no valid features are prepared

    # Include the post features in the list for vectorization
    all_features = [post_features] + image_features

    # Ensure there's at least one feature for comparison
    if len(all_features) <= 1:
        return []  # Ensure there's at least one feature for comparison

    # Vectorize the combined features
    vectorizer = TfidfVectorizer(stop_words='english')
    feature_vectors = vectorizer.fit_transform(all_features)

    # Calculate the cosine similarity between the post and all images
    similarity_matrix = cosine_similarity(feature_vectors[0:1], feature_vectors[1:])

    # Get the indices of similar images sorted by similarity score
    similar_image_indices = np.argsort(similarity_matrix[0])[::-1]

    # Return the image objects sorted by similarity
    similar_images = [(all_images[i],similar_image_indices) for i in similar_image_indices]

    return similar_images

def get_similar_videos_to_post(post, all_videos):
    # Step 1: Prepare the data
    post_text = post.content
    video_texts = [video.description for video in all_videos]

    # Combine post text with video descriptions
    all_texts = [post_text] + video_texts

    # Step 2: Calculate TF-IDF for content similarity
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(all_texts)

    # Step 3: Calculate tag-based similarity
    all_tags = set(tag.name for video in all_videos for tag in video.tags.all())
    post_tags = set(tag.name for tag in post.tags.all())
    all_tag_vectors = []

    for video in all_videos:
        video_tags = set(tag.name for tag in video.tags.all())
        tag_vector = [1 if tag in video_tags else 0 for tag in all_tags]
        all_tag_vectors.append(tag_vector)

    post_tag_vector = [1 if tag in post_tags else 0 for tag in all_tags]
    all_tag_vectors.insert(0, post_tag_vector)  # Insert post tag vector at the beginning

    tag_similarity = cosine_similarity(np.array(all_tag_vectors))

    # Step 4: Calculate category-based similarity
    all_categories = set(video.catagory.name for video in all_videos if video.catagory)
    post_category = post.catagory.name if post.catagory else None

    post_category_vector = [1 if category == post_category else 0 for category in all_categories]
    all_category_vectors = []

    for video in all_videos:
        video_category = video.catagory.name if video.catagory else None
        category_vector = [1 if category == video_category else 0 for category in all_categories]
        all_category_vectors.append(category_vector)

    all_category_vectors.insert(0, post_category_vector)  # Insert post category vector at the beginning

    category_similarity = cosine_similarity(np.array(all_category_vectors))

    # Step 5: Combine all similarities (weighted)
    text_similarity = cosine_similarity(tfidf_matrix)

    combined_similarity = (
            0.5 * text_similarity +  # Assuming 50% weight to text similarity
            0.3 * tag_similarity +  # Assuming 30% weight to tag similarity
            0.2 * category_similarity  # Assuming 20% weight to category similarity
    )

    # Step 6: Get similar videos
    # Convert the indices to Python int to avoid the TypeError
    similar_video_indices = [int(i) for i in combined_similarity[0].argsort()[::-1][1:6]]

    similar_videos = [(all_videos[i - 1],similar_video_indices[i-1]) for i in similar_video_indices]  # Adjust indexing

    return similar_videos




#get similar post for blogpost
def preprocess_content(content):
    """Remove HTML tags and return plain text."""
    return strip_tags(content)
def preprocess_combined_content(content, tags):
    """Combine content and tags into a single string."""
    return f"{preprocess_content(content)} {tags}"


def compute_combined_similarity(content1, tags1, content2, tags2):
    """Compute similarity between two blog posts considering both content and tags."""
    combined_content1 = preprocess_combined_content(content1, tags1)
    combined_content2 = preprocess_combined_content(content2, tags2)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([combined_content1, combined_content2])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity[0][0]


def get_post_contents():
    """Retrieve and preprocess post content."""
    posts = Post.objects.all()
    contents = [preprocess_content(post.content) for post in posts]
    return posts, contents

def compute_similarity_blogpost(content1, content2):
    """Compute similarity between two pieces of text."""
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([content1, content2])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity[0][0]


def find_similar_posts(blogpost_id):
    """Find posts similar to the given blog post."""
    target_blogpost = BlogPost.objects.get(id=blogpost_id)
    target_content = preprocess_content(target_blogpost.content)

    all_posts, all_contents = get_post_contents()

    # Calculate similarity
    similarities = []
    for post, content in zip(all_posts, all_contents):
        similarity_score = compute_similarity_blogpost(target_content, content)
        similarities.append((post, similarity_score))

    # Sort by similarity score
    similar_posts = sorted(similarities, key=lambda x: x[1], reverse=True)
    return [(post,score) for post, score in similar_posts]

def get_blogpost_contents():
    """Retrieve and preprocess blog post content."""
    blogposts = BlogPost.objects.all()
    contents = [preprocess_content(blogpost.content) for blogpost in blogposts]
    return blogposts, contents

def get_blogpost_tags(blogpost):
    """Retrieve tags as a space-separated string."""
    tags = blogpost.tags.all()
    return ' '.join(tag.name for tag in tags)

def find_similar_blogposts(current_blogpost_id):
    """Find blog posts similar to the given blog post."""
    # Get the target blog post and its content
    target_blogpost = BlogPost.objects.get(id=current_blogpost_id)
    target_content = preprocess_content(target_blogpost.content)

    # Retrieve all blog posts and their content
    all_blogposts, all_contents = get_blogpost_contents()

    # Calculate similarity
    similarities = []
    for blogpost, content in zip(all_blogposts, all_contents):
        if blogpost.id != current_blogpost_id:  # Exclude the current blog post
            similarity_score = compute_similarity(target_content, content)
            similarities.append((blogpost, similarity_score))

    # Sort by similarity score
    similar_blogposts = sorted(similarities, key=lambda x: x[1], reverse=True)
    return [(blogpost,score) for blogpost, score in similar_blogposts]


def find_similar_blogposts_with_tags(current_blogpost_id):
    """Find blog posts similar to the given blog post using both content and tags."""
    # Get the target blog post and its content and tags
    target_blogpost = BlogPost.objects.get(id=current_blogpost_id)
    target_content = preprocess_content(target_blogpost.content)
    target_tags = get_blogpost_tags(target_blogpost)

    # Retrieve all blog posts and their content and tags
    all_blogposts, all_contents, all_tags = get_blogpost_contents_and_tags()

    # Calculate similarity
    similarities = []
    for blogpost, content, tags in zip(all_blogposts, all_contents, all_tags):
        if blogpost.id != current_blogpost_id:  # Exclude the current blog post
            similarity_score = compute_combined_similarity(target_content, target_tags, content, tags)
            similarities.append((blogpost, similarity_score))

    # Sort by similarity score
    similar_blogposts = sorted(similarities, key=lambda x: x[1], reverse=True)
    return [(blogpost,score) for blogpost, score in similar_blogposts]
def get_blogpost_contents_and_tags():
    """Retrieve blog post contents and tags."""
    blogposts = BlogPost.objects.all()
    contents = [preprocess_content(blogpost.content) for blogpost in blogposts]
    tags = [get_blogpost_tags(blogpost) for blogpost in blogposts]
    return blogposts, contents, tags
def get_image_tags(image):
    """Retrieve image tags as a space-separated string."""
    tags = image.tags_img.all()
    return ' '.join(tag.name for tag in tags)

from sklearn.feature_extraction.text import TfidfVectorizer

def preprocess_content_imgblog(content):
    """Preprocess the blogpost or image content."""
    # Simple example; adjust as needed for your content
    return content.replace('\n', ' ').strip()

def preprocess_combined_content_imbblog(content, tags):
    """Combine content and tags into a single string."""
    return f"{preprocess_content(content)} {tags}"


from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def compute_similarity_imgblog(text1, tags1, text2, tags2):
    """Compute similarity between two text and tags combinations."""
    combined_content1 = preprocess_combined_content_imbblog(text1, tags1)
    combined_content2 = preprocess_combined_content_imbblog(text2, tags2)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([combined_content1, combined_content2])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity[0][0]

def find_similar_images_imgblog(blogpost_id):
    """Find images similar to the given blogpost using both content and tags."""
    # Get the target blogpost and its content and tags
    target_blogpost = BlogPost.objects.get(id=blogpost_id)
    target_content = preprocess_content_imgblog(target_blogpost.content)
    target_tags = get_blogpost_tags(target_blogpost)

    # Retrieve all images and their content and tags
    images = Image.objects.all()
    image_data = [(img, preprocess_content(img.description), get_image_tags(img)) for img in images]

    # Calculate similarity
    similarities = []
    for img, img_content, img_tags in image_data:
        similarity_score = compute_similarity_imgblog(target_content, target_tags, img_content, img_tags)
        similarities.append((img, similarity_score))

    # Sort by similarity score
    similar_images = sorted(similarities, key=lambda x: x[1], reverse=True)
    return [(img,score) for img, score in similar_images]

def find_similar_images_imgpost(blogpost_id):
    """Find images similar to the given blogpost using both content and tags."""
    # Get the target blogpost and its content and tags
    target_blogpost = Post.objects.get(id=blogpost_id)
    target_content = preprocess_content_imgblog(target_blogpost.content)
    target_tags = get_blogpost_tags(target_blogpost)

    # Retrieve all images and their content and tags
    images = Image.objects.all()
    image_data = [(img, preprocess_content(img.description), get_image_tags(img)) for img in images]

    # Calculate similarity
    similarities = []
    for img, img_content, img_tags in image_data:
        similarity_score = compute_similarity_imgblog(target_content, target_tags, img_content, img_tags)
        similarities.append((img, similarity_score))

    # Sort by similarity score
    similar_images = sorted(similarities, key=lambda x: x[1], reverse=True)
    return [(img,score) for img, score in similar_images]

def get_video_tags(video):
    """Retrieve tags for a Video as a space-separated string."""
    tags = video.tags.all()
    return ' '.join(tag.name for tag in tags)

def find_similar_videos_blogpost(blogpost):
    """Find videos similar to the given BlogPost using both content and tags."""
    # Get the target BlogPost and its content and tags


    target_blogpost = blogpost
    target_content = preprocess_content(target_blogpost.content)
    target_tags = get_blogpost_tags(target_blogpost)

    # Retrieve all videos and their content and tags
    videos = video.objects.all()
    video_data = [(vid, preprocess_content(vid.description), get_video_tags(vid)) for vid in videos]

    # Calculate similarity
    similarities = []
    for vid, vid_content, vid_tags in video_data:
        similarity_score = compute_similarity_imgblog(target_content, target_tags, vid_content, vid_tags)
        similarities.append((vid, similarity_score))

    # Sort by similarity score
    similar_videos = sorted(similarities, key=lambda x: x[1], reverse=True)
    return [(vid,score) for vid, score in similar_videos]
##############################################################
# for videos to find similar videos
##############################################################

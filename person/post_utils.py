from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Post,BlogPost


def preprocess_text(title, content, tags):
    """Combine and preprocess title, content, and tags into a single string."""
    combined_text = f"{title} {content} {tags}"
    return combined_text.replace('\n', ' ').strip()

def calculate_text_similarity(text1, text2):
    """Calculate similarity score between two pieces of text."""
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity_score[0][0]

def get_tags_as_string(instance, field_name):
    """Retrieve tags for an instance as a space-separated string."""
    tags = getattr(instance, field_name).all()
    return ' '.join(tag.name for tag in tags)


def find_similar_posts_to_post(post_id):
    """Find posts similar to the given post based on content and tags."""
    # Retrieve the target post
    target_post = Post.objects.get(id=post_id)

    # Prepare the target post's content for comparison
    target_tags = get_tags_as_string(target_post, 'tags')
    target_content = preprocess_text(target_post.title, target_post.content, target_tags)

    # Retrieve all posts and prepare their content for comparison
    posts = Post.objects.exclude(id=post_id)  # Exclude the target post from the comparison
    post_data = [
        (post, preprocess_text(
            post.title,
            post.content,
            get_tags_as_string(post, 'tags')
        ))
        for post in posts
    ]

    # Calculate similarity scores between the target post and all other posts
    post_similarity_scores = []
    for post, post_content in post_data:
        similarity_score = calculate_text_similarity(target_content, post_content)
        post_similarity_scores.append((post, similarity_score))

    # Sort posts by similarity score in descending order
    similar_posts = sorted(post_similarity_scores, key=lambda x: x[1], reverse=True)

    # Return only the post objects
    return [(post,score) for post, score in similar_posts]


def find_similar_blogposts_to_post(post, data_object):
    """Find BlogPosts similar to the given Post based on content and tags."""
    # Retrieve the target post
    target_post = post

    # Prepare the target post's content for comparison
    target_tags = get_tags_as_string(target_post, 'tags')
    target_content = preprocess_text(target_post.title, target_post.content, target_tags)

    # Retrieve all blog posts and prepare their content for comparison
    blog_posts = data_object  # Adjust the query if needed
    blog_post_data = [
        (blog_post, preprocess_text(
            blog_post.title,
            blog_post.content,
            get_tags_as_string(blog_post, 'tags')
        ))
        for blog_post in blog_posts
    ]

    # Calculate similarity scores between the target post and all blog posts
    blog_post_similarity_scores = []
    for blog_post, blog_post_content in blog_post_data:
        similarity_score = calculate_text_similarity(target_content, blog_post_content)
        blog_post_similarity_scores.append((blog_post, similarity_score))

    # Sort blog posts by similarity score in descending order
    similar_blog_posts = sorted(blog_post_similarity_scores, key=lambda x: x[1], reverse=True)

    # Return only the blog post objects
    return [(blog_post,score) for blog_post, score in similar_blog_posts]

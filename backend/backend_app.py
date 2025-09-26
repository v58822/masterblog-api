from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route("/api/posts", methods=["GET"])
def get_posts():

    sort_field = request.args.get("sort")
    direction = request.args.get("direction", "asc")

    posts = POSTS
    if sort_field:
        if sort_field not in ["title", "content"]:
            return jsonify({"error": "You can only sort by: 'title' or 'content'"}), 400
        if direction not in ["asc", "desc"]:
            return jsonify({"error": "Invalid sort direction"}), 400
        posts = sorted(
            POSTS,
            key=lambda post: post[sort_field].lower(),
            reverse=direction == "desc",
        )
    return jsonify(posts)


@app.route("/api/posts", methods=["POST"])
def add_post():

    # reading data from dict
    data = request.get_json()
    if "title" not in data:
        return jsonify({"error": "Missing field: title"}), 400
    if "content" not in data:
        return jsonify({"error": "Missing field: content"}), 400

    title = data["title"].strip()
    content = data["content"].strip()

    if not title:
        return jsonify({"error": "Title cannot be empty"}), 400
    if not content:
        return jsonify({"error": "Content cannot be empty"}), 400

    # creating a new ID
    try:
        new_id = max(post["id"] for post in POSTS) + 1
    except ValueError:  # List would be empty here
        new_id = 1

    new_post = {"id": new_id, "title": title, "content": content}

    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route("/api/posts/<int:id>", methods=["DELETE"])
def delete_post(id):
    for post in POSTS:
        if post["id"] == id:
            POSTS.remove(post)
            return (
                jsonify(
                    {"message": f"Post with id {id} has been deleted successfully."}
                ),
                200,
            )
    return jsonify({"message": f"Post with id {id} was not found."}), 404


@app.route("/api/posts/<int:id>", methods=["PUT"])
def update_post(id):

    data = request.get_json()

    # search for post
    for post in POSTS:
        if post["id"] == id:
            if "title" in data:
                title = data["title"].strip()
                if not title:
                    return jsonify({"error": "Title cannot be empty"}), 400
                post["title"] = title

            if "content" in data:
                content = data["content"].strip()
                if not content:
                    return jsonify({"error": "Content cannot be empty"}), 400
                post["content"] = content

            return jsonify(post), 200

    return jsonify({"message": f"Post with id {id} was not found."}), 404


@app.route("/api/posts/search", methods=["GET"])
def search_posts():

    title = request.args.get("title")
    content = request.args.get("content")

    results = []

    for post in POSTS:
        if title and title.lower() in post["title"].lower():
            if post not in results:
                results.append(post)
        if content and content.lower() in post["content"].lower():
            if post not in results:
                results.append(post)
    return jsonify(results), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)

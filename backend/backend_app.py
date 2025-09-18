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
    return jsonify(POSTS)


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)

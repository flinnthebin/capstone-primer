from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    return jsonify(db.get_all_students()), 200


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """

    data = request.json
    name = data.get("name")
    course = data.get("course")
    mark = data.get("mark")

    if not name:
        return jsonify({"error": "a girl has no name"}), 404
    if not course:
        return jsonify({"error": "a girl has no course"}), 404
    if mark is not None:
        try:
            mark = int(mark)
        except (ValueError, TypeError):
            return jsonify({"error": "a girl has no marks"}), 404
        if not 0 <= mark <= 100:
            return jsonify({"error": "a girl has no marks"}), 404

    student = db.insert_student(name, course, mark)
    return jsonify(student), 200


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    if db.get_student_by_id(student_id) is None:
        return jsonify({"error": "id does not exist"}), 404

    data = request.json
    name = data.get("name")
    course = data.get("course")
    mark = data.get("mark")

    if not name:
        return jsonify({"error": "a girl has no name"}), 404
    if not course:
        return jsonify({"error": "a girl has no course"}), 404
    if mark is not None:
        try:
            mark = int(mark)
        except (ValueError, TypeError):
            return jsonify({"error": "a girl has no marks"}), 404
        if not 0 <= mark <= 100:
            return jsonify({"error": "a girl has no marks"}), 404

    student_data = db.update_student(student_id, name, course, mark)
    return jsonify(student_data), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    if db.get_student_by_id(student_id) is None:
        return jsonify({"error": "student not found"}), 404
    db.delete_student(student_id)
    return '', 200


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    marks = []
    data = db.get_all_students()
    for i in data:
        mark = i.get("mark")
        if type(mark) is int:
            marks.append(mark)

    if not mark:
        jsonify({"count": 0,"average": 0, "min": 0, "max": 0}), 200
    return jsonify({
            "count": len(marks),
           "average": round(sum(marks) / len(marks), 2),
            "min": min(marks),
            "max": max(marks),
        }), 200


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

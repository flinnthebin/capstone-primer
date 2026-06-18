# Document your edge case here
- To get marks for this section you will need to explain to your tutor:
1) The edge case you identified

Students have names, courses and optionally, marks. When trying to aggregate marks under stats, I kept getting:

automark-1  | Status 200
automark-1  | FAIL: GET /stats failed (implement the /stats endpoint)

for this code:

```python
marks = []
    data = db.get_all_students()
    for i in data:
        mark = i.get("mark")
        marks.append(mark)

    return jsonify({
            "count": len(marks),
           "average": round(sum(marks) / len(marks), 2),
            "min": min(marks),
            "max": max(marks),
        }), 200
```
Which I couldn't understand until I realised that students with no marks have NULL marks.

2) How you have accounted for this in your implementation

To account for this in my implementation, we type check marks as they come in to filter out NULL (or None bc python).

```python
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

    return jsonify({
            "count": len(marks),
           "average": round(sum(marks) / len(marks), 2),
            "min": min(marks),
            "max": max(marks),
        }), 200
```

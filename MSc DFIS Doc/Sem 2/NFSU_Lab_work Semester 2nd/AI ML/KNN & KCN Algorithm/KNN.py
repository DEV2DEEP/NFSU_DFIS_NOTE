# -------------------------------
# KNN Algorithm 
# -------------------------------

import matplotlib.pyplot as plt

# Student Dataset
students = [
    {"name": "Aman", "roll": 1, "class": "BSc", "marks": 85, "result": "Pass"},
    {"name": "Riya", "roll": 2, "class": "BSc", "marks": 40, "result": "Fail"},
    {"name": "Karan", "roll": 3, "class": "BSc", "marks": 75, "result": "Pass"},
    {"name": "Neha", "roll": 4, "class": "BSc", "marks": 30, "result": "Fail"},
    {"name": "Vikram", "roll": 5, "class": "BSc", "marks": 90, "result": "Pass"}
]

# Function to calculate distance (without math library)
def distance(x1, x2):
    return (x1 - x2) * (x1 - x2)  # Squared distance

# KNN function
def knn_predict(new_marks, k):
    distances = []

    for student in students:
        d = distance(new_marks, student["marks"])
        distances.append((d, student["result"]))

    distances.sort()
    nearest = distances[:k]

    pass_count = 0
    fail_count = 0

    for item in nearest:
        if item[1] == "Pass":
            pass_count += 1
        else:
            fail_count += 1

    if pass_count > fail_count:
        return "Pass"
    else:
        return "Fail"


# ---- Test ----
new_student_marks = 60
prediction = knn_predict(new_student_marks, 3)

print("New Student Marks:", new_student_marks)
print("Predicted Result:", prediction)

# -------------------------------
# Graph Visualization
# -------------------------------

# Separate Pass and Fail students
pass_marks = []
fail_marks = []

for student in students:
    if student["result"] == "Pass":
        pass_marks.append(student["marks"])
    else:
        fail_marks.append(student["marks"])

# Plot existing students
plt.scatter(pass_marks, [1]*len(pass_marks), marker='o')
plt.scatter(fail_marks, [0]*len(fail_marks), marker='x')

# Plot new student
if prediction == "Pass":
    plt.scatter(new_student_marks, 1, marker='D')
else:
    plt.scatter(new_student_marks, 0, marker='D')

# Labels
plt.yticks([0,1], ["Fail", "Pass"])
plt.xlabel("Marks")
plt.title("KNN Student Classification Graph")

plt.show()

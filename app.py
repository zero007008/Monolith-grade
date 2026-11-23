
from flask import Flask, request, render_template_string
from collections import Counter

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Monolith | Activity Analyzer</title>
<style>
*{box-sizing:border-box}
body{
 margin:0;background:#080914;color:#f3f0ff;
 font-family:Arial,sans-serif;padding:20px;
}
.container{max-width:950px;margin:auto}
header{text-align:center;padding:25px 5px}
h1{color:#b99aff;margin-bottom:8px}
.sub{color:#9993b7;font-size:14px}
.panel{
 background:#141329;border:1px solid #39305c;
 border-radius:17px;padding:20px;margin-bottom:18px;
}
h2{font-size:19px;color:#c6adff}
input,textarea{
 width:100%;padding:13px;margin:6px 0 14px;
 border:1px solid #39345b;border-radius:9px;
 background:#0c0b1b;color:white;font-size:15px;
}
label{font-size:13px;color:#bdb5d8}
button{
 border:0;padding:12px 18px;border-radius:9px;
 background:#8755e8;color:white;font-weight:bold;
 cursor:pointer;margin:4px;
}
button.secondary{background:#292442}
button.danger{background:#7c304c}
.member{
 border:1px solid #39305c;padding:15px;
 border-radius:12px;margin:12px 0;
}
.stats{
 display:grid;grid-template-columns:repeat(3,1fr);
 gap:10px;margin:15px 0;
}
.stat{
 background:#211b3b;border-radius:12px;padding:15px;
 text-align:center;
}
.stat strong{display:block;font-size:26px;color:#c5a4ff}
.stat span{font-size:12px;color:#aaa}
.tag{
 display:inline-block;background:#30234e;
 color:#d6c5ff;padding:6px 10px;
 border-radius:20px;margin:4px;font-size:12px;
}
.result{border-left:3px solid #9c70ff;padding:12px 15px;
 margin:15px 0;background:#1b1830;border-radius:8px}
.small{color:#aaa;font-size:13px}
@media(max-width:500px){
 body{padding:10px}
 .stats{grid-template-columns:1fr 1fr}
}
@media print{
 body{background:white;color:#222}
 .no-print{display:none!important}
 .panel,.stat,.result{background:white;color:#222;border:1px solid #ddd}
 h1,h2,.stat strong{color:#542b99}
 .small,.sub,.stat span{color:#555}
}
</style>
</head>
<body>
<div class="container">
<header>
 <h1>MONOLITH</h1>
 <div class="sub">SOCIAL NETWORK ANALYZER</div>
 <p>Member Activity & Responsibility Analysis</p>
</header>

<form action="/analyze" method="POST" id="mainForm">
 <div class="panel">
  <h2>Member Information</h2>
  <div id="members">
   <div class="member">
    <label>Student ID</label>
    <input name="student_id[]" placeholder="Enter Student ID">
    <label>Member Name</label>
    <input name="member_name[]" placeholder="Enter Member Name">
    <label>Activity / Assigned Topics</label>
    <textarea name="activity[]" rows="3"
    placeholder="Enter activities or assigned topics"></textarea>
   </div>
  </div>
  <button type="button" onclick="addMember()">+ Add Member</button>
  <button type="submit">Analyze Activities</button>
 </div>
</form>

<script>
function addMember(){
 const box=document.createElement('div');
 box.className='member';
 box.innerHTML=`
 <label>Student ID</label>
 <input name="student_id[]" placeholder="Enter Student ID">
 <label>Member Name</label>
 <input name="member_name[]" placeholder="Enter Member Name">
 <label>Activity / Assigned Topics</label>
 <textarea name="activity[]" rows="3"
 placeholder="Enter activities or assigned topics"></textarea>
 <button type="button" class="danger"
 onclick="this.parentElement.remove()">Remove</button>`;
 document.getElementById('members').appendChild(box);
}
</script>
</div>
</body>
</html>
"""

REPORT = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Analysis Report | Monolith</title>
<style>
*{box-sizing:border-box}
body{background:#080914;color:#eee;font-family:Arial;padding:18px}
.container{max-width:900px;margin:auto}
.panel{background:#17152c;border:1px solid #40345e;
 border-radius:15px;padding:20px;margin:15px 0}
h1,h2{color:#c5a5ff}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.stat{background:#282044;padding:17px;border-radius:12px}
.stat strong{display:block;font-size:27px;color:#c6a6ff}
.member{padding:16px;background:#201c36;border-radius:12px;margin:12px 0}
.tag{display:inline-block;background:#352851;padding:7px 10px;
 border-radius:20px;margin:4px;font-size:12px;color:#e2d2ff}
.small{color:#aaa;font-size:13px}
button{padding:12px 18px;border:0;border-radius:9px;
 background:#8755e8;color:white;margin:5px;cursor:pointer}
@media(max-width:500px){.stats{grid-template-columns:1fr 1fr}}
@media print{
 body{background:white;color:#222}
 .no-print{display:none}
 .panel,.stat,.member{background:white;color:#222;border:1px solid #ddd}
 h1,h2,.stat strong{color:#542b99}
 .small{color:#555}
}
</style>
</head>
<body>
<div class="container">
<header>
<h1>MONOLITH</h1>
<p>Social Network Analyzer — Activity Report</p>
<p class="small">Generated Member Responsibility Analysis</p>
</header>

<div class="panel">
<h2>Group Overview</h2>
<div class="stats">
 <div class="stat"><strong>{{total}}</strong><span>Members</span></div>
 <div class="stat"><strong>{{activities}}</strong><span>Activity Entries</span></div>
 <div class="stat"><strong>{{topics}}</strong><span>Unique Topics</span></div>
</div>
</div>

<div class="panel">
<h2>Member Responsibilities</h2>
{% for m in members %}
<div class="member">
 <h3>{{m.name}}</h3>
 <p class="small">Student ID: {{m.sid}}</p>
 <p><b>Assigned Activities</b></p>
 {% for a in m['items'] %}
 <div class="tag">{{a}}</div>
{% endfor %}
 <p class="small">Activity count: {{m.count}}</p>
</div>
{% endfor %}
</div>

<div class="panel">
<h2>Analysis Summary</h2>
<p>{{summary}}</p>
<h3>Data Quality</h3>
<p>Missing information: {{missing}}</p>
<p>Duplicate activity entries: {{duplicates}}</p>
<h3>Activity Distribution</h3>
{% for name,count in distribution %}
<p>{{name}} — {{count}} topic(s)</p>
{% endfor %}
</div>

<div class="no-print">
<button onclick="window.print()">Print / Save PDF</button>
<button onclick="location.href='/'">Back to Input</button>
</div>
</div>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(PAGE)


@app.route("/analyze", methods=["POST"])
def analyze():
    ids = request.form.getlist("student_id[]")
    names = request.form.getlist("member_name[]")
    activities = request.form.getlist("activity[]")

    members = []
    all_topics = []
    missing = 0

    for sid, name, activity in zip(ids, names, activities):
        sid = sid.strip()
        name = name.strip()
        activity = activity.strip()

        if not sid or not name or not activity:
            missing += 1
            continue

        items = [
            x.strip()
            for x in activity.replace("\n", ";").split(";")
            if x.strip()
        ]

        members.append({
            "sid": sid,
            "name": name,
            "items": items,
            "count": len(items)
        })

        all_topics.extend(x.lower() for x in items)

    if not members:
        return "No valid member data. Please go back and enter information.", 400

    duplicate_count = len(all_topics) - len(set(all_topics))
    distribution = Counter(all_topics)

    total = len(members)
    topic_count = len(all_topics)
    unique_topics = len(distribution)

    average = topic_count / total

    summary = (
        f"The group contains {total} members with "
        f"{topic_count} activity entries and "
        f"{unique_topics} unique topics. "
        f"The average number of topics per member is "
        f"{average:.1f}. "
    )

    if duplicate_count:
        summary += (
            f"{duplicate_count} repeated activity entries "
            f"were detected. Review them to avoid overlapping work."
        )
    else:
        summary += "No repeated activity entries were detected."

    return render_template_string(
        REPORT,
        members=members,
        total=total,
        activities=topic_count,
        topics=unique_topics,
        missing=missing,
        duplicates=duplicate_count,
        summary=summary,
        distribution=sorted(
            distribution.items(),
            key=lambda x: x[1],
            reverse=True
        )
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

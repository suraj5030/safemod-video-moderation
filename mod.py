import boto3, time

r = boto3.client("rekognition")
j = r.start_content_moderation(
    Video={"S3Object": {"Bucket": "safemod-test-suraj", "Name": "test.mp4"}},
    MinConfidence=50
)["JobId"]

while (res := r.get_content_moderation(JobId=j))["JobStatus"] == "IN_PROGRESS":
    time.sleep(5)

print(res["JobStatus"])
for m in res.get("ModerationLabels", []):
    l = m["ModerationLabel"]
    if l["ParentName"] and l["Name"] != l["ParentName"]:
        if not any(x["ModerationLabel"]["ParentName"] == l["Name"] and x["Timestamp"] == m["Timestamp"] for x in res["ModerationLabels"]):
            print(f'{m["Timestamp"]/1000:.1f}s  {l["Name"]}  {l["Confidence"]:.1f}%')
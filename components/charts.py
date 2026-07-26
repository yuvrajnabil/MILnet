import plotly.express as px
import pandas as pd

def vote_chart(votes):
    order = ["Real", "Fake", "Not sure"]
    counts = {k: 0 for k in order}
    for vote in votes:
        counts[vote.vote] = counts.get(vote.vote, 0) + 1
    df = pd.DataFrame({"Vote": list(counts.keys()), "Count": list(counts.values())})
    return px.bar(df, x="Vote", y="Count", text="Count", title="Public voting results")

def social_platform_chart(df):
    grouped = df.groupby("Platform", as_index=False)["Engagement"].sum()
    return px.bar(grouped, x="Platform", y="Engagement", text_auto=True, title="Engagement by platform")

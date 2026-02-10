import duckdb
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from implicit.als import AlternatingLeastSquares
import umap
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.sparse import csr_matrix

def reduce_to_3d(embeddings, n_neighbors = 15, min_dist = 0.1, random_state = 42):
    reducer = umap.UMAP(
        n_components=3,
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        random_state=random_state,
        metric='cosine'
    )

    embeddings_3d = reducer.fit_transform(embeddings)
    return embeddings_3d

def create_user_visualization(embeddings_3d, user_ids):
    fig = go.Figure()

    fig.add_trace(go.Scatter3d(
        x=embeddings_3d[:100_000, 0],
        y=embeddings_3d[:100_000, 1],
        z=embeddings_3d[:100_000, 2],
        mode='markers',
        marker=dict(
            size=5,
            colorscale="viridis",
            color="rgba(0,0,255,0.8)"
        ),
        text=[f"User {uid}" for uid in user_ids[:100_000]]
    ))

    fig.update_layout(
        title="User Embeddings (UMAP 3D)",
        scene=dict(
            xaxis_title="UMAP 1",
            yaxis_title="UMAP 2",
            zaxis_title="UMAP 3"
        ),
        width=1000,
        height=800
    )

    return fig

PARQUET_PATH = "../2022_place_canvas_history.parquet"

query = f"""
    SELECT
        user_id,
        CONCAT(x1, ',', y1) AS coord,
        COUNT(*) AS freq
    FROM
        '{PARQUET_PATH}'
    WHERE
        timestamp <= '2022-04-02 12:00:00'
    GROUP BY
        user_id, x1, y1
"""

df = duckdb.query(query).df()

embeddings = np.load("user_embeddings.npy")
clusters_3d = np.load("day1_cluster_data.npy")

user_ids = df["user_id"].unique()
u_fig = create_user_visualization(clusters_3d, user_ids)
u_fig.update_layout(title="Day 1 User Embeddings")
# u_fig.write_html("day_1_als_3d.html")

u_fig.show()
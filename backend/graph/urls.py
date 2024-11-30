# energy_graph/urls.py
from django.urls import path
from .views import NodeView, EdgeView, GraphView

urlpatterns = [
    path("nodes/", NodeView.as_view(), name="node-list"),
    path("edges/", EdgeView.as_view(), name="edge-list"),
    path("graph/", GraphView.as_view(), name="graph"),
]

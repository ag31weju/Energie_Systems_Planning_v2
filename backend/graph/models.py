# Define Node and Edge as Django models to persist the data.
from django.db import models

# Create your models here.
# graph/models.py


class Node(models.Model):
    NODE_TYPES = [
        # consumers
        ("Residential", "Residential"),
        ("Commercial", "Commercial"),
        ("University", "University"),
        # producers
        ("Coal Power Plant", "Coal"),
        ("Wind Turbine", "Wind"),
        ("Nuclear Power Plant", "Nuclear"),
        ("Solar Power Plant", "Solar"),
    ]

    node_id = models.CharField(max_length=50, unique=True)
    node_type = models.CharField(max_length=20, choices=NODE_TYPES)
    x = models.FloatField()
    y = models.FloatField()
    parameters = models.JSONField(default=dict)  # To store additional parameters

    def __str__(self):
        return f"{self.node_id} ({self.node_type})"


class Edge(models.Model):
    start_node = models.ForeignKey(
        Node, related_name="outgoing_edges", on_delete=models.CASCADE
    )
    end_node = models.ForeignKey(
        Node, related_name="incoming_edges", on_delete=models.CASCADE
    )
    weight = models.FloatField(default=1.0)
    properties = models.JSONField(default=dict)  # To store additional edge properties

    def __str__(self):
        return f"{self.start_node.node_id} -> {self.end_node.node_id} (Weight: {self.weight})"

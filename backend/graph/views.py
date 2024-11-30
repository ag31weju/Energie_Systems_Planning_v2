#Create views for CRUD operations and APIs for adding nodes/edges and retrieving the graph.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Node, Edge
from .serializers import NodeSerializer, EdgeSerializer
from .services import EnergyGraph

class NodeView(APIView):
    def get(self, request):
        nodes = Node.objects.all()
        serializer = NodeSerializer(nodes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EdgeView(APIView):
    def get(self, request):
        edges = Edge.objects.all()
        serializer = EdgeSerializer(edges, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EdgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GraphView(APIView):
    def get(self, request):
        graph = EnergyGraph()
        nodes = NodeSerializer(graph.nodes, many=True).data
        edges = EdgeSerializer(graph.edges, many=True).data
        return Response({"nodes": nodes, "edges": edges})

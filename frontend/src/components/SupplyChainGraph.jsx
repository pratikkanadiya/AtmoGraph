import { useEffect, useState } from "react";

import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
} from "@xyflow/react";

import "@xyflow/react/dist/style.css";


function SupplyChainGraph() {

  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);

  const [selectedNode, setSelectedNode] = useState(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);


  useEffect(() => {

    fetch("http://127.0.0.1:8000/graph")

      .then((response) => {

        if (!response.ok) {
          throw new Error("Failed to load graph data");
        }

        return response.json();
      })

      .then((data) => {

        console.log("GRAPH DATA:", data);

        const flowNodes = data.nodes
          .filter((node) => node.id && node.name)
          .map((node, index) => ({
            id: node.id,

            position: {
              x: (index % 4) * 300,
              y: Math.floor(index / 4) * 200,
            },

            data: {
              label: node.name,
              ...node,
            },
          }));


        const flowEdges = data.relationships
          .filter(
            (relationship) =>
              relationship.source &&
              relationship.target
          )
          .map((relationship) => ({
            id: relationship.id,

            source: relationship.source,

            target: relationship.target,

            label: relationship.type,
          }));


        console.log("FLOW NODES:", flowNodes);
        console.log("FLOW EDGES:", flowEdges);

        setNodes(flowNodes);
        setEdges(flowEdges);

        setLoading(false);
      })

      .catch((error) => {

        console.error("GRAPH ERROR:", error);

        setError(error.message);

        setLoading(false);
      });

  }, []);


  const handleNodeClick = (event, node) => {

    console.log("SELECTED NODE:", node);

    setSelectedNode(node.data);
  };



  if (loading) {

    return (
      <div
        style={{
          width: "100%",
          height: "650px",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        Loading supply chain graph...
      </div>
    );
  }


  if (error) {

    return (
      <div
        style={{
          width: "100%",
          height: "650px",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "red",
        }}
      >
        Failed to load graph: {error}
      </div>
    );
  }


  return (

    <div
      style={{
        position: "relative",
        width: "100%",
        height: "650px",
        minHeight: "650px",
      }}
    >

      <div
        style={{
          width: "100%",
          height: "650px",
          minHeight: "650px",
          border: "1px solid #d1d5db",
          borderRadius: "12px",
          overflow: "hidden",
        }}
      >

        <ReactFlow
          nodes={nodes}
          edges={edges}
          fitView
          onNodeClick={handleNodeClick}
          style={{
            width: "100%",
            height: "100%",
          }}
        >

          <Background />

          <Controls />

          <MiniMap />

        </ReactFlow>

      </div>


      {selectedNode && (

        <div
          style={{
            position: "absolute",
            top: "20px",
            right: "20px",
            width: "300px",
            padding: "20px",
            background: "white",
            borderRadius: "12px",
            boxShadow: "0 8px 30px rgba(0,0,0,0.15)",
            zIndex: 10,
          }}
        >

          <button
            onClick={() => setSelectedNode(null)}
            style={{
              position: "absolute",
              top: "8px",
              right: "10px",
              border: "none",
              background: "transparent",
              fontSize: "24px",
              cursor: "pointer",
            }}
          >
            ×
          </button>


          <h3>
            {selectedNode.name}
          </h3>


          <p>
            <strong>ID:</strong>{" "}
            {selectedNode.id}
          </p>


          <p>
            <strong>Type:</strong>{" "}
            {selectedNode.labels?.join(", ")}
          </p>


          {selectedNode.country && (
            <p>
              <strong>Country:</strong>{" "}
              {selectedNode.country}
            </p>
          )}


          {selectedNode.risk_level && (
            <p>
              <strong>Risk Level:</strong>{" "}
              {selectedNode.risk_level}
            </p>
          )}


          {selectedNode.risk_score !== null &&
            selectedNode.risk_score !== undefined && (
              <p>
                <strong>Risk Score:</strong>{" "}
                {selectedNode.risk_score}
              </p>
            )}


          {selectedNode.risk_status && (
            <p>
              <strong>Status:</strong>{" "}
              {selectedNode.risk_status}
            </p>
          )}


          {selectedNode.risk_confidence !== null &&
            selectedNode.risk_confidence !== undefined && (
              <p>
                <strong>Confidence:</strong>{" "}
                {(selectedNode.risk_confidence * 100).toFixed(1)}%
              </p>
            )}

        </div>
      )}

    </div>
  );
}


export default SupplyChainGraph;
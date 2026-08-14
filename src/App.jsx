import { useState } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  Handle,
  Position,
} from "@xyflow/react";

import "@xyflow/react/dist/style.css";
import "./App.css";

const CustomNode = ({ data }) => {
  return (
    <div className={`custom-node ${data.type}`}>
      <Handle type="target" position={Position.Left} />

      <div className="node-title">{data.label}</div>
      <div className="node-type">{data.type}</div>

      <Handle type="source" position={Position.Right} />
    </div>
  );
};
const initialNodes = [
  {
    id: "supplier-1",
    position: { x: 50, y: 100 },
    data: {
    label: "Supplier A",
    type: "supplier",
},
  },
  {
    id: "supplier-2",
    position: { x: 50, y: 350 },
    data: {
    label: "Supplier B",
    type: "supplier",
},
  },
  {
    id: "factory-1",
    position: { x: 300, y: 100 },
    data: {
  label: "Factory A",
  type: "factory",
},
  },
  {
    id: "factory-2",
    position: { x: 300, y: 350 },
    data: {
  label: "Factory B",
  type: "factory",
},
  },
  {
    id: "port-1",
    position: { x: 550, y: 100 },
    data: {
  label: "Port A",
  type: "port",
},
  },
  {
    id: "port-2",
    position: { x: 550, y: 350 },
    data: {
  label: "Port B",
  type: "port",
},
  },
  {
    id: "warehouse-1",
    position: { x: 800, y: 100 },
    data: { label: "Warehouse A" ,
      type : "warehouse"
    },
  },
  {
    id: "warehouse-2",
    position: { x: 800, y: 350 },
    data: { label: "Warehouse B" , type : "warehouse"},
  },
  {
    id: "retailer-1",
    position: { x: 1050, y: 100 },
    data: { label: "Retailer A" , type : "retailer" },
  },
  {
    id: "retailer-2",
    position: { x: 1050, y: 350 },
    data: { label: "Retailer B" , type : "retailer" },
  },
];

const initialEdges = [
  {
    id: "e-s1-f1",
    source: "supplier-1",
    target: "factory-1",
    label: "Supplies",
  },
  {
    id: "e-s1-f2",
    source: "supplier-1",
    target: "factory-2",
    label: "Supplies",
  },
  {
    id: "e-s2-f2",
    source: "supplier-2",
    target: "factory-2",
    label: "Supplies",
  },
  {
    id: "e-f1-p1",
    source: "factory-1",
    target: "port-1",
    label: "Ships through",
  },
  {
    id: "e-f1-p2",
    source: "factory-1",
    target: "port-2",
    label: "Ships through",
  },
  {
    id: "e-f2-p2",
    source: "factory-2",
    target: "port-2",
    label: "Ships through",
  },
  {
    id: "e-p1-w1",
    source: "port-1",
    target: "warehouse-1",
    label: "Transports to",
  },
  {
    id: "e-p2-w1",
    source: "port-2",
    target: "warehouse-1",
    label: "Transports to",
  },
  {
    id: "e-p2-w2",
    source: "port-2",
    target: "warehouse-2",
    label: "Transports to",
  },
  {
    id: "e-w1-r1",
    source: "warehouse-1",
    target: "retailer-1",
    label: "Supplies",
  },
  {
    id: "e-w1-r2",
    source: "warehouse-1",
    target: "retailer-2",
    label: "Supplies",
  },
  {
    id: "e-w2-r2",
    source: "warehouse-2",
    target: "retailer-2",
    label: "Supplies",
  },
];
const nodeTypes = {
  custom: CustomNode,
};

function App() {
  const [selectedNode, setSelectedNode] = useState(null);

  const handleNodeClick = (event, node) => {
    setSelectedNode(node);
  };

  return (
    <div className="app">
      <header className="header">
        <h1>AtmoGraph</h1>
        <p>Supply Chain Ripple Effect Predictor</p>
      </header>

      <div className="content">
        <div className="graph-container">
          <ReactFlow
  nodes={initialNodes.map((node) => ({
    ...node,
    type: "custom",
  }))}
  edges={initialEdges}
  nodeTypes={nodeTypes}
  onNodeClick={handleNodeClick}
  fitView
>
            <Background />
            <Controls />
            <MiniMap />
          </ReactFlow>
        </div>

        <div className="details-panel">
          <h2>Node Details</h2>

          {selectedNode ? (
            <>
              <h3>{selectedNode.data.label}</h3>
              <p>
                <strong>Node ID:</strong> {selectedNode.id}
              </p>
              <p>
                <strong>Status:</strong> Normal
              </p>
              <p>
                <strong>Risk:</strong> Low
              </p>
            </>
          ) : (
            <p>Click a node to view its details.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
} from "@xyflow/react";

import "@xyflow/react/dist/style.css";

const nodes = [
  {
    id: "supplier",
    position: { x: 50, y: 180 },
    data: { label: "Shanghai Semiconductor\nSupplier" },
  },
  {
    id: "shanghai",
    position: { x: 300, y: 180 },
    data: { label: "Shanghai Port" },
  },
  {
    id: "rotterdam",
    position: { x: 550, y: 80 },
    data: { label: "Rotterdam Port" },
  },
  {
    id: "la",
    position: { x: 800, y: 180 },
    data: { label: "Los Angeles Port" },
  },
  {
    id: "manufacturer",
    position: { x: 1050, y: 180 },
    data: { label: "Global Electronics Factory" },
  },
  {
    id: "warehouse",
    position: { x: 1300, y: 180 },
    data: { label: "California Warehouse" },
  },
  {
    id: "industry",
    position: { x: 1550, y: 180 },
    data: { label: "Consumer Electronics" },
  },
];

const edges = [
  {
    id: "e1",
    source: "supplier",
    target: "shanghai",
    label: "SUPPLIES",
  },
  {
    id: "e2",
    source: "shanghai",
    target: "rotterdam",
    label: "CONNECTED_TO",
  },
  {
    id: "e3",
    source: "rotterdam",
    target: "la",
    label: "CONNECTED_TO",
  },
  {
    id: "e4",
    source: "la",
    target: "manufacturer",
    label: "SHIPS_TO",
  },
  {
    id: "e5",
    source: "manufacturer",
    target: "warehouse",
    label: "SHIPS_TO",
  },
  {
    id: "e6",
    source: "warehouse",
    target: "industry",
    label: "SERVES",
  },
];

function SupplyChainGraph() {
  return (
    <div style={{ width: "100%", height: "650px" }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
      >
        <Background />
        <Controls />
        <MiniMap />
      </ReactFlow>
    </div>
  );
}

export default SupplyChainGraph;
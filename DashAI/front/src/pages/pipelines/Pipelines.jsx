import React, { useState, useCallback } from "react";
import { Box, Typography, Dialog, DialogTitle, DialogActions, Button } from "@mui/material";
import ReactFlow, { addEdge, Background, Controls, useEdgesState, useNodesState } from "reactflow";
import 'reactflow/dist/style.css';
import CustomLayout from "../../components/custom/CustomLayout";

import DataLoaderNode from "./nodes/DataLoaderNode";
import DataExplorationNode from "./nodes/DataExplorationNode";
import TaskSelectorNode from "./nodes/TaskSelectorNode";
import MetricsNode from "./nodes/MetricsNode";

// const nodeTypes = {
//   DataLoader: DataLoaderNode,
//   DataExploration: DataExplorationNode,
//   TaskSelector: TaskSelectorNode,
//   Metrics: MetricsNode,
// };

function PipelinesPage() {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selectedNode, setSelectedNode] = useState(null);
  const [dragging, setDragging] = useState(null);

  const onDragStart = (event, nodeType) => {
    setDragging(nodeType);
  };

  const onDrop = useCallback((event) => {
    event.preventDefault();
    const reactFlowBounds = event.target.getBoundingClientRect();
    const position = { x: event.clientX - reactFlowBounds.left, y: event.clientY - reactFlowBounds.top };
    
    const newNode = {
      id: `${dragging}-${nodes.length}`, 
      type: dragging, 
      position,
      data: { label: `${dragging} Node` },
    };

    setNodes((nds) => nds.concat(newNode));
  }, [dragging, nodes.length, setNodes]);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const onNodeClick = (event, node) => {
    setSelectedNode(node);
  };

  const handleCloseDialog = () => {
    setSelectedNode(null);
  };

  const renderNodeDialogContent = () => {
    if (!selectedNode) return null;
  
    const { type } = selectedNode;
  
    if (type === "DataLoader") {
      return <DataLoaderNode open={!!selectedNode} onClose={handleCloseDialog} />;
    } else if (type === "DataExploration") {
      return <DataExplorationNode open={!!selectedNode} onClose={handleCloseDialog} />;
    } else if (type === "TaskSelector") {
      return <TaskSelectorNode open={!!selectedNode} onClose={handleCloseDialog} />;
    } else if (type === "Metrics") {
      return <MetricsNode open={!!selectedNode} onClose={handleCloseDialog} />;
    }
    
    return null;
  };

  return (
    <CustomLayout title="Pipelines Module">
      <Box display="flex" height="100vh">
        <Box sx={{ width: 300, p: 2, backgroundColor: "#212121", overflowY: "auto" }}>
          <Typography variant="h6" gutterBottom sx={{ color: "#fff" }}>
            Nodes
          </Typography>

          <Box
            onDragStart={(e) => onDragStart(e, "DataLoader")}
            draggable
            sx={{ mb: 1, p: 1, backgroundColor: "#333", color: "#fff", borderRadius: 1, textAlign: "center", cursor: "grab" }}
          >
            <Typography>Data Loader</Typography>
          </Box>

          <Box
            onDragStart={(e) => onDragStart(e, "DataExploration")}
            draggable
            sx={{ mb: 1, p: 1, backgroundColor: "#333", color: "#fff", borderRadius: 1, textAlign: "center", cursor: "grab" }}
          >
            <Typography>Data Exploration</Typography>
          </Box>

          <Box
            onDragStart={(e) => onDragStart(e, "TaskSelector")}
            draggable
            sx={{ mb: 1, p: 1, backgroundColor: "#333", color: "#fff", borderRadius: 1, textAlign: "center", cursor: "grab" }}
          >
            <Typography>Task Selector</Typography>
          </Box>

          <Box
            onDragStart={(e) => onDragStart(e, "Metrics")}
            draggable
            sx={{ mb: 1, p: 1, backgroundColor: "#333", color: "#fff", borderRadius: 1, textAlign: "center", cursor: "grab" }}
          >
            <Typography>Metrics</Typography>
          </Box>
        </Box>

        <Box sx={{ flexGrow: 1, p: 2, backgroundColor: "#fff" }}>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onDrop={onDrop}
            onDragOver={(event) => event.preventDefault()}
            onNodeClick={onNodeClick} 
            // nodeTypes={nodeTypes}
            fitView
            style={{ width: '100%', height: '100%' }}
          >
            <Background />
            <Controls />
          </ReactFlow>
        </Box>

        <Dialog open={!!selectedNode} onClose={handleCloseDialog}>
          <DialogTitle>{selectedNode?.data?.label || "Node Details"}</DialogTitle>
          {renderNodeDialogContent()}
          <DialogActions>
            <Button onClick={handleCloseDialog} color="primary">
              Close
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </CustomLayout>
  );
}

export default PipelinesPage;

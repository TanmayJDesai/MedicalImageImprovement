import React, { useRef, useEffect, useState } from "react";
import { Canvas, Image, Rect, Textbox } from "fabric"; // Update imports
import "./App.css";

export default function OrigImageAnnotationTool({ improvedImage }) {
  const canvasRef = useRef(null);
  const fabricRef = useRef(null);

  useEffect(() => {
  const canvasElement = canvasRef.current;
  if (!improvedImage || !canvasElement) return;

  // Prevent double initialization
  if (canvasElement.__fabricInitialized) return;

  // Get visual size of canvas from DOM
  const { width, height } = canvasElement.getBoundingClientRect();

  // Set internal resolution
  canvasElement.width = width;
  canvasElement.height = height;

  // Initialize Fabric
  const canvas = new Canvas(canvasElement);
  canvas.setWidth(width);
  canvas.setHeight(height);

  fabricRef.current = canvas;

  // Mark DOM element as initialized
  canvasElement.__fabricInitialized = true;

  return () => {
    if (fabricRef.current) {
      fabricRef.current.dispose();
      fabricRef.current = null;
      canvasElement.__fabricInitialized = false;
    }
  };
}, [improvedImage]);

  

  const deleteSelectedAnnotation = () => {
    const canvas = fabricRef.current;
    const active = canvas.getActiveObject();
    if (!active || !active.annotationGroupId) return;

    const objectsToRemove = canvas
      .getObjects()
      .filter((obj) => obj.annotationGroupId === active.annotationGroupId);

    objectsToRemove.forEach((obj) => canvas.remove(obj));
    canvas.discardActiveObject();
    canvas.renderAll();
  };

  const createAnnotations = () => {
    const canvas = fabricRef.current;
    if (!canvas) return;

    const id = Date.now();

    const rect = new Rect({
      left: 100,
      top: 100,
      width: 150,
      height: 100,
      fill: "rgba(255,255,0,0.4)",
      stroke: "orange",
      strokeWidth: 2,
      selectable: true,
      annotationGroupId: id,
    });

    const text = new Textbox("Double-click to edit", {
      left: 110,
      top: 110,
      width: 130,
      fontSize: 16,
      fill: "black",
      backgroundColor: "white",
      editable: true,
      selectable: true,
      annotationGroupId: id,
    });

    canvas.add(rect);
    canvas.add(text);
    canvas.setActiveObject(text);

    // Keep them visually synced
    rect.on("moving", () => {
      text.set({
        left: rect.left + 10,
        top: rect.top + 10,
      });
      canvas.renderAll();
    });
  };

  return (
    <div className="annotation-container">
      <div className="annotation-controls">
        <button onClick={createAnnotations} className="annotate-button">
          Add Highlight + Text
        </button>
        <button onClick={deleteSelectedAnnotation} className="delete-button">
          Delete Selected
        </button>
      </div>
      <h3>Annotate Original Image</h3>
      <div
        className="annotation-wrapper"
        style={{
          backgroundImage: `url(${improvedImage})`,
          backgroundSize: "contain",
          backgroundRepeat: "no-repeat",
          backgroundPosition: "center",
          position: "relative",
          width: "100%",
          maxWidth: "1000px",
          aspectRatio: "16 / 9", // or set a height
          margin: "0 auto",
        }}
      >
        <canvas
          ref={canvasRef}
          className="display-canvas"
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            pointerEvents: "auto",
          }}
        />
      </div>
    </div>
  );
}

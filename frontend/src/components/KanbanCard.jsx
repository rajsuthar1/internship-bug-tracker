import React from 'react';
import { useDraggable } from '@dnd-kit/core';
import { CSS } from '@dnd-kit/utilities';

const KanbanCard = ({ issue, onDelete, onEdit }) => {
  const { attributes, listeners, setNodeRef, transform, isDragging } = useDraggable({
    id: issue.id,
  });

  const style = {
    transform: CSS.Translate.toString(transform),
    opacity: isDragging ? 0.6 : 1,
    zIndex: isDragging ? 999 : 1,
  };

  return (
    <div 
      ref={setNodeRef} 
      style={style} 
      className={`issue-card ${isDragging ? 'dragging' : ''}`}
      {...attributes}
    >
      <div className="issue-header">
        <span className="issue-id">#{issue.id}</span>
        <div className="card-actions">
          {/* Edit Button */}
          <button 
            className="edit-btn" 
            title="Edit Issue"
            onClick={() => onEdit(issue)}
          >
            ✏️
          </button>
          
          {/* Delete Button */}
          <button 
            className="delete-btn" 
            title="Delete Issue"
            onClick={() => onDelete(issue.id)}
          >
            ×
          </button>
        </div>
      </div>
      
      {/* DRAG HANDLE: We attach listeners ONLY to the content area. 
         This prevents action buttons from triggering a drag. 
      */}
      <div className="issue-content" {...listeners}>
        <h3>{issue.title}</h3>
        <p>{issue.description}</p>
        <div className="drag-handle-hint">⋮⋮ Drag to move</div>
      </div>
    </div>
  );
};

export default KanbanCard;
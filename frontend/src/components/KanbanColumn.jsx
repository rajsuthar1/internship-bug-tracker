import React from 'react';
import { useDroppable } from '@dnd-kit/core';
import KanbanCard from './KanbanCard';

const KanbanColumn = ({ id, title, issues, onDelete, onEdit }) => {
  // isOver is a boolean that tells us if a card is currently hovering here
  const { setNodeRef, isOver } = useDroppable({ id });

  return (
    <div 
      ref={setNodeRef} 
      className={`kanban-column ${isOver ? 'drag-over' : ''}`}
    >
      <div className="column-header">
        <h3>{title}</h3>
        <span className="count">{issues.length}</span>
      </div>
      
      <div className="column-content">
        {issues.map((issue) => (
          <KanbanCard 
            key={issue.id} 
            issue={issue} 
            onDelete={onDelete} 
            onEdit={onEdit} 
          />
        ))}
        
        {/* Visual placeholder if column is empty and being hovered */}
        {issues.length === 0 && isOver && (
          <div className="column-placeholder">Drop here</div>
        )}
      </div>
    </div>
  );
};

export default KanbanColumn;
import { useEffect, useState } from 'react'
import { DndContext, closestCorners, KeyboardSensor, PointerSensor, useSensor, useSensors } from '@dnd-kit/core'
import { sortableKeyboardCoordinates } from '@dnd-kit/sortable'
import { getIssues, createIssue, deleteIssue, updateIssue } from './api/issueService'
// Assuming you create this small service to fetch projects
import axios from 'axios' 

import KanbanColumn from './components/KanbanColumn'
import './App.css'

function App() {
  const [issues, setIssues] = useState([])
  const [projects, setProjects] = useState([]) // New: Store all projects
  const [currentProjectId, setCurrentProjectId] = useState(4) // Start with your new project
  const [searchTerm, setSearchTerm] = useState('')
  const [showModal, setShowModal] = useState(false)
  const [editingIssueId, setEditingIssueId] = useState(null)
  const [formData, setFormData] = useState({ title: '', description: '', project_id: 4, status: 'To Do' })

  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 5 } }),
    useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates })
  )

  // Load projects and issues
  const loadData = async () => {
    try {
      // Fetch Projects for the dropdown
      const projRes = await axios.get("http://127.0.0.1:8000/api/v1/projects/");
      setProjects(projRes.data);
      
      // Fetch Issues
      const issueRes = await getIssues();
      setIssues(issueRes);
    } catch (err) {
      console.error("Fetch error:", err);
    }
  }

  useEffect(() => { loadData() }, [])

  // Filter by search term AND current project
  const filteredIssues = issues.filter(issue => 
    issue.project_id === parseInt(currentProjectId) && (
      issue.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      issue.description.toLowerCase().includes(searchTerm.toLowerCase())
    )
  )

  const handleEditClick = (issue) => {
    setEditingIssueId(issue.id)
    setFormData({ 
      title: issue.title, 
      description: issue.description, 
      project_id: issue.project_id, 
      status: issue.status 
    })
    setShowModal(true)
  }

  const handleCloseModal = () => {
    setShowModal(false)
    setEditingIssueId(null)
    setFormData({ title: '', description: '', project_id: currentProjectId, status: 'To Do' })
  }

  const handleDragEnd = async (event) => {
    const { active, over } = event
    if (!over) return

    const issueId = active.id
    const newStatus = over.id
    const issue = issues.find(i => i.id === issueId)

    if (issue && issue.status !== newStatus) {
      setIssues(prev => prev.map(i => i.id === issueId ? { ...i, status: newStatus } : i))
      try {
        await updateIssue(issueId, { ...issue, status: newStatus })
      } catch (err) {
        loadData() 
      }
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      if (editingIssueId) {
        await updateIssue(editingIssueId, formData)
      } else {
        await createIssue({ ...formData, project_id: currentProjectId })
      }
      handleCloseModal()
      loadData()
    } catch (err) {
      console.error("Save failed:", err)
    }
  }

  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this issue?")) {
      await deleteIssue(id)
      loadData()
    }
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div className="brand">
          <h1>🐞 Bug Tracker</h1>
          <div className="project-selector-wrapper">
            <label>Project: </label>
            <select 
              value={currentProjectId} 
              onChange={(e) => setCurrentProjectId(e.target.value)}
              className="project-select"
            >
              {projects.map(p => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>
        </div>
        <div className="header-actions">
          <input 
            type="text" className="search-bar" placeholder="Search bugs..." 
            value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)}
          />
          <button className="add-button" onClick={() => setShowModal(true)}>+ New Issue</button>
        </div>
      </header>

      <DndContext sensors={sensors} collisionDetection={closestCorners} onDragEnd={handleDragEnd}>
        <main className="kanban-board">
          {['To Do', 'In Progress', 'Done'].map(status => (
            <KanbanColumn 
              key={status}
              id={status}
              title={status} 
              issues={filteredIssues.filter(i => i.status === status)} 
              onDelete={handleDelete}
              onEdit={handleEditClick}
            />
          ))}
        </main>
      </DndContext>

      {showModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h2>{editingIssueId ? '✏️ Edit Issue' : '🚀 Report New Bug'}</h2>
            <form onSubmit={handleSubmit}>
              <input 
                type="text" placeholder="Issue Title" required
                value={formData.title}
                onChange={e => setFormData({...formData, title: e.target.value})}
              />
              <textarea 
                placeholder="Description" required
                value={formData.description}
                onChange={e => setFormData({...formData, description: e.target.value})}
              />
              <div className="modal-actions">
                <button type="button" className="cancel-btn" onClick={handleCloseModal}>Cancel</button>
                <button type="submit" className="submit-btn">
                  {editingIssueId ? 'Update Issue' : 'Create Issue'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default App